# 🚀 GitHub Actions + OSS 配置完成

## ✅ 已完成

1. **代码已推送到 GitHub**
   - 仓库: https://github.com/suuuuuu-1/cloud-price-index

2. **GitHub Actions 已配置**
   - ✅ 自动测试（Python 3.10/3.11/3.12）
   - ✅ 数据处理工作流（从 OSS 拉取 → 处理 → 生成报告）

3. **OSS 数据管理已就绪**
   - ✅ `upload_data.py` - 上传数据到 OSS
   - ✅ `download_data.py` - 从 OSS 下载数据
   - ✅ OSS_GUIDE.md - 完整使用文档

## 📝 下一步操作

### 第 1 步：上传数据到 OSS

```bash
# 1. 编辑 .env 文件，填入你的 OSS 信息
OSS_ENABLED=true
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com  # 改成你的区域
ALIYUN_OSS_BUCKET=your-bucket-name               # 改成你的 bucket
ALIYUN_ACCESS_KEY_ID=your-key-id                 # 改成你的 key
ALIYUN_ACCESS_KEY_SECRET=your-key-secret         # 改成你的 secret

# 2. 安装 oss2
pip install oss2

# 3. 上传数据（会上传整个 data 目录，约 1.5GB）
python upload_data.py
```

### 第 2 步：配置 GitHub Secrets

1. 访问: https://github.com/suuuuuu-1/cloud-price-index/settings/secrets/actions

2. 点击 "New repository secret"，依次添加：

   | Name | Value |
   |------|-------|
   | `ALIYUN_OSS_ENDPOINT` | `oss-cn-hangzhou.aliyuncs.com` |
   | `ALIYUN_OSS_BUCKET` | 你的 bucket 名称 |
   | `ALIYUN_ACCESS_KEY_ID` | 你的 AccessKey ID |
   | `ALIYUN_ACCESS_KEY_SECRET` | 你的 AccessKey Secret |

### 第 3 步：测试 GitHub Actions

1. **查看自动测试**
   - 访问: https://github.com/suuuuuu-1/cloud-price-index/actions
   - 应该能看到 "Tests" 工作流正在运行或已完成

2. **手动触发数据处理**（配置 Secrets 后）
   - Actions → "Process Data from OSS" → "Run workflow"
   - 会自动从 OSS 下载数据并处理

## 🎯 工作流说明

### Tests (自动触发)
- **触发时机**: 每次 push 或 PR
- **功能**: 运行单元测试，检查代码结构
- **Python 版本**: 3.10, 3.11, 3.12

### Process Data from OSS (手动/定时)
- **触发时机**: 手动触发 或 每天凌晨 2 点
- **功能**: 
  1. 从 OSS 下载数据
  2. 处理数据（计算价格指数）
  3. 上传结果到 Artifacts
- **结果下载**: Actions → 选择运行 → Artifacts → price-index-results

## 📊 数据流程

```
本地 data/
    ↓ (python upload_data.py)
阿里云 OSS
    ↓ (GitHub Actions 自动)
处理数据 → 生成报告
    ↓
GitHub Artifacts (可下载)
```

## 💡 使用场景

### 场景 1: 团队协作
```bash
# 新成员加入
git clone https://github.com/suuuuuu-1/cloud-price-index.git
python download_data.py  # 从 OSS 下载数据
python process_simple.py # 处理数据
```

### 场景 2: 自动化报告
- 配置好 GitHub Secrets
- 每天自动处理数据
- 从 Artifacts 下载最新报告

### 场景 3: 本地开发
```bash
# 使用本地数据（不需要 OSS）
python process_simple.py --start-date 2025-05-17 --end-date 2025-06-15
```

## ⚠️ 注意事项

1. **首次上传数据需要时间**（约 1.5GB，取决于网速）
2. **OSS 费用**：约 0.2-5 元/月（存储+流量）
3. **GitHub Actions 免费额度**：公开仓库无限制，私有仓库 2000 分钟/月
4. **数据隐私**：如果数据敏感，建议使用私有仓库

## 🔧 故障排查

**Q: Actions 中 "Download data from OSS" 失败？**
- 检查 GitHub Secrets 是否配置正确
- 检查 OSS Bucket 是否存在
- 检查 AccessKey 权限

**Q: upload_data.py 上传失败？**
- 检查 .env 文件配置
- 检查网络连接
- 检查 OSS Bucket 权限

**Q: Tests 失败？**
- 正常，因为没有真实数据文件
- 可以在本地运行: `pytest tests/ -v`

## 📚 相关文档

- [OSS_GUIDE.md](OSS_GUIDE.md) - OSS 完整使用指南
- [SUCCESS.md](SUCCESS.md) - 项目运行成功指南
- [README.md](README.md) - 项目总体说明

---

**下一步**：配置你的 OSS 信息，上传数据，然后在 GitHub 配置 Secrets！
