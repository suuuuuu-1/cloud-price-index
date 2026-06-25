"""
价格指数计算单元测试
"""
import unittest
import pandas as pd
from src.compute.compute_index import IndexCalculator

class TestIndexCalculator(unittest.TestCase):
    """测试价格指数计算"""

    def setUp(self):
        """初始化测试数据"""
        self.base_date = "2026-06-01"
        self.calculator = IndexCalculator(self.base_date)

        # 构建测试数据
        self.sku_daily_df = pd.DataFrame([
            {"date": "2026-06-01", "sku_id": "SKU001", "product_name": "商品A", "category_l1": "手机数码",
             "category_l2": "手机", "brand": "华为", "avg_price": 3000.0, "total_sales": 100,
             "platform_count": 3, "shop_count": 5},
            {"date": "2026-06-02", "sku_id": "SKU001", "product_name": "商品A", "category_l1": "手机数码",
             "category_l2": "手机", "brand": "华为", "avg_price": 3150.0, "total_sales": 120,
             "platform_count": 3, "shop_count": 5},
            {"date": "2026-06-01", "sku_id": "SKU002", "product_name": "商品B", "category_l1": "电脑办公",
             "category_l2": "笔记本", "brand": "联想", "avg_price": 5000.0, "total_sales": 80,
             "platform_count": 3, "shop_count": 4},
            {"date": "2026-06-02", "sku_id": "SKU002", "product_name": "商品B", "category_l1": "电脑办公",
             "category_l2": "笔记本", "brand": "联想", "avg_price": 4900.0, "total_sales": 90,
             "platform_count": 3, "shop_count": 4},
        ])

    def test_compute_sku_index(self):
        """测试 SKU 指数计算"""
        sku_index = self.calculator.compute_sku_index(self.sku_daily_df)

        # 检查基期指数为 100
        base_sku001 = sku_index[(sku_index['date'] == self.base_date) & (sku_index['sku_id'] == 'SKU001')]
        self.assertEqual(base_sku001.iloc[0]['index'], 100.0)

        # 检查第二天指数计算
        day2_sku001 = sku_index[(sku_index['date'] == '2026-06-02') & (sku_index['sku_id'] == 'SKU001')]
        expected_index = 3150.0 / 3000.0 * 100
        self.assertAlmostEqual(day2_sku001.iloc[0]['index'], expected_index, places=2)

        # 检查环比涨跌幅
        expected_change_pct = (105.0 / 100.0 - 1) * 100
        self.assertAlmostEqual(day2_sku001.iloc[0]['change_pct'], expected_change_pct, places=2)

    def test_compute_category_index(self):
        """测试类目指数计算"""
        sku_index = self.calculator.compute_sku_index(self.sku_daily_df)
        category_index = self.calculator.compute_category_index(sku_index)

        # 检查类目数量
        unique_categories = category_index['category'].nunique()
        self.assertEqual(unique_categories, 2)

        # 检查基期指数为 100
        base_category = category_index[category_index['date'] == self.base_date]
        for idx, row in base_category.iterrows():
            self.assertEqual(row['index'], 100.0)

    def test_compute_overall_index(self):
        """测试全网指数计算"""
        sku_index = self.calculator.compute_sku_index(self.sku_daily_df)
        category_index = self.calculator.compute_category_index(sku_index)

        category_daily = self.sku_daily_df.groupby(['date', 'category_l1']).agg({
            'avg_price': 'mean',
            'total_sales': 'sum',
            'sku_id': 'nunique'
        }).reset_index()
        category_daily.columns = ['date', 'category', 'avg_price', 'total_sales', 'sku_count']

        overall_index = self.calculator.compute_overall_index(category_index, category_daily)

        # 检查基期指数为 100
        base_overall = overall_index[overall_index['date'] == self.base_date]
        self.assertEqual(base_overall.iloc[0]['index'], 100.0)

        # 检查日期数量
        self.assertEqual(len(overall_index), 2)

if __name__ == '__main__':
    unittest.main()
