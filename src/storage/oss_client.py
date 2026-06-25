"""
OSS 客户端模块
处理阿里云 OSS 存储操作
"""
import os
import oss2
import pandas as pd
from typing import Dict
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class OSSClient:
    """阿里云 OSS 客户端"""

    def __init__(self, endpoint: str, access_key_id: str, access_key_secret: str,
                 bucket_name: str, prefix: str = ""):
        """
        初始化 OSS 客户端

        Args:
            endpoint: OSS endpoint
            access_key_id: AccessKey ID
            access_key_secret: AccessKey Secret
            bucket_name: Bucket 名称
            prefix: 对象前缀
        """
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
        self.prefix = prefix.rstrip('/')

    def _get_object_key(self, layer: str, table_name: str, file_name: str, date: str = None) -> str:
        """
        构建对象键

        Args:
            layer: 数据层
            table_name: 表名
            file_name: 文件名
            date: 日期分区（可选）

        Returns:
            对象键
        """
        if date:
            return f"{self.prefix}/{layer}/{table_name}/dt={date}/{file_name}"
        else:
            return f"{self.prefix}/{layer}/{file_name}"

    def upload_csv(self, df: pd.DataFrame, layer: str, table_name: str, date: str = None):
        """
        上传 DataFrame 为 CSV 到 OSS

        Args:
            df: 数据 DataFrame
            layer: 数据层
            table_name: 表名
            date: 日期分区（可选）
        """
        # 将 DataFrame 转换为 CSV 字符串
        csv_content = df.to_csv(index=False, encoding='utf-8-sig')

        # 构建对象键
        object_key = self._get_object_key(layer, table_name, f"{table_name}.csv", date)

        # 上传到 OSS
        self.bucket.put_object(object_key, csv_content.encode('utf-8-sig'))
        logger.info(f"上传 CSV 到 OSS: {object_key}")

    def upload_json(self, data: Dict or list, layer: str, file_name: str):
        """
        上传 JSON 到 OSS

        Args:
            data: 数据（字典或列表）
            layer: 数据层
            file_name: 文件名
        """
        import json

        # 转换为 JSON 字符串
        json_content = json.dumps(data, ensure_ascii=False, indent=2)

        # 构建对象键
        object_key = self._get_object_key(layer, "", file_name)

        # 上传到 OSS
        self.bucket.put_object(object_key, json_content.encode('utf-8'))
        logger.info(f"上传 JSON 到 OSS: {object_key}")

    def download_csv(self, layer: str, table_name: str, date: str = None) -> pd.DataFrame:
        """
        从 OSS 下载 CSV

        Args:
            layer: 数据层
            table_name: 表名
            date: 日期分区（可选）

        Returns:
            DataFrame
        """
        object_key = self._get_object_key(layer, table_name, f"{table_name}.csv", date)

        result = self.bucket.get_object(object_key)
        content = result.read().decode('utf-8-sig')

        import io
        return pd.read_csv(io.StringIO(content))

    def list_dates(self, layer: str, table_name: str) -> list:
        """
        列出某个表的所有日期分区

        Args:
            layer: 数据层
            table_name: 表名

        Returns:
            日期列表
        """
        prefix = f"{self.prefix}/{layer}/{table_name}/dt="
        dates = set()

        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            # 从路径中提取日期
            parts = obj.key.split('/')
            for part in parts:
                if part.startswith('dt='):
                    dates.add(part.replace('dt=', ''))

        return sorted(list(dates))
