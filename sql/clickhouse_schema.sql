-- ClickHouse 扩展方案建表语句
-- 用于将数据导入 ClickHouse 进行高性能查询分析

-- 1. 原始价格明细表 (ODS 层)
CREATE TABLE IF NOT EXISTS raw_product_price_detail
(
    date Date COMMENT '日期',
    sku_id String COMMENT 'SKU ID',
    product_id String COMMENT '商品 ID',
    product_name String COMMENT '商品名称',
    category_l1 String COMMENT '一级类目',
    category_l2 String COMMENT '二级类目',
    brand String COMMENT '品牌',
    platform String COMMENT '平台',
    shop_id String COMMENT '店铺 ID',
    price Decimal(10, 2) COMMENT '价格',
    sales Int32 COMMENT '销量',
    is_promo UInt8 COMMENT '是否促销',
    collect_time DateTime COMMENT '采集时间'
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, sku_id, platform, shop_id)
SETTINGS index_granularity = 8192
COMMENT '原始商品价格明细表';

-- 2. SKU 日汇总表 (DWS 层)
CREATE TABLE IF NOT EXISTS dws_sku_daily_summary
(
    date Date COMMENT '日期',
    sku_id String COMMENT 'SKU ID',
    product_name String COMMENT '商品名称',
    category_l1 String COMMENT '一级类目',
    category_l2 String COMMENT '二级类目',
    brand String COMMENT '品牌',
    avg_price Decimal(10, 2) COMMENT '平均价格',
    total_sales Int64 COMMENT '总销量',
    platform_count UInt32 COMMENT '平台数',
    shop_count UInt32 COMMENT '店铺数'
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, sku_id)
SETTINGS index_granularity = 8192
COMMENT 'SKU 日汇总表';

-- 3. 类目日汇总表 (DWS 层)
CREATE TABLE IF NOT EXISTS dws_category_daily_summary
(
    date Date COMMENT '日期',
    category String COMMENT '类目',
    avg_price Decimal(10, 2) COMMENT '平均价格',
    total_sales Int64 COMMENT '总销量',
    sku_count UInt32 COMMENT 'SKU 数量'
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, category)
SETTINGS index_granularity = 8192
COMMENT '类目日汇总表';

-- 4. 价格指数日报表 (ADS 层)
CREATE TABLE IF NOT EXISTS ads_price_index_daily
(
    date Date COMMENT '日期',
    index_type String COMMENT '指数类型（overall/category/sku）',
    dimension_value String COMMENT '维度值（类目名或SKU ID）',
    index_value Decimal(10, 2) COMMENT '指数值',
    change_pct Decimal(10, 2) COMMENT '环比涨跌幅（%）'
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, index_type, dimension_value)
SETTINGS index_granularity = 8192
COMMENT '价格指数日报表';

-- 示例查询

-- 查询某日全网价格指数
SELECT
    date,
    index_value,
    change_pct
FROM ads_price_index_daily
WHERE index_type = 'overall'
  AND date >= '2026-06-01'
ORDER BY date;

-- 查询各类目价格指数趋势
SELECT
    date,
    dimension_value AS category,
    index_value,
    change_pct
FROM ads_price_index_daily
WHERE index_type = 'category'
  AND date >= '2026-06-01'
ORDER BY date, category;

-- 查询 TOP 涨幅类目
SELECT
    dimension_value AS category,
    index_value,
    change_pct
FROM ads_price_index_daily
WHERE index_type = 'category'
  AND date = today()
ORDER BY change_pct DESC
LIMIT 10;

-- 查询某类目的 SKU 明细
SELECT
    date,
    sku_id,
    product_name,
    avg_price,
    total_sales
FROM dws_sku_daily_summary
WHERE category_l1 = '手机数码'
  AND date = today()
ORDER BY total_sales DESC
LIMIT 20;
