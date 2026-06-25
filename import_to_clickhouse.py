"""
导入数据到 ClickHouse
"""
import pandas as pd
import clickhouse_connect
from datetime import datetime
import os

def get_clickhouse_client():
    """创建 ClickHouse 客户端"""
    client = clickhouse_connect.get_client(
        host=os.getenv('CLICKHOUSE_HOST', 'localhost'),
        port=int(os.getenv('CLICKHOUSE_PORT', 8123)),
        username=os.getenv('CLICKHOUSE_USER', 'default'),
        password=os.getenv('CLICKHOUSE_PASSWORD', '')
    )
    return client

def create_tables(client):
    """创建表结构"""
    # 读取并执行 SQL
    with open('sql/clickhouse_schema.sql', 'r', encoding='utf-8') as f:
        sql_statements = f.read().split(';')

    for sql in sql_statements:
        sql = sql.strip()
        if sql and not sql.startswith('--'):
            print(f"执行: {sql[:50]}...")
            client.command(sql)

    print("✓ 表结构创建完成")

def import_daily_prices(client, date_str):
    """导入每日价格数据"""
    file_path = f'data/daily_price/daily_prices_{date_str.replace("-", "")}.csv'

    if not os.path.exists(file_path):
        return

    df = pd.read_csv(file_path, encoding='gbk')

    # 准备数据
    data = []
    for _, row in df.iterrows():
        data.append({
            'date': row['change_date'],
            'sku_id': str(row['product_id']),
            'product_name': row['name'],
            'category_id': str(row['category_id']),
            'price': float(row['price'])
        })

    # 批量插入
    client.insert('raw_product_price_detail', data)
    print(f"✓ 导入 {date_str}: {len(data)} 条")

def import_categories(client):
    """导入类目数据"""
    df = pd.read_csv('data/categories.csv', encoding='gbk')

    data = []
    for _, row in df.iterrows():
        data.append({
            'category_id': str(row['category_id']),
            'category_name': row['category'],
            'hierarchy': int(row['hierarchy']),
            'weight': float(row['weight']),
            'parent_id': str(row['parent']) if pd.notna(row['parent']) else ''
        })

    client.insert('dim_category', data)
    print(f"✓ 导入类目: {len(data)} 条")

def import_products(client):
    """导入商品数据"""
    df = pd.read_csv('data/products.csv', encoding='gbk')

    data = []
    for _, row in df.iterrows():
        data.append({
            'product_id': str(row['product_id']),
            'category_id': str(row['category_id']),
            'product_name': row['name'],
            'weight': float(row['weight']),
            'base_price': float(row['price'])
        })

    client.insert('dim_product', data)
    print(f"✓ 导入商品: {len(data)} 条")

def main():
    """主函数"""
    print("=" * 80)
    print("导入数据到 ClickHouse")
    print("=" * 80)

    # 连接
    client = get_clickhouse_client()
    print(f"✓ 连接成功: {client.server_version}")

    # 创建表
    create_tables(client)

    # 导入基础数据
    import_categories(client)
    import_products(client)

    # 导入价格数据（示例：导入前 30 天）
    from src.utils.dates import get_date_range
    dates = get_date_range('2025-05-17', '2025-06-15')

    for date in dates:
        import_daily_prices(client, date)

    print("\n" + "=" * 80)
    print("导入完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()
