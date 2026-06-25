# 自动部署到服务器

## 🚀 功能

每次 push 到 main 分支，自动更新服务器代码

## 📋 配置步骤

### 第 1 步：服务器初始化

SSH 到服务器：
```bash
ssh my-vps-01
```

在服务器上执行：
```bash
# 克隆仓库
cd /home
git clone https://github.com/suuuuuu-1/cloud-price-index.git
cd cloud-price-index

# 安装依赖
pip install -r requirements.txt

# 配置 .env
nano .env
# 粘贴 OSS 配置

# 下载数据
python download_data.py
```

### 第 2 步：配置 GitHub Secrets

访问：https://github.com/suuuuuu-1/cloud-price-index/settings/secrets/actions

添加 3 个 secrets：

| Name | Value | 说明 |
|------|-------|------|
| `VPS_HOST` | 服务器 IP | 如 `123.45.67.89` |
| `VPS_USER` | SSH 用户名 | 如 `root` 或 `ubuntu` |
| `VPS_SSH_KEY` | SSH 私钥 | 完整的私钥内容 |

### 第 3 步：获取 SSH 私钥

本地执行：
```bash
# 查看私钥
cat ~/.ssh/id_rsa

# 如果没有，生成新的
ssh-keygen -t rsa -b 4096

# 复制私钥（完整内容，包括 BEGIN 和 END）
cat ~/.ssh/id_rsa | clip  # Windows
cat ~/.ssh/id_rsa | pbcopy  # Mac
```

私钥格式：
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
...（很多行）...
-----END OPENSSH PRIVATE KEY-----
```

### 第 4 步：添加公钥到服务器

```bash
# 本地查看公钥
cat ~/.ssh/id_rsa.pub

# 在服务器上执行
ssh my-vps-01
nano ~/.ssh/authorized_keys
# 粘贴公钥，保存
```

## ✅ 测试部署

配置完成后：
```bash
# 本地修改代码
git add .
git commit -m "Test auto deploy"
git push

# GitHub Actions 会自动：
# 1. 连接服务器
# 2. 执行 git pull
# 3. 更新代码
```

查看结果：
- GitHub → Actions → "Deploy to Server"

## 📝 工作流程

```
本地修改代码
    ↓
git push
    ↓
GitHub Actions 触发
    ↓
SSH 连接服务器
    ↓
git pull 更新代码
    ↓
完成！
```

## 🔧 服务器目录结构

```bash
/home/cloud-price-index/
├── data/              # 从 OSS 下载的数据
├── output/            # 处理结果
├── src/               # 源代码（自动更新）
├── .env               # OSS 配置
└── process_simple.py  # 处理脚本
```

## 💡 使用场景

### 手动处理（服务器上）
```bash
ssh my-vps-01
cd /home/cloud-price-index
python process_simple.py --start-date 2025-05-17 --end-date 2025-06-15
```

### 代码更新
- 本地修改 → push → 服务器自动更新
- 无需手动登录服务器 git pull

## ⚠️ 注意事项

1. **SSH Key 不要泄露**
2. **服务器路径**: `/home/cloud-price-index`（可修改 deploy.yml）
3. **首次需要手动 clone**（Actions 只做 git pull）
4. **数据不会自动更新**（需要手动 download_data.py）

## 🎯 可选：添加自动处理

如果需要代码更新后自动处理数据，修改 deploy.yml：
```yaml
script: |
  cd /home/cloud-price-index || exit
  git pull origin main
  python process_simple.py --start-date 2025-05-17 --end-date 2025-06-15
  echo "代码更新并处理完成"
```
