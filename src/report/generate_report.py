"""
报告生成模块
生成 DataV 可视化所需的 JSON 报告
"""
import pandas as pd
from typing import Dict, List
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class ReportGenerator:
    """报告生成器"""

    def __init__(self):
        pass

    def generate_overall_index_report(self, overall_index_df: pd.DataFrame) -> List[Dict]:
        """
        生成全网价格指数报告

        Args:
            overall_index_df: 全网指数 DataFrame

        Returns:
            JSON 数据（列表）
        """
        data = overall_index_df[['date', 'index', 'change_pct']].to_dict('records')
        logger.info(f"生成全网指数报告: {len(data)} 条记录")
        return data

    def generate_category_index_report(self, category_index_df: pd.DataFrame) -> List[Dict]:
        """
        生成类目价格指数报告

        Args:
            category_index_df: 类目指数 DataFrame

        Returns:
            JSON 数据（列表）
        """
        data = category_index_df[['date', 'category', 'index', 'change_pct']].to_dict('records')
        logger.info(f"生成类目指数报告: {len(data)} 条记录")
        return data

    def generate_sku_index_report(self, sku_index_df: pd.DataFrame, top_n: int = 100) -> List[Dict]:
        """
        生成 TOP SKU 价格指数报告

        Args:
            sku_index_df: SKU 指数 DataFrame
            top_n: 返回数量

        Returns:
            JSON 数据（列表）
        """
        # 选取最后一天销量最高的 TOP SKU
        latest_date = sku_index_df['date'].max()
        top_skus = sku_index_df[sku_index_df['date'] == latest_date].nlargest(top_n, 'total_sales')

        # 获取这些 SKU 的所有历史数据
        sku_ids = top_skus['sku_id'].tolist()
        result_df = sku_index_df[sku_index_df['sku_id'].isin(sku_ids)]

        data = result_df[['date', 'sku_id', 'product_name', 'category_l1', 'index', 'change_pct']].to_dict('records')

        # 重命名字段
        for item in data:
            item['category'] = item.pop('category_l1')

        logger.info(f"生成 TOP SKU 指数报告: {len(data)} 条记录")
        return data

    def generate_top_movers_report(self, top_movers_df: pd.DataFrame) -> List[Dict]:
        """
        生成涨跌幅 TOP 报告

        Args:
            top_movers_df: 涨跌幅 TOP DataFrame

        Returns:
            JSON 数据（列表）
        """
        data = top_movers_df.to_dict('records')

        # 重命名字段
        for item in data:
            item['category'] = item.pop('category_l1')

        logger.info(f"生成涨跌幅 TOP 报告: {len(data)} 条记录")
        return data

    def generate_daily_report(self, overall_daily_df: pd.DataFrame) -> List[Dict]:
        """
        生成每日汇总报告

        Args:
            overall_daily_df: 全网日汇总 DataFrame

        Returns:
            JSON 数据（列表）
        """
        data = overall_daily_df[['date', 'avg_price', 'total_sales', 'sku_count']].to_dict('records')
        logger.info(f"生成每日汇总报告: {len(data)} 条记录")
        return data
