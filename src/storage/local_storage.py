"""
本地存储模块
处理本地文件存储操作
"""
import os
import pandas as pd
from typing import Dict
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class LocalStorage:
    """本地存储管理器"""

    def __init__(self, base_dir: str = "data"):
        """
        初始化本地存储

        Args:
            base_dir: 数据根目录
        """
        self.base_dir = base_dir
        self._ensure_directories()

    def _ensure_directories(self):
        """确保所有必要的目录存在"""
        layers = ["ods", "dwd", "dws", "ads"]
        for layer in layers:
            os.makedirs(os.path.join(self.base_dir, layer), exist_ok=True)

    def save_csv(self, df: pd.DataFrame, layer: str, table_name: str, date: str = None):
        """
        保存 DataFrame 为 CSV 文件

        Args:
            df: 数据 DataFrame
            layer: 数据层（ods/dwd/dws/ads）
            table_name: 表名
            date: 日期分区（可选）
        """
        if date:
            # 带日期分区
            dir_path = os.path.join(self.base_dir, layer, table_name, f"dt={date}")
            os.makedirs(dir_path, exist_ok=True)
            file_path = os.path.join(dir_path, f"{table_name}.csv")
        else:
            # 不带日期分区
            file_path = os.path.join(self.base_dir, layer, f"{table_name}.csv")

        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        logger.info(f"保存 CSV 文件: {file_path}")

    def save_json(self, data: Dict or list, layer: str, file_name: str):
        """
        保存 JSON 文件

        Args:
            data: 数据（字典或列表）
            layer: 数据层（通常是 ads）
            file_name: 文件名
        """
        import json

        file_path = os.path.join(self.base_dir, layer, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"保存 JSON 文件: {file_path}")

    def read_csv(self, layer: str, table_name: str, date: str = None) -> pd.DataFrame:
        """
        读取 CSV 文件

        Args:
            layer: 数据层
            table_name: 表名
            date: 日期分区（可选）

        Returns:
            DataFrame
        """
        if date:
            file_path = os.path.join(self.base_dir, layer, table_name, f"dt={date}", f"{table_name}.csv")
        else:
            file_path = os.path.join(self.base_dir, layer, f"{table_name}.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        return pd.read_csv(file_path)

    def get_all_dates(self, layer: str, table_name: str) -> list:
        """
        获取某个表的所有日期分区

        Args:
            layer: 数据层
            table_name: 表名

        Returns:
            日期列表
        """
        table_dir = os.path.join(self.base_dir, layer, table_name)
        if not os.path.exists(table_dir):
            return []

        dates = []
        for item in os.listdir(table_dir):
            if item.startswith("dt="):
                dates.append(item.replace("dt=", ""))

        return sorted(dates)
