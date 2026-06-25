# 使用真实数据的快速指南

## 📦 真实数据说明

老师提供的数据包含：
- **categories.csv** - 商品类目（约 300+ 个类目，多层级）
- **products.csv** - 商品主数据（约 40,000 个商品）
- **daily_price/** - 每日价格数据（2025-05-17 到 2028-05-15，共 1095 天）

## 🚀 快速开始（无需安装依赖即可查看数据）

### 查看数据统计

```bash
# 查看有多少类目
python -c "import pandas as pd; df=pd.read_csv('data/categories.csv', encoding='gbk'); print(f'类目数: {len(df)}')"

# 查看有多少商品
python -c "import pandas as pd; df=pd.read_csv('data/products.csv', encoding='gbk'); print(f'商品数: {len(df)}')"

# 查看某天的价格数据
python -c "import pandas as pd; df=pd.read_csv('data/daily_price/daily_prices_20250517.csv', encoding='gbk'); print(f'当日价格数: {len(df)}'); print(df.head())"
```

## 📊 处理真实数据

已为你创建专门的处理脚本：**process_real_data.py**

### 运行方式

```bash
# 处理 30 天数据（2025-05-17 到 2025-06-15）
python process_real_data.py --start-date 2025-05-17 --end-date 2025-06-15 --base-date 2025-05-17

# 处理更长时间（比如 3 个月）
python process_real_data.py --start-date 2025-05-17 --end-date 2025-08-15 --base-date 2025-05-17

# 处理整年数据
python process_real_data.py --start-date 2025-05-17 --end-date 2026-05-16 --base-date 2025-05-17
```

### 输出结果

运行后会在 `output/` 目录生成：
- **overall_index.csv** - 全网价格指数（CSV 格式）
- **overall_index.json** - 全网价格指数（JSON 格式，供 DataV 使用）

示例输出：
```csv
date,overall_index,product_count,category_count,change_pct
2025-05-17,100.0,40000,300,0.0
2025-05-18,100.5,40000,300,0.5
2025-05-19,99.8,40000,300,-0.7
```

## 🔧 如果需要安装依赖

```bash
pip install pandas -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

**注意**：只需要 pandas，不需要其他依赖包（dotenv, yaml, oss2 都不需要）

## 📈 数据说明

### categories.csv 字段
- `category` - 类目名称（中文）
- `category_id` - 类目 ID
- `hierarchy` - 层级（1=一级类目，2=二级类目，3=三级类目）
- `weight` - 权重（用于计算加权指数）
- `price` - 类目价格（null）
- `parent` - 父类目 ID

### products.csv 字段
- `product_id` - 商品 ID
- `category_id` - 所属类目 ID
- `name` - 商品名称
- `weight` - 商品权重
- `price` - 基期价格
- `change_count` - 价格变动次数

### daily_prices_YYYYMMDD.csv 字段
- `product_id` - 商品 ID
- `category_id` - 类目 ID
- `name` - 商品名称
- `price` - 当日价格
- `change_date` - 日期

## 🎓 课程报告建议

使用真实数据的优势：
1. **数据规模大** - 40,000 个商品，1095 天数据
2. **真实业务场景** - 多层级类目，真实价格波动
3. **可做深入分析** - 长期趋势、季节性、类目对比

报告可包含：
- 全网价格指数变化趋势（1-3 年）
- 各类目价格指数对比
- 价格波动分析
- 季节性特征分析

## ⚠️ 注意事项

1. **文件编码**: 所有 CSV 文件都是 GBK 编码
2. **数据量**: 处理全部 1095 天数据需要较长时间（约 10-30 分钟）
3. **建议**: 先处理 30 天数据测试，确认无误后再处理更长时间

## 📊 快速统计

```bash
# 查看数据日期范围
ls data/daily_price/ | head -1  # 第一天
ls data/daily_price/ | tail -1  # 最后一天

# 统计文件数
ls data/daily_price/*.csv | wc -l  # 总天数
```
