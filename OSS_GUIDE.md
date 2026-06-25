# OSS 数据管理指南

## 📦 概述

本项目支持将 data 数据存储在阿里云 OSS，实现：
- ✅ 数据不占用 Git 仓库空间
- ✅ 团队成员共享数据
- ✅ GitHub Actions 自动从 OSS 拉取数据处理

## 🚀 快速开始

### 1. 上传本地数据到 OSS

```bash
# 1. 配置 .env 文件
OSS_ENABLED=true
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
ALIYUN_OSS_BUCKET=your-bucket-name
ALIYUN_ACCESS_KEY_ID=your-access-key-id
ALIYUN_ACCESS_KEY_SECRET=your-access-key-secret
OSS_PREFIX=cloud-price-index

# 2. 上传数据
python upload_data.py
```

### 2. 从 OSS 下载数据

```bash
# 在新环境中下载数据
python download_data.py
```

### 3. 处理数据

```bash
# 下载后即可处理
python process_simple.py --start-date 2025-05-17 --end-date 2025-06-15
```

## 🔧 GitHub Actions 配置

### 添加 Secrets

在 GitHub 仓库中设置以下 Secrets：

1. 进入仓库 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加以下 4 个 secrets：

| Name | Value | 示例 |
|------|-------|------|
| `ALIYUN_OSS_ENDPOINT` | OSS 端点 | `oss-cn-hangzhou.aliyuncs.com` |
| `ALIYUN_OSS_BUCKET` | Bucket 名称 | `your-bucket-name` |
| `ALIYUN_ACCESS_KEY_ID` | AccessKey ID | `LTAI5t...` |
| `ALIYUN_ACCESS_KEY_SECRET` | AccessKey Secret | `xxx...` |

### 手动触发 Actions

1. 进入仓库 → Actions
2. 选择 "Process Data from OSS"
3. 点击 "Run workflow"

## 📁 OSS 目录结构

```
your-bucket/
└── cloud-price-index/
    └── data/
        ├── categories.csv
        ├── products.csv
        └── daily_price/
            ├── daily_prices_20250517.csv
            ├── daily_prices_20250518.csv
            └── ...
```

## 🔒 安全建议

1. **不要**将 AccessKey 提交到 Git
2. 使用 GitHub Secrets 存储凭证
3. 定期轮换 AccessKey
4. 使用 RAM 账号并授予最小权限

## 📊 数据大小估算

- categories.csv: ~12 KB
- products.csv: ~3.6 MB
- daily_price/ (1095天): ~1.5 GB

总计约 1.5 GB，建议使用 OSS 标准存储。

## 💡 成本估算

阿里云 OSS 标准存储（按量付费）：
- 存储费用: 1.5 GB × 0.12元/GB/月 = 0.18元/月
- 流量费用: 下载 1 次/天 × 30天 = ~5元/月

## ⚡ 常见问题

**Q: 如何加速上传/下载？**
A: 选择就近的 OSS 区域（如 `oss-cn-hangzhou` 对应杭州）

**Q: 团队成员如何访问？**
A: 共享 .env 文件（通过安全渠道），或创建 RAM 子账号

**Q: GitHub Actions 失败？**
A: 检查 Secrets 是否配置正确，查看 Actions 日志

## 📝 工作流

### 初次使用
```bash
# 1. 本地有数据
python upload_data.py

# 2. 在 GitHub 配置 Secrets
# 3. 手动触发 Actions 测试
```

### 日常使用
```bash
# 新成员克隆仓库后
git clone https://github.com/suuuuuu-1/cloud-price-index.git
cd cloud-price-index

# 下载数据
python download_data.py

# 处理数据
python process_simple.py
```

### CI/CD 自动化
- 每天凌晨 2 点自动从 OSS 拉取数据
- 自动处理并生成报告
- 结果上传到 Artifacts
