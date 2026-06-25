"""
简化版真实数据处理
"""
import os
import pandas as pd
import argparse
import json
from datetime import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-date', type=str, default='2025-05-17')
    parser.add_argument('--end-date', type=str, default='2025-06-15')
    parser.add_argument('--base-date', type=str, default='2025-05-17')
    args = parser.parse_args()

    print("=" * 80)
    print("处理真实电商价格数据")
    print("=" * 80)

    # 加载主数据
    print(f"\n加载基础数据...")
    categories = pd.read_csv('data/categories.csv', encoding='gbk')
    products = pd.read_csv('data/products.csv', encoding='gbk')
    print(f"类目数: {len(categories)}, 商品数: {len(products)}")

    # 加载基期数据
    base_file = f'data/daily_price/daily_prices_{args.base_date.replace("-", "")}.csv'
    base_df = pd.read_csv(base_file, encoding='gbk')
    print(f"基期数据 ({args.base_date}): {len(base_df)} 条")

    # 计算基期价格
    base_prices = base_df.groupby('product_id')['price'].mean()

    # 处理每个日期
    from src.utils.dates import get_date_range
    dates = get_date_range(args.start_date, args.end_date)

    results = []
    for date in dates:
        date_str = date.replace("-", "")
        file_path = f'data/daily_price/daily_prices_{date_str}.csv'

        if not os.path.exists(file_path):
            print(f"跳过 {date} (文件不存在)")
            continue

        # 加载当日数据
        daily_df = pd.read_csv(file_path, encoding='gbk')

        # 计算当日平均价格
        daily_prices = daily_df.groupby('product_id')['price'].mean()

        # 计算商品指数（共同商品）
        common_products = base_prices.index.intersection(daily_prices.index)
        base_avg = base_prices[common_products].mean()
        daily_avg = daily_prices[common_products].mean()

        # 简单指数
        index_value = (daily_avg / base_avg * 100).round(2)

        results.append({
            'date': date,
            'index': index_value,
            'product_count': len(daily_df),
            'common_products': len(common_products)
        })

        print(f"{date}: 指数={index_value:.2f}, 商品数={len(daily_df)}")

    # 保存结果
    result_df = pd.DataFrame(results)
    result_df['change_pct'] = result_df['index'].pct_change() * 100
    result_df['change_pct'] = result_df['change_pct'].round(2)
    result_df.loc[0, 'change_pct'] = 0.0

    os.makedirs('output', exist_ok=True)
    result_df.to_csv('output/overall_index.csv', index=False, encoding='utf-8-sig')

    # 保存JSON
    json_data = result_df[['date', 'index', 'change_pct']].to_dict('records')
    with open('output/overall_index.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("处理完成！")
    print(f"CSV: output/overall_index.csv")
    print(f"JSON: output/overall_index.json")
    print("=" * 80)

if __name__ == '__main__':
    main()
