"""
数据查看工具（不需要安装任何依赖）
快速查看老师提供的真实数据
"""
import csv
import os

def view_categories():
    """查看类目数据"""
    print("=" * 80)
    print("类目数据 (categories.csv)")
    print("=" * 80)

    with open('data/categories.csv', 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        print(f"\n总类目数: {len(rows)}")
        print(f"\n前 10 个类目:")
        print(f"{'类目名称':<20} {'类目ID':<15} {'层级':<6} {'权重':<10}")
        print("-" * 80)

        for i, row in enumerate(rows[:10]):
            print(f"{row['category']:<20} {row['category_id']:<15} {row['hierarchy']:<6} {row['weight']:<10}")

        # 统计各层级类目数
        hierarchy_count = {}
        for row in rows:
            h = row['hierarchy']
            hierarchy_count[h] = hierarchy_count.get(h, 0) + 1

        print(f"\n层级统计:")
        for h, count in sorted(hierarchy_count.items()):
            print(f"  第 {h} 层: {count} 个类目")

def view_products():
    """查看商品数据"""
    print("\n" + "=" * 80)
    print("商品数据 (products.csv)")
    print("=" * 80)

    with open('data/products.csv', 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        print(f"\n总商品数: {len(rows)}")
        print(f"\n前 10 个商品:")
        print(f"{'商品ID':<16} {'类目ID':<15} {'商品名称':<20} {'权重':<10} {'价格':<8}")
        print("-" * 80)

        for i, row in enumerate(rows[:10]):
            name = row['name'][:18] if len(row['name']) > 18 else row['name']
            print(f"{row['product_id']:<16} {row['category_id']:<15} {name:<20} {row['weight']:<10} {row['price']:<8}")

def view_daily_prices():
    """查看每日价格数据"""
    print("\n" + "=" * 80)
    print("每日价格数据 (daily_price/)")
    print("=" * 80)

    # 统计文件数
    daily_files = sorted([f for f in os.listdir('data/daily_price') if f.endswith('.csv')])

    print(f"\n总天数: {len(daily_files)}")
    print(f"日期范围: {daily_files[0].replace('daily_prices_', '').replace('.csv', '')} 到 {daily_files[-1].replace('daily_prices_', '').replace('.csv', '')}")

    # 查看第一天的数据
    first_file = daily_files[0]
    print(f"\n查看第一天数据: {first_file}")

    with open(f'data/daily_price/{first_file}', 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        print(f"当日价格记录数: {len(rows)}")
        print(f"\n前 10 条记录:")
        print(f"{'商品ID':<16} {'类目ID':<15} {'商品名称':<20} {'价格':<8} {'日期':<12}")
        print("-" * 80)

        for i, row in enumerate(rows[:10]):
            name = row['name'][:18] if len(row['name']) > 18 else row['name']
            print(f"{row['product_id']:<16} {row['category_id']:<15} {name:<20} {row['price']:<8} {row['change_date']:<12}")

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("真实电商价格数据查看工具")
    print("=" * 80)

    try:
        view_categories()
        view_products()
        view_daily_prices()

        print("\n" + "=" * 80)
        print("数据查看完成！")
        print("\n下一步:")
        print("1. 安装 pandas: pip install pandas")
        print("2. 运行处理脚本: python process_real_data.py --start-date 2025-05-17 --end-date 2025-06-15")
        print("=" * 80)

    except FileNotFoundError as e:
        print(f"\n错误: 找不到文件 - {e}")
        print("请确保 data/ 目录存在且包含 categories.csv, products.csv 和 daily_price/ 文件夹")
    except Exception as e:
        print(f"\n错误: {e}")

if __name__ == '__main__':
    main()
