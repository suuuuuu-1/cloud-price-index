"""
数据汇总模块
对清洗后的数据进行汇总，生成 DWS 层数据
"""
import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DataAggregator:
    """数据汇总器"""

    def __init__(self):
        pass

    def aggregate_sku_daily(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        SKU 日汇总

        Args:
            df: 清洗后的数据 DataFrame

        Returns:
            SKU 日汇总 DataFrame
        """
        agg_df = df.groupby(['date', 'sku_id', 'product_name', 'category_l1', 'category_l2', 'brand']).agg({
            'price': 'mean',  # 平均价格
            'sales': 'sum',   # 总销量
            'platform': 'nunique',  # 平台数
            'shop_id': 'nunique'    # 店铺数
        }).reset_index()

        agg_df.columns = ['date', 'sku_id', 'product_name', 'category_l1', 'category_l2', 'brand',
                          'avg_price', 'total_sales', 'platform_count', 'shop_count']

        # 四舍五入
        agg_df['avg_price'] = agg_df['avg_price'].round(2)

        logger.info(f"SKU 日汇总完成: {len(agg_df)} 条记录")
        return agg_df

    def aggregate_category_daily(self, sku_daily_df: pd.DataFrame) -> pd.DataFrame:
        """
        类目日汇总

        Args:
            sku_daily_df: SKU 日汇总 DataFrame

        Returns:
            类目日汇总 DataFrame
        """
        agg_df = sku_daily_df.groupby(['date', 'category_l1']).agg({
            'avg_price': 'mean',  # 类目平均价格
            'total_sales': 'sum',  # 类目总销量
            'sku_id': 'nunique'    # SKU 数量
        }).reset_index()

        agg_df.columns = ['date', 'category', 'avg_price', 'total_sales', 'sku_count']

        # 四舍五入
        agg_df['avg_price'] = agg_df['avg_price'].round(2)

        logger.info(f"类目日汇总完成: {len(agg_df)} 条记录")
        return agg_df

    def aggregate_overall_daily(self, sku_daily_df: pd.DataFrame) -> pd.DataFrame:
        """
        全网日汇总

        Args:
            sku_daily_df: SKU 日汇总 DataFrame

        Returns:
            全网日汇总 DataFrame
        """
        agg_df = sku_daily_df.groupby('date').agg({
            'avg_price': 'mean',   # 全网平均价格
            'total_sales': 'sum',  # 全网总销量
            'sku_id': 'nunique'    # 全网 SKU 数量
        }).reset_index()

        agg_df.columns = ['date', 'avg_price', 'total_sales', 'sku_count']

        # 四舍五入
        agg_df['avg_price'] = agg_df['avg_price'].round(2)

        logger.info(f"全网日汇总完成: {len(agg_df)} 条记录")
        return agg_df
