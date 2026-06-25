"""
真实数据处理主程序
处理老师提供的真实电商价格数据
"""
import os
import pandas as pd
import argparse
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def load_categories():
    """加载类目数据"""
    df = pd.read_csv('data/categories.csv', encoding='gbk')
    logger.info(f"加载类目数据: {len(df)} 条记录")
    return df

def load_products():
    """加载商品数据"""
    df = pd.read_csv('data/products.csv', encoding='gbk')
    logger.info(f"加载商品数据: {len(df)} 条记录")
    return df

def load_daily_prices(date_str):
    """加载指定日期的价格数据"""
    file_path = f'data/daily_price/daily_prices_{date_str.replace("-", "")}.csv'
    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        return None

    df = pd.read_csv(file_path, encoding='gbk')
    logger.info(f"加载 {date_str} 价格数据: {len(df)} 条记录")
    return df

def compute_category_index(daily_df, products_df, categories_df, base_date_df):
    """计算类目价格指数"""
    # 合并商品信息
    df = daily_df.merge(products_df[['product_id', 'category_id', 'weight']],
                       on='product_id', how='left', suffixes=('', '_prod'))

    # 合并类目信息（daily_df已有category_id，使用_prod的）
    df = df.merge(categories_df[['category_id', 'category', 'hierarchy']],
                 left_on='category_id_prod', right_on='category_id', how='left')

    # 计算基期价格（使用 category_id_prod）
    base_df = base_date_df.merge(products_df[['product_id', 'category_id', 'weight']],
                                  on='product_id', how='left')
    base_prices = base_df.groupby('category_id')['price'].mean().reset_index()
    base_prices.columns = ['category_id_prod', 'base_price']

    # 当期价格（使用 category_id_prod）
    current_prices = df.groupby('category_id_prod')['price'].mean().reset_index()
    current_prices.columns = ['category_id_prod', 'current_price']

    # 计算指数
    result = current_prices.merge(base_prices, on='category_id_prod')
    result = result.merge(categories_df[['category_id', 'category', 'weight']],
                         left_on='category_id_prod', right_on='category_id')

    result['index'] = (result['current_price'] / result['base_price'] * 100).round(2)

    return result

def compute_overall_index(category_index_df):
    """计算全网加权价格指数"""
    total_weight = category_index_df['weight'].sum()
    overall_index = (category_index_df['index'] * category_index_df['weight']).sum() / total_weight
    return round(overall_index, 2)

def main():
    parser = argparse.ArgumentParser(description='处理真实电商价格数据')
    parser.add_argument('--start-date', type=str, default='2025-05-17', help='开始日期 YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, default='2025-06-15', help='结束日期 YYYY-MM-DD')
    parser.add_argument('--base-date', type=str, default='2025-05-17', help='基期日期 YYYY-MM-DD')
    args = parser.parse_args()

    logger.info("="*80)
    logger.info("开始处理真实电商价格数据")
    logger.info("="*80)

    # 加载主数据
    categories_df = load_categories()
    products_df = load_products()

    # 加载基期数据
    base_date_df = load_daily_prices(args.base_date)
    if base_date_df is None:
        logger.error(f"无法加载基期数据: {args.base_date}")
        return

    # 生成日期列表
    from src.utils.dates import get_date_range
    dates = get_date_range(args.start_date, args.end_date)

    # 处理每个日期
    results = []
    for date in dates:
        logger.info(f"\n处理日期: {date}")

        daily_df = load_daily_prices(date)
        if daily_df is None:
            continue

        # 计算类目指数
        category_index = compute_category_index(daily_df, products_df, categories_df, base_date_df)

        # 计算全网指数
        overall_index = compute_overall_index(category_index)

        result = {
            'date': date,
            'overall_index': overall_index,
            'product_count': len(daily_df),
            'category_count': len(category_index)
        }
        results.append(result)

        logger.info(f"全网指数: {overall_index}, 商品数: {len(daily_df)}")

    # 保存结果
    result_df = pd.DataFrame(results)
    result_df['change_pct'] = result_df['overall_index'].pct_change() * 100
    result_df['change_pct'] = result_df['change_pct'].round(2)
    result_df.loc[0, 'change_pct'] = 0.0

    os.makedirs('output', exist_ok=True)
    result_df.to_csv('output/overall_index.csv', index=False, encoding='utf-8-sig')

    # 输出 JSON
    import json
    with open('output/overall_index.json', 'w', encoding='utf-8') as f:
        json.dump(result_df.to_dict('records'), f, ensure_ascii=False, indent=2)

    logger.info("\n" + "="*80)
    logger.info("处理完成！")
    logger.info(f"结果已保存到: output/overall_index.csv")
    logger.info(f"JSON 已保存到: output/overall_index.json")
    logger.info("="*80)

if __name__ == '__main__':
    main()
