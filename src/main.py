"""
主程序入口
一键运行完整的数据处理流程
"""
import os
import argparse
import yaml
from dotenv import load_dotenv
from src.utils.logger import setup_logger
from src.utils.dates import get_date_range
from src.ingestion.generate_mock_data import MockDataGenerator
from src.compute.clean_data import DataCleaner
from src.compute.aggregate_data import DataAggregator
from src.compute.compute_index import IndexCalculator
from src.report.generate_report import ReportGenerator
from src.storage.local_storage import LocalStorage
from src.storage.oss_client import OSSClient
import pandas as pd

logger = setup_logger(__name__)

def load_config():
    """加载配置文件"""
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='云价格指数计算平台')
    parser.add_argument('--date', type=str, help='指定单个日期，格式 YYYY-MM-DD')
    parser.add_argument('--start-date', type=str, help='指定开始日期，格式 YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, help='指定结束日期，格式 YYYY-MM-DD')
    return parser.parse_args()

def get_storage_clients(config):
    """获取存储客户端"""
    load_dotenv()
    local_storage = LocalStorage()
    oss_client = None
    oss_enabled = os.getenv('OSS_ENABLED', 'false').lower() == 'true'

    if oss_enabled:
        endpoint = os.getenv('ALIYUN_OSS_ENDPOINT')
        bucket = os.getenv('ALIYUN_OSS_BUCKET')
        access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
        access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
        prefix = os.getenv('OSS_PREFIX', 'price-index-platform')

        if all([endpoint, bucket, access_key_id, access_key_secret]):
            oss_client = OSSClient(endpoint, access_key_id, access_key_secret, bucket, prefix)
            logger.info("OSS 存储已启用")
        else:
            logger.warning("OSS 配置不完整，只使用本地存储")

    return local_storage, oss_client

def process_date(date, config, data_generator, cleaner, aggregator, local_storage, oss_client=None):
    """处理单个日期的数据"""
    logger.info(f"开始处理日期: {date}")
    
    logger.info("Step 1: 生成原始数据 (ODS)")
    ods_df = data_generator.generate_data_for_date(date)
    local_storage.save_csv(ods_df, 'ods', 'product_price_raw', date)
    if oss_client:
        oss_client.upload_csv(ods_df, 'ods', 'product_price_raw', date)
    
    logger.info("Step 2: 清洗数据 (DWD)")
    dwd_df = cleaner.clean(ods_df)
    local_storage.save_csv(dwd_df, 'dwd', 'product_price_clean', date)
    if oss_client:
        oss_client.upload_csv(dwd_df, 'dwd', 'product_price_clean', date)
    
    logger.info("Step 3: 汇总数据 (DWS)")
    sku_daily = aggregator.aggregate_sku_daily(dwd_df)
    category_daily = aggregator.aggregate_category_daily(sku_daily)
    overall_daily = aggregator.aggregate_overall_daily(sku_daily)
    
    local_storage.save_csv(sku_daily, 'dws', 'sku_daily_summary', date)
    local_storage.save_csv(category_daily, 'dws', 'category_daily_summary', date)
    local_storage.save_csv(overall_daily, 'dws', 'overall_daily_summary', date)
    
    if oss_client:
        oss_client.upload_csv(sku_daily, 'dws', 'sku_daily_summary', date)
        oss_client.upload_csv(category_daily, 'dws', 'category_daily_summary', date)
        oss_client.upload_csv(overall_daily, 'dws', 'overall_daily_summary', date)
    
    logger.info(f"完成处理日期: {date}")

def compute_index_and_generate_reports(dates, config, local_storage, oss_client=None):
    """计算指数并生成报告"""
    logger.info("Step 4: 计算价格指数 (ADS)")
    
    sku_daily_list = []
    category_daily_list = []
    overall_daily_list = []
    
    for date in dates:
        sku_daily = local_storage.read_csv('dws', 'sku_daily_summary', date)
        category_daily = local_storage.read_csv('dws', 'category_daily_summary', date)
        overall_daily = local_storage.read_csv('dws', 'overall_daily_summary', date)
        
        sku_daily_list.append(sku_daily)
        category_daily_list.append(category_daily)
        overall_daily_list.append(overall_daily)
    
    all_sku_daily = pd.concat(sku_daily_list, ignore_index=True)
    all_category_daily = pd.concat(category_daily_list, ignore_index=True)
    all_overall_daily = pd.concat(overall_daily_list, ignore_index=True)
    
    base_date = config['base_date']
    calculator = IndexCalculator(base_date)
    
    sku_index = calculator.compute_sku_index(all_sku_daily)
    category_index = calculator.compute_category_index(sku_index)
    overall_index = calculator.compute_overall_index(category_index, all_category_daily)
    top_movers = calculator.get_top_movers(sku_index)
    
    logger.info("Step 5: 生成 DataV 报告 (ADS)")
    report_gen = ReportGenerator()
    
    overall_index_report = report_gen.generate_overall_index_report(overall_index)
    category_index_report = report_gen.generate_category_index_report(category_index)
    sku_index_report = report_gen.generate_sku_index_report(sku_index)
    top_movers_report = report_gen.generate_top_movers_report(top_movers)
    daily_report = report_gen.generate_daily_report(all_overall_daily)
    
    local_storage.save_json(overall_index_report, 'ads', 'overall_index.json')
    local_storage.save_json(category_index_report, 'ads', 'category_index.json')
    local_storage.save_json(sku_index_report, 'ads', 'sku_index.json')
    local_storage.save_json(top_movers_report, 'ads', 'top_movers.json')
    local_storage.save_json(daily_report, 'ads', 'daily_report.json')
    
    if oss_client:
        oss_client.upload_json(overall_index_report, 'ads', 'overall_index.json')
        oss_client.upload_json(category_index_report, 'ads', 'category_index.json')
        oss_client.upload_json(sku_index_report, 'ads', 'sku_index.json')
        oss_client.upload_json(top_movers_report, 'ads', 'top_movers.json')
        oss_client.upload_json(daily_report, 'ads', 'daily_report.json')
    
    logger.info("所有报告生成完成")

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("云价格指数计算平台 - Cloud Price Index Platform")
    logger.info("=" * 80)
    
    config = load_config()
    args = parse_args()
    
    if args.date:
        dates = [args.date]
    elif args.start_date and args.end_date:
        dates = get_date_range(args.start_date, args.end_date)
    else:
        dates = get_date_range(config['start_date'], config['end_date'])
    
    logger.info(f"处理日期范围: {dates[0]} 到 {dates[-1]} ({len(dates)} 天)")
    
    local_storage, oss_client = get_storage_clients(config)
    data_generator = MockDataGenerator(config)
    cleaner = DataCleaner()
    aggregator = DataAggregator()
    
    for date in dates:
        process_date(date, config, data_generator, cleaner, aggregator, local_storage, oss_client)
    
    compute_index_and_generate_reports(dates, config, local_storage, oss_client)
    
    logger.info("=" * 80)
    logger.info("所有数据处理完成！")
    logger.info(f"本地数据目录: data/")
    if oss_client:
        logger.info(f"OSS 数据已上传")
    logger.info("=" * 80)

if __name__ == '__main__':
    main()
