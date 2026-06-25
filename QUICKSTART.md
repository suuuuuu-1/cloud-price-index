# Cloud Price Index - 快速开始指南

## 项目已创建成功 ✓

所有文件和目录结构已完整创建。

## 立即开始

### 第 1 步：安装依赖

由于网络环境限制，建议使用国内镜像源：

```bash
# 方案 1：阿里云镜像（推荐）
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 方案 2：豆瓣镜像
pip install -r requirements.txt -i https://pypi.douban.com/simple/ --trusted-host pypi.douban.com

# 方案 3：腾讯云镜像
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/ --trusted-host mirrors.cloud.tencent.com
```

**依赖包说明：**
- `pandas>=2.0.0` - 数据处理核心库
- `python-dotenv>=1.0.0` - 环境变量管理
- `PyYAML>=6.0` - YAML 配置文件解析
- `oss2>=2.18.0` - 阿里云 OSS SDK

### 第 2 步：配置环境

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**本地测试模式**（无需 OSS，默认配置）：
```env
OSS_ENABLED=false
```

**阿里云 OSS 模式**（需要配置）：
```env
OSS_ENABLED=true
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
ALIYUN_OSS_BUCKET=你的bucket名称
ALIYUN_ACCESS_KEY_ID=你的AccessKey
ALIYUN_ACCESS_KEY_SECRET=你的AccessKeySecret
OSS_PREFIX=price-index-platform
```

### 第 3 步：运行程序

```bash
# 运行完整流程（生成 30 天数据）
python -m src.main --start-date 2026-06-01 --end-date 2026-06-30
```

**其他运行方式：**

```bash
# 使用配置文件中的日期
python -m src.main

# 只生成某一天的数据
python -m src.main --date 2026-06-15

# 自定义日期范围
python -m src.main --start-date 2026-06-10 --end-date 2026-06-20
```

### 第 4 步：查看结果

运行完成后，数据会保存在 `data/` 目录下：

```
data/
├── ods/                                    # 原始数据层
│   └── product_price_raw/
│       └── dt=2026-06-01/
│           └── product_price_raw.csv
├── dwd/                                    # 明细数据层
│   └── product_price_clean/
│       └── dt=2026-06-01/
│           └── product_price_clean.csv
├── dws/                                    # 汇总数据层
│   ├── sku_daily_summary/
│   ├── category_daily_summary/
│   └── overall_daily_summary/
└── ads/                                    # 应用数据层（可视化）
    ├── overall_index.json                  # 全网价格指数
    ├── category_index.json                 # 类目价格指数
    ├── sku_index.json                      # SKU 价格指数
    ├── top_movers.json                     # 涨跌幅 TOP
    └── daily_report.json                   # 每日报告
```

### 第 5 步：对接 DataV（可选）

1. **上传到 OSS**（设置 `OSS_ENABLED=true`）
2. **在 DataV 中配置数据源**：
   - 数据源类型：阿里云 OSS
   - 选择对应的 Bucket
   - 读取 `ads/` 目录下的 JSON 文件

3. **JSON 文件说明**：

| 文件 | 用途 | 字段 |
|------|------|------|
| `overall_index.json` | 全网价格指数时间序列 | date, index, change_pct |
| `category_index.json` | 各类目价格指数 | date, category, index, change_pct |
| `sku_index.json` | TOP SKU 价格指数 | date, sku_id, product_name, category, index, change_pct |
| `top_movers.json` | 涨跌幅 TOP 商品 | date, sku_id, product_name, category, index, change_pct |
| `daily_report.json` | 每日汇总报告 | date, avg_price, total_sales, sku_count |

## 配置调整

编辑 `config/config.yaml` 可调整数据生成参数：

```yaml
# 基期日期（用于指数计算）
base_date: "2026-06-01"

# 生成日期范围
start_date: "2026-06-01"
end_date: "2026-06-30"

# SKU 数量（默认 2000）
sku_count: 2000

# 平台列表
platforms:
  - "淘宝"
  - "京东"
  - "拼多多"

# 类目列表
categories:
  - "手机数码"
  - "电脑办公"
  - "家用电器"
  # ... 更多类目

# 脏数据比例（默认 2%）
dirty_data_rate: 0.02
```

## 运行测试

```bash
# 运行单元测试
python -m unittest tests/test_compute_index.py

# 或使用 pytest（需要安装）
python -m pytest tests/
```

## 查看日志

日志文件保存在 `logs/` 目录，按日期命名：
```
logs/20260625.log
```

## ClickHouse 扩展（可选）

如果需要将数据导入 ClickHouse 进行高性能查询：

1. 在 ClickHouse 中执行 `sql/clickhouse_schema.sql` 创建表
2. 使用 `clickhouse-client` 或其他工具导入 CSV 文件
3. 进行高性能 OLAP 分析

示例导入命令：
```bash
clickhouse-client --query="INSERT INTO raw_product_price_detail FORMAT CSV" < data/ods/product_price_raw/dt=2026-06-01/product_price_raw.csv
```

## 数据规模

默认配置下的数据规模：

- **时间跨度**：30 天
- **SKU 数量**：2000 个
- **平台数量**：3 个（淘宝、京东、拼多多）
- **类目数量**：8 个
- **每个 SKU 店铺数**：2-5 个
- **预计数据量**：10-20 万行（ODS 层）

可通过修改 `config/config.yaml` 中的 `sku_count` 调整数据规模。

## 课程报告要点

本项目涵盖以下技术要点，可用于课程设计报告：

1. **数据仓库分层架构**（ODS → DWD → DWS → ADS）
2. **数据清洗技术**（异常值检测、重复数据处理）
3. **价格指数算法**（加权平均法、基期法）
4. **云存储技术**（阿里云 OSS）
5. **数据可视化**（DataV 对接）
6. **ETL 流程设计**
7. **Python 数据处理**（pandas）
8. **配置管理**（YAML、环境变量）

## 常见问题

**Q: 如何修改数据生成数量？**  
A: 编辑 `config/config.yaml`，修改 `sku_count` 参数

**Q: 如何只生成某一天的数据？**  
A: 使用 `python -m src.main --date 2026-06-15`

**Q: 如何不上传到 OSS？**  
A: 在 `.env` 中设置 `OSS_ENABLED=false`

**Q: 数据在哪里查看？**  
A: 本地数据在 `data/` 目录，OSS 数据在对应 Bucket 的 `price-index-platform/` 前缀下

**Q: 如何调整脏数据比例？**  
A: 编辑 `config/config.yaml`，修改 `dirty_data_rate` 参数（0.02 表示 2%）

**Q: 如何添加更多类目？**  
A: 编辑 `config/config.yaml`，在 `categories` 列表中添加

## 技术支持

如有问题，请检查：
1. `logs/` 目录下的日志文件
2. Python 版本是否 >= 3.10
3. 依赖包是否正确安装
4. `.env` 文件配置是否正确

---

**祝你的课程设计顺利完成！** 🎉
