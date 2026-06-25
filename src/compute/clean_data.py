"""
数据清洗模块
对原始数据进行清洗，生成 DWD 层数据
"""
import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DataCleaner:
    """数据清洗器"""

    def __init__(self):
        pass

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据

        清洗规则：
        1. 删除 price <= 0 的记录
        2. 删除 sales < 0 的记录
        3. 删除商品名称为空的记录
        4. 删除价格异常暴涨的记录
        5. 去除重复报价

        Args:
            df: 原始数据 DataFrame

        Returns:
            清洗后的 DataFrame
        """
        original_count = len(df)

        # 1. 删除价格小于等于 0 的记录
        df = df[df['price'] > 0]

        # 2. 删除销量小于 0 的记录
        df = df[df['sales'] >= 0]

        # 3. 删除商品名称为空的记录
        df = df[df['product_name'].notna() & (df['product_name'] != '')]

        # 4. 删除价格异常暴涨的记录
        # 使用统计方法：删除价格超过中位数 10 倍的记录
        price_median = df.groupby('sku_id')['price'].transform('median')
        df = df[df['price'] <= price_median * 10]

        # 5. 去除重复报价（相同 SKU、平台、店铺、日期）
        df = df.drop_duplicates(subset=['date', 'sku_id', 'platform', 'shop_id'], keep='first')

        # 重置索引
        df = df.reset_index(drop=True)

        cleaned_count = len(df)
        removed_count = original_count - cleaned_count
        removal_rate = removed_count / original_count * 100 if original_count > 0 else 0

        logger.info(f"数据清洗完成: 原始 {original_count} 条, 清洗后 {cleaned_count} 条, "
                    f"删除 {removed_count} 条 ({removal_rate:.2f}%)")

        return df
