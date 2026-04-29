# 打包指南

## 📦 将Python程序打包为独立可执行文件

本文档介绍如何将Minecraft Mod Classifier Python版本打包为独立的可执行程序，无需安装Python即可运行。

## 🔧 打包工具

我们使用 **PyInstaller** 来打包Python程序：
- ✅ 跨平台支持（Windows/Linux/macOS）
- ✅ 单文件输出
- ✅ 包含所有依赖
- ✅ 用户无需安装Python

## 🚀 快速打包

### Windows用户

1. **确保已安装Python 3.7+**

2. **运行打包脚本**
   ```cmd
   build.bat
   ```

3. **等待打包完成**
   - 自动安装PyInstaller
   - 编译可执行文件
   - 准备发布包

4. **获取结果**
   ```
   release/Minecraft-mod-classifier/
   ├── Minecraft-mod-classifier.exe  ← 主程序
   ├── README.md
   ├── QUICKSTART.md
   ├── LICENSE
   ├── Input/                         ← 放入待分类Mod
   └── Output/                        ← 分类结果
       ├── ClientOnly/
       ├── ServerOnly/
       └── ...
   ```

### Linux/macOS用户

1. **确保已安装Python 3.7+**

2. **添加执行权限并运行**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

3. **获取结果**
   ```
   release/Minecraft-mod-classifier/
   ├── Minecraft-mod-classifier  ← 主程序
   ├── README.md
   ├── QUICKSTART.md
   ├── LICENSE
   ├── Input/
   └── Output/
   ```

## 📋 手动打包步骤

如果你想自定义打包过程：

### 1. 安装PyInstaller

```bash
pip install pyinstaller
```

### 2. 执行打包命令

**Windows:**
```cmd
pyinstaller --clean ^
    --name "Minecraft-mod-classifier" ^
    --onefile ^
    --console ^
    --add-data "mods_data.json;." ^
    main.py
```

**Linux/macOS:**
```bash
pyinstaller --clean \
    --name "Minecraft-mod-classifier" \
    --onefile \
    --console \
    --add-data "mods_data.json:." \
    main.py
```

### 3. 参数说明

| 参数 | 说明 |
|------|------|
| `--clean` | 清理临时文件 |
| `--name` | 可执行文件名称 |
| `--onefile` | 打包为单个文件 |
| `--console` | 显示控制台窗口 |
| `--add-data` | 包含额外文件（格式：源文件;目标目录） |
| `--icon` | 设置图标（可选） |
| `--windowed` | 隐藏控制台（GUI程序用） |

### 4. 准备发布包

```bash
# 创建发布目录
mkdir -p release/Minecraft-mod-classifier

# 复制可执行文件
cp dist/Minecraft-mod-classifier release/Minecraft-mod-classifier/

# 复制文档
cp README.md QUICKSTART.md LICENSE release/Minecraft-mod-classifier/

# 创建必要目录
mkdir -p release/Minecraft-mod-classifier/Input
mkdir -p release/Minecraft-mod-classifier/Output/{ClientOnly,ServerOnly,ClientRequiredServerOptional,ClientOptionalServerRequired,ClientAndServerRequired,ClientOptionalServerOptional,Unknown}
```

### 5. 压缩发布包

**Windows:**
```cmd
cd release
Compress-Archive -Path Minecraft-mod-classifier -DestinationPath minecraft-mod-classifier-windows-x86_64.zip
```

**Linux/macOS:**
```bash
cd release
tar -czf minecraft-mod-classifier-linux-x86_64.tar.gz Minecraft-mod-classifier
```

## 🎯 高级选项

### 减小文件大小

```bash
# 启用UPX压缩（需要先安装UPX）
pyinstaller --onefile --upx-dir=/path/to/upx main.py

# 或使用内置压缩
pyinstaller --onefile --strip main.py
```

### 添加程序图标

