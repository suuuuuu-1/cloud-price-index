"""
价格指数计算模块
基于汇总数据计算价格指数，生成 ADS 层数据
"""
import pandas as pd
from typing import Dict, List
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class IndexCalculator:
    """价格指数计算器"""

    def __init__(self, base_date: str):
        """
        初始化计算器

        Args:
            base_date: 基期日期
        """
        self.base_date = base_date

    def compute_sku_index(self, sku_daily_df: pd.DataFrame) -> pd.DataFrame:
        """
        计算 SKU 价格指数

        Args:
            sku_daily_df: SKU 日汇总 DataFrame

        Returns:
            SKU 指数 DataFrame
        """
        # 获取基期价格
        base_df = sku_daily_df[sku_daily_df['date'] == self.base_date][['sku_id', 'avg_price']]
        base_df.columns = ['sku_id', 'base_price']

        # 合并基期价格
        index_df = sku_daily_df.merge(base_df, on='sku_id', how='left')

        # 计算指数
        index_df['index'] = (index_df['avg_price'] / index_df['base_price'] * 100).round(2)

        # 按 SKU 排序，计算环比涨跌幅
        index_df = index_df.sort_values(['sku_id', 'date'])
        index_df['prev_index'] = index_df.groupby('sku_id')['index'].shift(1)
        index_df['change_pct'] = ((index_df['index'] / index_df['prev_index'] - 1) * 100).round(2)

        # 第一天没有环比
        index_df.loc[index_df['date'] == self.base_date, 'change_pct'] = 0

        return index_df

    def compute_category_index(self, sku_index_df: pd.DataFrame) -> pd.DataFrame:
        """
        计算类目价格指数

        Args:
            sku_index_df: SKU 指数 DataFrame

        Returns:
            类目指数 DataFrame
        """
        # 计算 SKU 销量权重
        sku_index_df['weight'] = sku_index_df.groupby(['date', 'category_l1'])['total_sales'].transform(
            lambda x: x / x.sum()
        )

        # 加权求和得到类目指数
        category_index = sku_index_df.groupby(['date', 'category_l1']).apply(
            lambda x: (x['index'] * x['weight']).sum()
        ).reset_index()
        category_index.columns = ['date', 'category', 'index']
        category_index['index'] = category_index['index'].round(2)

        # 计算环比涨跌幅
        category_index = category_index.sort_values(['category', 'date'])
        category_index['prev_index'] = category_index.groupby('category')['index'].shift(1)
        category_index['change_pct'] = ((category_index['index'] / category_index['prev_index'] - 1) * 100).round(2)

        # 第一天没有环比
        category_index.loc[category_index['date'] == self.base_date, 'change_pct'] = 0

        return category_index

    def compute_overall_index(self, category_index_df: pd.DataFrame,
                               category_daily_df: pd.DataFrame) -> pd.DataFrame:
        """
        计算全网价格指数

        Args:
            category_index_df: 类目指数 DataFrame
            category_daily_df: 类目日汇总 DataFrame

        Returns:
            全网指数 DataFrame
        """
        # 合并类目销量
        merged_df = category_index_df.merge(
            category_daily_df[['date', 'category', 'total_sales']],
            on=['date', 'category'],
            how='left'
        )

        # 计算类目销量权重
        merged_df['weight'] = merged_df.groupby('date')['total_sales'].transform(
            lambda x: x / x.sum()
        )

        # 加权求和得到全网指数
        overall_index = merged_df.groupby('date').apply(
            lambda x: (x['index'] * x['weight']).sum()
        ).reset_index()
        overall_index.columns = ['date', 'index']
        overall_index['index'] = overall_index['index'].round(2)

        # 计算环比涨跌幅
        overall_index = overall_index.sort_values('date')
        overall_index['prev_index'] = overall_index['index'].shift(1)
        overall_index['change_pct'] = ((overall_index['index'] / overall_index['prev_index'] - 1) * 100).round(2)

        # 第一天没有环比
        overall_index.loc[overall_index['date'] == self.base_date, 'change_pct'] = 0

        return overall_index

    def get_top_movers(self, sku_index_df: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
        """
        获取涨跌幅 TOP 商品

        Args:
            sku_index_df: SKU 指数 DataFrame
            top_n: 返回数量

        Returns:
            涨跌幅 TOP DataFrame
        """
        # 过滤掉基期日期（没有涨跌幅）
        df = sku_index_df[sku_index_df['date'] != self.base_date].copy()

        # 按日期分组，取每天涨跌幅最大和最小的 SKU
        top_gainers = df.sort_values('change_pct', ascending=False).groupby('date').head(top_n // 2)
        top_losers = df.sort_values('change_pct', ascending=True).groupby('date').head(top_n // 2)

        top_movers = pd.concat([top_gainers, top_losers]).sort_values(['date', 'change_pct'], ascending=[True, False])

        return top_movers[['date', 'sku_id', 'product_name', 'category_l1', 'index', 'change_pct']]
