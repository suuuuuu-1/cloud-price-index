"""
从 ClickHouse 查询并计算价格指数
"""
import clickhouse_connect
import pandas as pd
import os
import json

def get_client():
    """创建 ClickHouse 客户端"""
    return clickhouse_connect.get_client(
        host=os.getenv('CLICKHOUSE_HOST', 'localhost'),
        port=int(os.getenv('CLICKHOUSE_PORT', 8123)),
        username=os.getenv('CLICKHOUSE_USER', 'default'),
        password=os.getenv('CLICKHOUSE_PASSWORD', '')
    )

def compute_index_from_clickhouse(start_date, end_date, base_date):
    """从 ClickHouse 计算价格指数"""
    client = get_client()

    # 查询基期价格
    base_query = f"""
    SELECT
        product_id,
        avg(price) as base_price
    FROM raw_product_price_detail
    WHERE date = '{base_date}'
    GROUP BY product_id
    """
    base_df = client.query_df(base_query)

    # 查询每日价格
    daily_query = f"""
    SELECT
        date,
        product_id,
        avg(price) as current_price
    FROM raw_product_price_detail
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY date, product_id
    """
    daily_df = client.query_df(daily_query)

    # 合并计算指数
    df = daily_df.merge(base_df, on='product_id')
    df['product_index'] = (df['current_price'] / df['base_price'] * 100).round(2)

    # 计算全网指数
    result = df.groupby('date').agg({
        'product_index': 'mean',
        'product_id': 'count'
    }).reset_index()

    result.columns = ['date', 'index', 'product_count']
    result['index'] = result['index'].round(2)

    # 计算环比
    result['change_pct'] = result['index'].pct_change() * 100
    result['change_pct'] = result['change_pct'].round(2)
    result.loc[0, 'change_pct'] = 0.0

    return result

def main():
    """主函数"""
    print("=" * 80)
    print("从 ClickHouse 计算价格指数")
    print("=" * 80)

    result = compute_index_from_clickhouse('2025-05-17', '2025-06-15', '2025-05-17')

    # 保存结果
    os.makedirs('output', exist_ok=True)
    result.to_csv('output/clickhouse_index.csv', index=False, encoding='utf-8-sig')

    json_data = result[['date', 'index', 'change_pct']].to_dict('records')
    with open('output/clickhouse_index.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"\n{result.to_string()}")
    print("\n" + "=" * 80)
    print("完成！结果保存到 output/clickhouse_index.csv")
    print("=" * 80)

if __name__ == '__main__':
    main()
