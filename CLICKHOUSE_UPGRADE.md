# ClickHouse 升级指南

## 📦 方案对比

| 特性 | CSV 方案（当前） | ClickHouse 方案 |
|------|-----------------|----------------|
| 数据存储 | CSV 文件 | 列式数据库 |
| 查询速度 | 慢（秒级） | 快（毫秒级） |
| 数据量 | < 10GB | TB 级 |
| 部署难度 | ✅ 简单 | ⚠️ 需要服务器 |
| 成本 | 低 | 中等 |

## 🚀 升级步骤

### 第 1 步：安装 ClickHouse

#### 方式 1：Docker（推荐）
```bash
# 启动 ClickHouse 服务器
docker run -d \
  --name clickhouse \
  -p 8123:8123 -p 9000:9000 \
  --ulimit nofile=262144:262144 \
  clickhouse/clickhouse-server

# 验证
curl http://localhost:8123
```

#### 方式 2：本地安装（Windows）
```bash
# 下载
https://clickhouse.com/docs/en/install

# 或使用 WSL
wsl --install
# 然后在 WSL 中安装 ClickHouse
```

#### 方式 3：阿里云 ClickHouse（生产环境）
- 访问阿里云控制台
- 云数据库 ClickHouse
- 创建实例（按量付费约 0.5 元/小时）

### 第 2 步：安装 Python 客户端

```bash
pip install clickhouse-connect
```

### 第 3 步：配置连接

编辑 `.env`：
```bash
# ClickHouse 配置
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
```

如果使用阿里云：
```bash
CLICKHOUSE_HOST=your-instance.clickhouse.aliyuncs.com
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=your-user
CLICKHOUSE_PASSWORD=your-password
```

### 第 4 步：创建表结构

```bash
python -c "from import_to_clickhouse import get_clickhouse_client, create_tables; create_tables(get_clickhouse_client())"
```

或手动执行：
```bash
# Docker 方式
docker exec -it clickhouse clickhouse-client

# 然后复制 sql/clickhouse_schema.sql 内容执行
```

### 第 5 步：导入数据

```bash
# 导入前 30 天数据（测试）
python import_to_clickhouse.py

# 导入全部数据（修改脚本中的日期范围）
```

导入时间估算：
- 30 天数据：约 1-2 分钟
- 1 年数据：约 10-20 分钟
- 3 年数据：约 30-60 分钟

### 第 6 步：查询数据

```bash
# 使用 ClickHouse 计算价格指数
python query_clickhouse.py
```

## 📊 性能对比

### CSV 方案
```bash
python process_simple.py --start-date 2025-05-17 --end-date 2025-06-15
# 耗时：约 10-30 秒
```

### ClickHouse 方案
```bash
python query_clickhouse.py
# 耗时：约 1-3 秒
```

**速度提升：5-10 倍**

## 🎯 使用场景

### 继续用 CSV（推荐课程设计）
- ✅ 数据量 < 10GB
- ✅ 处理频率低（每天几次）
- ✅ 无需部署服务器
- ✅ 成本最低

### 升级 ClickHouse（生产环境）
- ✅ 数据量 > 10GB
- ✅ 需要实时查询
- ✅ 复杂聚合分析
- ✅ 多用户并发

## 💡 两者结合方案

可以同时支持两种方式：

```python
# 根据配置选择
if os.getenv('USE_CLICKHOUSE') == 'true':
    from query_clickhouse import compute_index_from_clickhouse
    result = compute_index_from_clickhouse(...)
else:
    from process_simple import main
    result = main()
```

## 🔧 ClickHouse 常用操作

### 查询数据量
```sql
SELECT
    count() as total_rows,
    formatReadableSize(sum(data_compressed_bytes)) as compressed_size
FROM system.parts
WHERE table = 'raw_product_price_detail';
```

### 查询每日统计
```sql
SELECT
    date,
    count() as price_count,
    avg(price) as avg_price
FROM raw_product_price_detail
WHERE date BETWEEN '2025-05-17' AND '2025-06-15'
GROUP BY date
ORDER BY date;
```

### 查询类目分布
```sql
SELECT
    c.category_name,
    count(DISTINCT p.product_id) as product_count,
    avg(r.price) as avg_price
FROM raw_product_price_detail r
JOIN dim_product p ON r.product_id = p.product_id
JOIN dim_category c ON p.category_id = c.category_id
WHERE r.date = '2025-05-17'
GROUP BY c.category_name
ORDER BY product_count DESC
LIMIT 10;
```

## 📝 建议

### 课程设计阶段
**继续用 CSV 方案**，理由：
- ✅ 简单，专注于业务逻辑
- ✅ 无需额外部署
- ✅ 性能足够

在报告中提及：
> "当前使用 CSV + pandas 处理数据，满足课程需求。预留了 ClickHouse 扩展方案，当数据量达到 TB 级时可平滑升级，查询性能可提升 10-100 倍。"

### 未来生产环境
考虑升级 ClickHouse，获得：
- 更快的查询速度
- 更强的并发能力
- 更好的扩展性

## ⚠️ 注意事项

1. **ClickHouse 不支持事务**
2. **删除/更新性能差**（设计时避免频繁更新）
3. **需要规划分区策略**（按月分区）
4. **内存占用较高**（建议 8GB+ RAM）

---

**当前建议**：继续用 CSV 方案完成课程设计，将 ClickHouse 作为技术展望部分写入报告。
