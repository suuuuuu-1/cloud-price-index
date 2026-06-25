# Python 版本切换指南

## 📊 你的 Python 版本情况

系统中安装了 3 个 Python：

| 版本 | 路径 | 状态 |
|------|------|------|
| **Python 3.6.8** | `D:\tofpy\` | ❌ 当前默认（太旧） |
| **Python 3.11.9** | `C:\Users\57123\AppData\Local\Programs\Python\Python311\` | ✅ 推荐使用 |
| **Python 3.12.7** | `D:\ProgramData\anaconda3\` | ✅ Anaconda（已自带pandas） |

## 🚀 快速切换（推荐方案）

### 方案 1：使用 Anaconda（最简单）

双击运行：**use_anaconda.bat**

优点：
- ✅ Anaconda 已自带 pandas、numpy 等常用包
- ✅ 无需安装依赖
- ✅ 可以直接运行项目

```bash
# 双击 use_anaconda.bat 后，直接运行：
python view_data.py
python process_real_data.py
```

### 方案 2：使用 Python 3.11

双击运行：**use_python311.bat**

```bash
# 双击 use_python311.bat 后，需要先安装 pandas：
pip install pandas -i https://mirrors.aliyun.com/pypi/simple/
python process_real_data.py
```

## 🔧 永久修改（可选）

如果想永久修改默认 Python 版本：

### Windows 图形界面方式

1. 右键"此电脑" → 属性
2. 高级系统设置 → 环境变量
3. 在"系统变量"中找到 `Path`
4. 编辑 `Path`：
   - **删除或移到最下面**：`D:\tofpy` 和 `D:\tofpy\Scripts`
   - **移到最上面**：
     - 使用 Anaconda: `D:\ProgramData\anaconda3` 和 `D:\ProgramData\anaconda3\Scripts`
     - 使用 Python 3.11: `C:\Users\57123\AppData\Local\Programs\Python\Python311` 和 `...\Scripts`
5. 确定 → 重启命令行

### PowerShell 命令方式（管理员权限）

```powershell
# 查看当前 PATH
$env:Path -split ';' | Select-String python

# 永久修改需要管理员权限，建议使用图形界面
```

## 📝 验证版本

```bash
python --version
```

期望输出：
- Python 3.11.9 或
- Python 3.12.7

## 💡 快速使用建议

**如果你想立即使用真实数据进行课程设计：**

1. **双击 `use_anaconda.bat`**（打开一个新的命令行窗口）
2. 在新窗口中运行：
   ```bash
   python view_data.py  # 查看数据
   python process_real_data.py --start-date 2025-05-17 --end-date 2025-06-15
   ```
3. 完成！结果在 `output/` 目录

## ⚠️ 注意事项

- 使用 `.bat` 文件的临时切换**只在当前窗口有效**
- 关闭命令行窗口后会恢复原来的设置
- 如果需要永久修改，按照上面的"永久修改"步骤操作

## 🎯 推荐方案

**立即使用 Anaconda**（最省事）：
```bash
双击 use_anaconda.bat
python process_real_data.py
```

Anaconda 已包含：
- ✅ pandas
- ✅ numpy
- ✅ matplotlib
- ✅ scipy
- ✅ 其他数据科学常用包
