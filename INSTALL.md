# 安装说明

## 依赖安装

由于网络环境问题，如果无法直接使用 pip 安装，可以尝试以下方法：

### 方法 1：使用国内镜像源（推荐）

```bash
# 阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 或使用豆瓣镜像
pip install -r requirements.txt -i https://pypi.douban.com/simple/ --trusted-host pypi.douban.com

# 或使用腾讯云镜像
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/ --trusted-host mirrors.cloud.tencent.com
```

### 方法 2：逐个安装

```bash
pip install pandas
pip install python-dotenv
pip install PyYAML
pip install oss2
```

### 方法 3：配置永久镜像源

Windows 系统：
1. 在用户目录下创建 `pip` 文件夹（如 `C:\Users\用户名\pip\`）
2. 在 `pip` 文件夹中创建 `pip.ini` 文件
3. 添加以下内容：

```ini
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
```

Linux/Mac 系统：
```bash
mkdir ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
EOF
```

然后再执行：
```bash
pip install -r requirements.txt
```

## 环境配置

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 如果只使用本地存储，保持 `OSS_ENABLED=false` 即可

3. 如果要使用阿里云 OSS，需要修改 `.env` 文件：
   ```env
   OSS_ENABLED=true
   ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
   ALIYUN_OSS_BUCKET=your-bucket-name
   ALIYUN_ACCESS_KEY_ID=your-access-key-id
   ALIYUN_ACCESS_KEY_SECRET=your-access-key-secret
   OSS_PREFIX=price-index-platform
   ```

## 运行项目

```bash
# 运行完整流程（使用配置文件中的日期范围）
python -m src.main

# 指定单个日期
python -m src.main --date 2026-06-21

# 指定日期范围
python -m src.main --start-date 2026-06-01 --end-date 2026-06-30
```

## 运行测试

```bash
python -m pytest tests/
# 或
python -m unittest tests/test_compute_index.py
```

## 常见问题

### 问题 1：ModuleNotFoundError
**原因**：依赖未安装
**解决**：按照上述方法安装依赖

### 问题 2：SSL 证书错误
**原因**：网络代理或防火墙问题
**解决**：使用 `--trusted-host` 参数或配置永久镜像源

### 问题 3：OSS 上传失败
**原因**：OSS 配置错误或权限不足
**解决**：
- 检查 `.env` 文件配置是否正确
- 确认 AccessKey 有 OSS 写入权限
- 确认 Bucket 存在且可访问

### 问题 4：数据目录权限问题
**原因**：没有创建数据目录的权限
**解决**：手动创建目录或以管理员身份运行

## 项目结构说明

```
cloud-price-index/
├── README.md               # 项目说明文档
├── INSTALL.md             # 安装说明（本文件）
├── requirements.txt        # Python 依赖列表
├── .env.example           # 环境变量示例
├── .gitignore             # Git 忽略文件
├── config/
│   └── config.yaml        # 项目配置文件
├── src/                   # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── ingestion/         # 数据采集模块
│   │   └── generate_mock_data.py
│   ├── compute/           # 数据计算模块
│   │   ├── clean_data.py
│   │   ├── aggregate_data.py
│   │   └── compute_index.py
│   ├── storage/           # 存储模块
│   │   ├── local_storage.py
│   │   └── oss_client.py
│   ├── report/            # 报告生成模块
│   │   └── generate_report.py
│   └── utils/             # 工具模块
│       ├── logger.py
│       └── dates.py
├── sql/                   # SQL 脚本
│   └── clickhouse_schema.sql
├── tests/                 # 测试目录
│   └── test_compute_index.py
├── data/                  # 数据目录（运行时自动创建）
│   ├── ods/
│   ├── dwd/
│   ├── dws/
│   └── ads/
└── logs/                  # 日志目录（运行时自动创建）
```
