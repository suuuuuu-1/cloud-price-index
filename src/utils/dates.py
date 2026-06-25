"""
日期工具模块
提供日期处理相关的工具函数
"""
from datetime import datetime, timedelta
from typing import List

def parse_date(date_str: str) -> datetime:
    """
    解析日期字符串

    Args:
        date_str: 日期字符串，格式 YYYY-MM-DD

    Returns:
        datetime 对象
    """
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(date: datetime) -> str:
    """
    格式化日期为字符串

    Args:
        date: datetime 对象

    Returns:
        日期字符串，格式 YYYY-MM-DD
    """
    return date.strftime("%Y-%m-%d")

def get_date_range(start_date: str, end_date: str) -> List[str]:
    """
    获取日期范围内的所有日期

    Args:
        start_date: 开始日期，格式 YYYY-MM-DD
        end_date: 结束日期，格式 YYYY-MM-DD

    Returns:
        日期字符串列表
    """
    start = parse_date(start_date)
    end = parse_date(end_date)

    dates = []
    current = start
    while current <= end:
        dates.append(format_date(current))
        current += timedelta(days=1)

    return dates

def get_day_of_week(date_str: str) -> int:
    """
    获取日期是星期几

    Args:
        date_str: 日期字符串，格式 YYYY-MM-DD

    Returns:
        星期几（0=周一, 6=周日）
    """
    date = parse_date(date_str)
    return date.weekday()
