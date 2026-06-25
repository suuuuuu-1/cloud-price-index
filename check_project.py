"""
项目结构验证脚本
验证所有必要的文件和目录是否存在
"""
import os
import sys

def check_file(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} - 文件不存在")
        return False

def check_dir(dirpath, description):
    """检查目录是否存在"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description}: {dirpath} - 目录不存在")
        return False

def main():
    """主函数"""
    print("=" * 80)
    print("Cloud Price Index - 项目结构验证")
    print("=" * 80)
    print()

    all_ok = True

    # 检查根目录文件
    print("检查根目录文件...")
    all_ok &= check_file("README.md", "项目说明")
    all_ok &= check_file("INSTALL.md", "安装说明")
    all_ok &= check_file("requirements.txt", "依赖列表")
    all_ok &= check_file(".env.example", "环境变量示例")
    all_ok &= check_file(".gitignore", "Git 忽略文件")
    print()

    # 检查配置文件
    print("检查配置文件...")
    all_ok &= check_dir("config", "配置目录")
    all_ok &= check_file("config/config.yaml", "项目配置")
    print()

    # 检查源代码
    print("检查源代码...")
    all_ok &= check_dir("src", "源代码目录")
    all_ok &= check_file("src/main.py", "主程序")
    all_ok &= check_file("src/ingestion/generate_mock_data.py", "数据生成模块")
    all_ok &= check_file("src/compute/clean_data.py", "数据清洗模块")
    all_ok &= check_file("src/compute/aggregate_data.py", "数据汇总模块")
    all_ok &= check_file("src/compute/compute_index.py", "指数计算模块")
    all_ok &= check_file("src/storage/local_storage.py", "本地存储模块")
    all_ok &= check_file("src/storage/oss_client.py", "OSS 客户端模块")
    all_ok &= check_file("src/report/generate_report.py", "报告生成模块")
    all_ok &= check_file("src/utils/logger.py", "日志工具")
    all_ok &= check_file("src/utils/dates.py", "日期工具")
    print()

    # 检查 SQL 文件
    print("检查 SQL 文件...")
    all_ok &= check_dir("sql", "SQL 目录")
    all_ok &= check_file("sql/clickhouse_schema.sql", "ClickHouse 建表语句")
    print()

    # 检查测试文件
    print("检查测试文件...")
    all_ok &= check_dir("tests", "测试目录")
    all_ok &= check_file("tests/test_compute_index.py", "指数计算测试")
    print()

    # 总结
    print("=" * 80)
    if all_ok:
        print("✓ 所有文件和目录检查通过！")
        print()
        print("下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 复制配置: cp .env.example .env")
        print("3. 运行程序: python -m src.main --start-date 2026-06-01 --end-date 2026-06-30")
        return 0
    else:
        print("✗ 部分文件或目录缺失，请检查项目结构")
        return 1

if __name__ == "__main__":
    sys.exit(main())
