"""
环境检查脚本
检查 Python 版本和依赖包是否满足项目要求
"""
import sys

def check_python_version():
    """检查 Python 版本"""
    print("=" * 80)
    print("Cloud Price Index - 环境检查")
    print("=" * 80)
    print()

    print(f"当前 Python 版本: {sys.version}")
    print(f"版本号: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()

    if sys.version_info < (3, 6):
        print("❌ Python 版本过低！")
        print("   要求: Python 3.6+")
        print("   建议: Python 3.10+")
        return False
    elif sys.version_info < (3, 10):
        print("⚠️  Python 版本偏低")
        print("   当前: Python {}.{}.{}".format(sys.version_info.major,
                                               sys.version_info.minor,
                                               sys.version_info.micro))
        print("   建议: Python 3.10+")
        print("   说明: 项目可以运行，但建议升级到 Python 3.10+ 以获得更好的性能")
        return True
    else:
        print("✓ Python 版本符合要求")
        return True

def check_dependencies():
    """检查依赖包"""
    print()
    print("检查依赖包...")
    print("-" * 80)

    dependencies = {
        'pandas': 'pandas',
        'dotenv': 'python-dotenv',
        'yaml': 'PyYAML',
        'oss2': 'oss2'
    }

    all_installed = True

    for module_name, package_name in dependencies.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"✗ {package_name} 未安装")
            all_installed = False

    print()

    if not all_installed:
        print("部分依赖包未安装，请运行:")
        print("pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/")
        return False
    else:
        print("✓ 所有依赖包已安装")
        return True

def check_config_files():
    """检查配置文件"""
    import os

    print()
    print("检查配置文件...")
    print("-" * 80)

    if os.path.exists('.env'):
        print("✓ .env 文件存在")
    else:
        print("⚠️  .env 文件不存在")
        print("   请运行: copy .env.example .env  (Windows)")
        print("   或运行: cp .env.example .env  (Linux/Mac)")

    if os.path.exists('config/config.yaml'):
        print("✓ config.yaml 文件存在")
    else:
        print("✗ config.yaml 文件不存在")
        return False

    return True

def main():
    """主函数"""
    py_ok = check_python_version()

    if py_ok:
        deps_ok = check_dependencies()
        config_ok = check_config_files()

        print()
        print("=" * 80)

        if py_ok and deps_ok and config_ok:
            print("✓ 环境检查通过！可以开始运行项目")
            print()
            print("运行命令:")
            print("python -m src.main --start-date 2026-06-01 --end-date 2026-06-30")
            return 0
        else:
            print("⚠️  环境检查发现问题，请先解决上述问题")
            return 1
    else:
        print()
        print("=" * 80)
        print("✗ Python 版本不满足最低要求，请升级 Python")
        return 1

if __name__ == "__main__":
    sys.exit(main())
