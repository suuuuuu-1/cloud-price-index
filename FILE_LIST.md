# Cloud Price Index - 项目文件清单

## 📋 项目文件列表（共 29 个文件）

### 根目录文件（9 个）
1. `README.md` - 项目完整说明文档
2. `QUICKSTART.md` - 快速开始指南
3. `INSTALL.md` - 安装说明文档
4. `PROJECT_SUMMARY.md` - 项目完成总结
5. `requirements.txt` - Python 依赖包列表
6. `.env.example` - 环境变量配置示例
7. `.gitignore` - Git 忽略规则
8. `check_project.py` - 项目结构验证脚本

### 配置文件（1 个）
9. `config/config.yaml` - 项目配置文件

### 源代码 - 主程序（2 个）
10. `src/__init__.py` - 模块初始化
11. `src/main.py` - 主程序入口 ⭐

### 源代码 - 数据采集模块（2 个）
12. `src/ingestion/__init__.py` - 模块初始化
13. `src/ingestion/generate_mock_data.py` - 模拟数据生成器 ⭐

### 源代码 - 数据计算模块（4 个）
14. `src/compute/__init__.py` - 模块初始化
15. `src/compute/clean_data.py` - 数据清洗器 ⭐
16. `src/compute/aggregate_data.py` - 数据汇总器 ⭐
17. `src/compute/compute_index.py` - 价格指数计算器 ⭐

### 源代码 - 存储模块（3 个）
18. `src/storage/__init__.py` - 模块初始化
19. `src/storage/local_storage.py` - 本地存储管理器 ⭐
20. `src/storage/oss_client.py` - 阿里云 OSS 客户端 ⭐

### 源代码 - 报告模块（2 个）
21. `src/report/__init__.py` - 模块初始化
22. `src/report/generate_report.py` - DataV 报告生成器 ⭐

### 源代码 - 工具模块（3 个）
23. `src/utils/__init__.py` - 模块初始化
24. `src/utils/logger.py` - 日志工具
25. `src/utils/dates.py` - 日期工具

### SQL 脚本（1 个）
26. `sql/clickhouse_schema.sql` - ClickHouse 建表语句

### 测试文件（2 个）
27. `tests/__init__.py` - 模块初始化
28. `tests/test_compute_index.py` - 价格指数计算单元测试

---

## 📊 代码统计

| 类别 | 文件数 | 说明 |
|------|--------|------|
| 文档 | 4 | README、快速开始、安装说明、项目总结 |
| 配置 | 3 | YAML 配置、环境变量、Git 忽略 |
| 源代码 | 17 | 核心业务代码 |
| SQL | 1 | ClickHouse 建表语句 |
| 测试 | 2 | 单元测试 |
| 工具 | 2 | 验证脚本、依赖列表 |
| **总计** | **29** | - |

核心代码文件（标注 ⭐）：8 个

---

## 🎯 核心模块说明

### 1. 数据生成模块
**文件**：`src/ingestion/generate_mock_data.py`  
**功能**：
- 生成 2000 个 SKU 主数据
- 模拟多平台、多店铺报价
- 实现价格波动和促销逻辑
- 注入 2% 脏数据

### 2. 数据清洗模块
**文件**：`src/compute/clean_data.py`  
**功能**：
- 删除异常价格和销量
- 删除空值记录
- 识别价格异常暴涨
- 去除重复报价

### 3. 数据汇总模块
**文件**：`src/compute/aggregate_data.py`  
**功能**：
- SKU 日汇总
- 类目日汇总
- 全网日汇总

### 4. 指数计算模块
**文件**：`src/compute/compute_index.py`  
**功能**：
- SKU 价格指数计算
- 类目价格指数（加权平均）
- 全网价格指数（加权平均）
- 环比涨跌幅计算

### 5. 存储模块
**文件**：`src/storage/local_storage.py` + `src/storage/oss_client.py`  
**功能**：
- 本地 CSV/JSON 存储
- 阿里云 OSS 上传下载
- 分区存储管理

### 6. 报告生成模块
**文件**：`src/report/generate_report.py`  
**功能**：
- 生成 5 种 JSON 报告
- 数据格式优化（适配 DataV）

### 7. 主程序
**文件**：`src/main.py`  
**功能**：
- 命令行参数解析
- 流程编排
- 日志记录

---

## 🚀 运行流程

```
main.py
  ↓
1. generate_mock_data.py → ODS 层数据
  ↓
2. clean_data.py → DWD 层数据
  ↓
3. aggregate_data.py → DWS 层数据
  ↓
4. compute_index.py → 计算指数
  ↓
5. generate_report.py → ADS 层 JSON
  ↓
6. local_storage.py / oss_client.py → 保存数据
```

---

## 📦 运行时生成的目录结构

运行后会自动创建以下目录：

```
data/
├── ods/
│   └── product_price_raw/
│       ├── dt=2026-06-01/
│       ├── dt=2026-06-02/
│       └── ...
├── dwd/
│   └── product_price_clean/
│       ├── dt=2026-06-01/
│       └── ...
├── dws/
│   ├── sku_daily_summary/
│   ├── category_daily_summary/
│   └── overall_daily_summary/
└── ads/
    ├── overall_index.json
    ├── category_index.json
    ├── sku_index.json
    ├── top_movers.json
    └── daily_report.json

logs/
└── 20260625.log
```

---

## ✅ 项目验证

运行验证脚本：
```bash
python check_project.py
```

预期输出：
```
✓ 所有文件和目录检查通过！
```

---

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| `README.md` | 完整项目说明，包括架构、数据分层、运行方式 |
| `QUICKSTART.md` | 快速开始，5 步运行项目 |
| `INSTALL.md` | 详细安装说明，解决常见问题 |
| `PROJECT_SUMMARY.md` | 项目完成总结，功能清单 |
| `FILE_LIST.md` | 文件清单（本文档） |

---

## 🔧 核心依赖

```
pandas>=2.0.0          # 数据处理核心
python-dotenv>=1.0.0   # 环境变量管理
PyYAML>=6.0            # 配置文件解析
oss2>=2.18.0           # 阿里云 OSS SDK
```

---

## 🎓 课程报告参考结构

1. **项目背景**（500 字）
   - 电商价格监控的意义
   - 价格指数的应用场景

2. **需求分析**（800 字）
   - 功能需求
   - 非功能需求
   - 技术选型

3. **系统设计**（1500 字）
   - 架构设计（数仓分层）
   - 模块设计
   - 数据流设计

4. **核心算法**（1000 字）
   - 价格指数计算方法
   - 加权平均算法
   - 环比计算方法

5. **实现细节**（1500 字）
   - 数据生成
   - 数据清洗
   - 数据汇总
   - 指数计算

6. **测试与部署**（500 字）
   - 单元测试
   - 运行验证
   - 部署方案

7. **总结与展望**（500 字）
   - 项目成果
   - 不足与改进
   - 未来扩展

**建议总字数**：6000-8000 字

---

## 💡 提示

- ⭐ 标记的文件是核心业务代码
- 所有 Python 文件都有详细的中文注释
- 配置文件采用 YAML 格式，易于修改
- 支持本地和云端双模式运行
- 数据分层清晰，便于理解和扩展

---

**项目创建完成，祝课程设计顺利！** 🎉
