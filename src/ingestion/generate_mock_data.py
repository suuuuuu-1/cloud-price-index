"""
模拟数据生成模块
生成模拟的电商商品价格数据
"""
import pandas as pd
import random
from datetime import datetime
from typing import Dict, List
from src.utils.logger import setup_logger
from src.utils.dates import get_day_of_week

logger = setup_logger(__name__)

class MockDataGenerator:
    """模拟数据生成器"""

    def __init__(self, config: Dict):
        """
        初始化生成器

        Args:
            config: 配置字典
        """
        self.config = config
        self.categories = config['categories']
        self.platforms = config['platforms']
        self.sku_count = config['sku_count']

        # 类目价格范围配置
        self.category_price_ranges = {
            "手机数码": (2000, 8000),
            "电脑办公": (3000, 15000),
            "家用电器": (500, 5000),
            "食品饮料": (10, 200),
            "服饰鞋包": (50, 500),
            "美妆个护": (30, 800),
            "运动户外": (100, 2000),
            "日用百货": (5, 100)
        }

        # 生成商品主数据
        self.skus = self._generate_skus()

    def _generate_skus(self) -> List[Dict]:
        """生成 SKU 主数据"""
        skus = []
        brands = ["华为", "小米", "苹果", "OPPO", "vivo", "联想", "戴尔", "惠普", "海尔", "美的",
                  "三只松鼠", "百草味", "优衣库", "耐克", "阿迪达斯", "欧莱雅", "兰蔻", "雅诗兰黛"]

        for i in range(self.sku_count):
            category = random.choice(self.categories)
            price_range = self.category_price_ranges[category]
            base_price = random.uniform(price_range[0], price_range[1])

            sku = {
                'sku_id': f"SKU{str(i+1).zfill(4)}",
                'product_id': f"PROD{str(i+1).zfill(4)}",
                'product_name': f"{category}商品{i+1}",
                'category_l1': category,
                'category_l2': f"{category}子类{random.randint(1, 3)}",
                'brand': random.choice(brands),
                'base_price': round(base_price, 2)
            }
            skus.append(sku)

        return skus

    def generate_data_for_date(self, date_str: str) -> pd.DataFrame:
        """
        生成指定日期的商品价格数据

        Args:
            date_str: 日期字符串，格式 YYYY-MM-DD

        Returns:
            价格数据 DataFrame
        """
        # 判断是否是促销日（周六）
        is_promo_day = get_day_of_week(date_str) == self.config.get('promo_day_of_week', 6)

        records = []
        for sku in self.skus:
            # 每个 SKU 在多个店铺销售
            num_shops = random.randint(
                self.config.get('shops_per_sku_min', 2),
                self.config.get('shops_per_sku_max', 5)
            )

            for shop_idx in range(num_shops):
                platform = random.choice(self.platforms)
                shop_id = f"SHOP{platform[:1]}{random.randint(1000, 9999)}"

                # 计算价格
                base_price = sku['base_price']
                fluctuation = self.config.get('price_fluctuation', 0.05)
                price = base_price * (1 + random.uniform(-fluctuation, fluctuation))

                # 促销日价格
                if is_promo_day:
                    discount = random.uniform(
                        self.config.get('promo_discount_min', 0.10),
                        self.config.get('promo_discount_max', 0.30)
                    )
                    price = price * (1 - discount)

                # 计算销量
                base_sales = random.randint(10, 100)
                if is_promo_day:
                    multiplier = random.uniform(
                        self.config.get('promo_sales_multiplier_min', 2),
                        self.config.get('promo_sales_multiplier_max', 5)
                    )
                    base_sales = int(base_sales * multiplier)

                record = {
                    'date': date_str,
                    'sku_id': sku['sku_id'],
                    'product_id': sku['product_id'],
                    'product_name': sku['product_name'],
                    'category_l1': sku['category_l1'],
                    'category_l2': sku['category_l2'],
                    'brand': sku['brand'],
                    'platform': platform,
                    'shop_id': shop_id,
                    'price': round(price, 2),
                    'sales': base_sales,
                    'is_promo': 1 if is_promo_day else 0,
                    'collect_time': f"{date_str} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
                }
                records.append(record)

        df = pd.DataFrame(records)

        # 添加脏数据
        df = self._add_dirty_data(df)

        logger.info(f"生成 {date_str} 的数据: {len(df)} 条记录")
        return df

    def _add_dirty_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加脏数据

        Args:
            df: 原始数据 DataFrame

        Returns:
            添加脏数据后的 DataFrame
        """
        dirty_rate = self.config.get('dirty_data_rate', 0.02)
        num_dirty = int(len(df) * dirty_rate)

        if num_dirty == 0:
            return df

        # 随机选择要污染的行
        dirty_indices = random.sample(range(len(df)), num_dirty)

        for idx in dirty_indices:
            dirty_type = random.choice(['negative_price', 'negative_sales', 'empty_name', 'price_spike', 'duplicate'])

            if dirty_type == 'negative_price':
                df.at[idx, 'price'] = random.uniform(-100, 0)
            elif dirty_type == 'negative_sales':
                df.at[idx, 'sales'] = random.randint(-100, -1)
            elif dirty_type == 'empty_name':
                df.at[idx, 'product_name'] = ''
            elif dirty_type == 'price_spike':
                df.at[idx, 'price'] = df.at[idx, 'price'] * random.uniform(10, 20)
            elif dirty_type == 'duplicate':
                # 复制该行（会在后续去重时被识别）
                pass

        return df
