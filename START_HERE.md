# 立即开始 - 3 步运行项目

## ✅ 项目状态
- 所有文件已创建完成（30 个文件）
- 代码已通过结构验证
- 文档完整齐全

## 🚀 立即开始（仅需 3 步）

### 第 1 步：安装依赖（2 分钟）

打开命令行，运行：

```bash
pip install pandas python-dotenv PyYAML oss2 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

或者：

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

> 💡 如果网络问题，可尝试其他镜像：
> - 豆瓣：`https://pypi.douban.com/simple/`
> - 腾讯云：`https://mirrors.cloud.tencent.com/pypi/simple/`

### 第 2 步：创建配置文件（10 秒）

```bash
# Windows 用户
copy .env.example .env

# Linux/Mac 用户
cp .env.example .env
```

> 💡 保持默认配置即可（OSS_ENABLED=false，只使用本地存储）

### 第 3 步：运行项目（3 分钟）

```bash
python -m src.main --start-date 2026-06-01 --end-date 2026-06-30
```

完成！数据会自动保存到 `data/` 目录。

---

## 📁 运行后的目录结构

```
data/
├── ods/                          # 原始数据
│   └── product_price_raw/
│       ├── dt=2026-06-01/
│       │   └── product_price_raw.csv
│       ├── dt=2026-06-02/
│       └── ...（共 30 天）
├── dwd/                          # 清洗后数据
│   └── product_price_clean/
│       └── dt=2026-06-01/
│           └── product_price_clean.csv
├── dws/                          # 汇总数据
│   ├── sku_daily_summary/
│   ├── category_daily_summary/
│   └── overall_daily_summary/
└── ads/                          # 可视化数据
    ├── overall_index.json       ⭐ DataV 使用
    ├── category_index.json      ⭐ DataV 使用
    ├── sku_index.json          ⭐ DataV 使用
    ├── top_movers.json         ⭐ DataV 使用
    └── daily_report.json       ⭐ DataV 使用
```

---

## 🎯 快速验证

### 验证 1：检查项目结构
```bash
python check_project.py
```
预期：✓ 所有文件和目录检查通过！

### 验证 2：检查环境
```bash
python check_env.py
```
预期：✓ 环境检查通过！

### 验证 3：查看生成的数据
运行完成后，打开 `data/ads/overall_index.json` 查看全网价格指数。

---

## 📊 预期结果

### 数据量
- **ODS 层**: 约 10-20 万行原始数据
- **DWD 层**: 约 9-19 万行清洗后数据
- **DWS 层**: 约 6 万行汇总数据
- **ADS 层**: 5 个 JSON 文件

### 运行时间
- 第一次运行：约 3-5 分钟
- 单日数据：约 5-10 秒

### 生成的 JSON 示例

**overall_index.json** - 全网价格指数
```json
[
  {
    "date": "2026-06-01",
    "index": 100.0,
    "change_pct": 0.0
  },
  {
    "date": "2026-06-02",
    "index": 101.2,
    "change_pct": 1.2
  }
]
```

**category_index.json** - 类目价格指数
```json
[
  {
    "date": "2026-06-01",
    "category": "手机数码",
    "index": 100.0,
    "change_pct": 0.0
  }
]
```

---

## 🔧 其他运行方式

### 只生成某一天
```bash
python -m src.main --date 2026-06-15
```

### 使用配置文件的默认日期
```bash
python -m src.main
```

### 自定义日期范围
```bash
python -m src.main --start-date 2026-06-10 --end-date 2026-06-20
```

---

## ⚙️ 高级配置

### 修改数据规模

编辑 `config/config.yaml`：

```yaml
# 修改 SKU 数量（默认 2000）
sku_count: 5000

# 修改脏数据比例（默认 2%）
dirty_data_rate: 0.05
```

### 启用阿里云 OSS

编辑 `.env` 文件：

```env
OSS_ENABLED=true
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
ALIYUN_OSS_BUCKET=你的bucket名称
ALIYUN_ACCESS_KEY_ID=你的AccessKey
ALIYUN_ACCESS_KEY_SECRET=你的Secret
```

---

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| **START_HERE.md** | 本文档，3 步快速开始 |
| **README.md** | 完整项目说明 |
| **QUICKSTART.md** | 5 步详细指南 |
| **INSTALL.md** | 详细安装说明 |
| **FULL_CHECK_REPORT.md** | 全面检查报告 |

---

## ❓ 常见问题

### Q: pip 安装失败？
A: 使用国内镜像源：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

### Q: 提示 ModuleNotFoundError？
A: 依赖包未安装，重新执行第 1 步

### Q: 如何查看日志？
A: 查看 `logs/` 目录下的日志文件

### Q: 数据在哪里？
A: 本地数据在 `data/` 目录

### Q: 如何修改 SKU 数量？
A: 编辑 `config/config.yaml`，修改 `sku_count`

---

## 🎓 课程报告提示

运行完成后，可以：

1. **截图展示**：
   - 项目目录结构
   - 运行日志
   - 生成的数据文件
   - JSON 数据内容

2. **数据分析**：
   - ODS 到 DWD 的清洗效果（对比数据量）
   - 各类目的价格指数趋势
   - 促销日的价格和销量变化

3. **技术说明**：
   - 数据仓库分层架构
   - 价格指数计算算法
   - 数据清洗策略

---

## 🎉 完成后

恭喜！你已经成功运行了一个完整的**电商价格指数计算平台**。

**接下来可以：**
1. ✅ 查看生成的数据和报告
2. ✅ 对接 DataV 进行可视化（可选）
3. ✅ 编写课程设计报告
4. ✅ 展示和答辩

---

**祝课程设计顺利完成！** 🎓✨