**Windows:**
```cmd
pyinstaller --onefile --icon=app.ico main.py
```

**macOS:**
```bash
pyinstaller --onefile --icon=app.icns main.py
```

### 隐藏控制台窗口（不推荐）

```bash
pyinstaller --onefile --windowed main.py
```

⚠️ **注意**：本程序是命令行工具，不建议隐藏控制台。

### 包含多个数据文件

```bash
pyinstaller --onefile \
    --add-data "mods_data.json;." \
    --add-data "README.md;." \
    --add-data "assets/*;assets/" \
    main.py
```

## 🔍 常见问题

### Q1: 打包后的文件很大（50MB+）？

**A:** 这是正常的，因为包含了Python解释器和所有依赖。

优化方法：
```bash
# 使用UPX压缩
pip install upx
pyinstaller --onefile --upx-dir=/path/to/upx main.py

# 或使用strip去除调试信息
pyinstaller --onefile --strip main.py
```

### Q2: 打包后运行报错"找不到mods_data.json"？

**A:** 确保使用了 `--add-data` 参数：

```bash
# Windows
--add-data "mods_data.json;."

# Linux/macOS
--add-data "mods_data.json:."
```

### Q3: 杀毒软件报毒？

**A:** PyInstaller打包的程序可能被误报。解决方法：
1. 向杀毒软件厂商提交白名单
2. 使用代码签名证书
3. 提供源代码供用户自行编译

### Q4: 如何减小首次启动时间？

**A:** 使用 `--onedir` 模式代替 `--onefile`：

```bash
pyinstaller --onedir main.py
```

优点：启动更快  
缺点：输出为目录而非单文件

### Q5: 跨平台打包？

**A:** PyInstaller不支持跨平台打包，需要在目标平台上分别打包：
- Windows程序 → 在Windows上打包
- Linux程序 → 在Linux上打包
- macOS程序 → 在macOS上打包

可以使用GitHub Actions自动化多平台打包。

## 📊 打包结果对比

| 项目 | Python源码 | PyInstaller打包 |
|------|-----------|----------------|
| 文件大小 | ~50KB | ~15-50MB |
| 需要Python | ✅ 是 | ❌ 否 |
| 需要依赖 | ✅ 是 | ❌ 否 |
| 启动速度 | 快 | 稍慢（解压） |
| 跨平台 | ✅ 是 | ❌ 需分别打包 |
| 易用性 | 中 | 高 |

## 🚀 GitHub Actions自动打包

项目已配置自动化打包工作流：

1. **推送代码到main分支**
2. **GitHub Actions自动触发**
3. **在Windows和Linux上打包**
4. **上传为Artifacts**
5. **Release时自动发布**

查看工作流配置：`.github/workflows/python-build.yml`

## 📝 发布检查清单

发布前请确认：

- [ ] 在目标平台测试可执行文件
- [ ] 验证所有功能正常工作
- [ ] 检查mods_data.json是否包含
- [ ] 确认Input/Output目录结构正确
- [ ] 包含必要的文档文件
- [ ] 压缩为zip/tar.gz格式
- [ ] 更新版本号
- [ ] 编写Release Notes

## 💡 最佳实践

### 1. 使用虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install pyinstaller
```

### 2. 定期清理缓存

```bash
# 删除PyInstaller缓存
rm -rf build dist *.spec
```

### 3. 版本管理

在文件名中包含版本号：
```bash
pyinstaller --name "Minecraft-mod-classifier-v2.0.0" main.py
```

### 4. 测试不同系统

在以下环境测试：
- Windows 10/11
- Ubuntu 20.04/22.04
- macOS 12/13

## 📚 相关资源

- [PyInstaller官方文档](https://pyinstaller.org/)
- [PyInstaller GitHub](https://github.com/pyinstaller/pyinstaller)
- [UPX压缩工具](https://upx.github.io/)

---

**打包完成！现在你可以分发独立的可执行文件了！** 🎉
