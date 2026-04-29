# Minecraft Mod Classifier (Python Version)

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-v0.1.7-orange.svg)](https://github.com/ZHwash/Minecraft-mod-classifier/releases/tag/v0.1.7)

> **⚠️ 注意：** 这是 [DHJComical/Minecraft-mod-classifier](https://github.com/DHJComical/Minecraft-mod-classifier) 的 Python 重构版本。原项目使用 C++ 实现，本版本完全重写为 Python，提供更简洁的代码、更好的跨平台支持和更低的贡献门槛。

## 🎮 项目简介

一个智能的 Minecraft Mod 分类工具，自动识别和分类 Mod 文件的运行端属性（客户端/服务端）。

**核心特性：**
- ✅ **智能双层分类** - 配置库快速匹配 + JAR 解析自动学习
- ✅ **多语言支持** - 中文/English 界面
- ✅ **全面格式支持** - Fabric/Forge/NeoForge
- ✅ **零依赖运行** - 仅需 Python 标准库
- ✅ **开箱即用** - 可打包为独立可执行文件

---

## 🚀 快速开始

### 方式一：使用独立可执行文件（推荐）

#### Windows
1. 下载 [Releases](https://github.com/ZHwash/Minecraft-mod-classifier/releases) 中的 `minecraft-mod-classifier-v0.1.7-windows-x86_64.zip`
2. 解压后双击 `Minecraft-mod-classifier.exe`
3. 将 `.jar` Mod 文件放入 `Input` 目录
4. 从 `Output` 目录获取分类结果

#### Linux/macOS
```bash
tar -xzf minecraft-mod-classifier-v0.1.7-linux-x86_64.tar.gz
cd Minecraft-mod-classifier
chmod +x Minecraft-mod-classifier
./Minecraft-mod-classifier
```

### 方式二：使用 Python 源码

```bash
git clone https://github.com/ZHwash/Minecraft-mod-classifier.git
cd Minecraft-mod-classifier
python src/python/main.py
```

详细使用说明请查看 [docs/USAGE.md](docs/USAGE.md)

---

## 📊 功能特性

### 支持的 Mod 类型

| 类型 | 说明 | 典型示例 |
|------|------|---------|
| ClientOnly | 仅客户端需要 | 小地图、光影、HUD |
| ServerOnly | 仅服务端需要 | 备份插件、性能优化 |
| ClientRequiredServerOptional | 客户端必装，服务端可选 | JEI、REI |
| ClientOptionalServerRequired | 客户端可选，服务端必装 | 世界生成Mod |
| ClientAndServerRequired | 两端都必须安装 | 大多数内容Mod |
| ClientOptionalServerOptional | 两端都可选 | 配置库、API库 |
| Unknown | 无法自动识别 | 需手动确认 |

### 智能文件名清洗

自动清理干扰信息：
```
"[机械动力]create-1.21.1-6.0.10-neoforge.jar" → "create.jar"
"jei-1.16.5-7.7.1.118.jar" → "jei.jar"
```

### 自动 JAR 解析

当配置库中没有该 Mod 时，自动读取 JAR 内部配置文件：
- `fabric.mod.json` (Fabric)
- `META-INF/neoforge.mods.toml` (NeoForge)
- `META-INF/mods.toml` (Forge)
- `mcmod.info` (旧版 Forge)

### 自动学习机制

首次运行时解析 JAR 并保存配置到 `config/mods_data.json`，后续运行直接查询，速度提升 **500倍**！

### 🆕 GitHub 集成（新增）

分类完成后，可选择将 `mods_data.json` 自动提交到 GitHub 仓库：

```bash
# 分类完成后会提示：
📤 提交到GitHub
是否将更新后的mods_data.json提交到GitHub仓库?
这将帮助社区共享Mod分类数据。

是否提交到GitHub? (y/n): y
请输入提交信息 (Enter使用默认): 添加了50个新Mod的分类规则

✅ 成功提交到GitHub!
```

**前提条件：**
- 当前目录是 Git 仓库
- 已配置远程仓库 (`git remote add origin <url>`)
- 有推送权限

详细说明请查看 [GITHUB_INTEGRATION.md](GITHUB_INTEGRATION.md)

---

## 🔗 与原项目的关系

**本仓库：** [ZHwash/Minecraft-mod-classifier](https://github.com/ZHwash/Minecraft-mod-classifier) (Python版本)  
**原仓库：** [DHJComical/Minecraft-mod-classifier](https://github.com/DHJComical/Minecraft-mod-classifier) (C++版本)

我们从原 C++ 项目 Fork 并进行了完全重构，主要原因包括：

1. **降低门槛** - Python 比 C++ 更容易学习和贡献
2. **内置 JAR 解析** - Python 的 `zipfile` 模块天然支持读取 JAR 文件
3. **无需编译** - 可直接运行或打包为独立可执行文件
4. **跨平台友好** - 同一份代码可在 Windows/Linux/macOS 运行
5. **代码简洁** - ~600行 Python vs ~800行 C++

**选择建议：**
- 🎯 如果你想要**开箱即用、易于维护**的版本 → 使用 **Python 版本**（本仓库）
- 🎯 如果你偏好**原生性能、C++生态** → 使用 **C++ 原版**（原仓库）

---

## 📁 项目结构

```
Minecraft-mod-classifier/
├── src/python/              # Python源代码
│   ├── main.py              # 主程序入口
│   ├── mod_classifier.py    # 核心分类逻辑
│   ├── jar_parser.py        # JAR包解析器
│   ├── config_manager.py    # 配置管理器
│   ├── file_utils.py        # 文件工具函数
│   ├── logger.py            # 日志系统
│   └── i18n.py              # 国际化支持
├── config/                  # 配置文件
│   ├── mods_data.json       # Mod配置数据库（自动生成）
│   └── settings.json        # 用户设置
├── Input/                   # 输入目录（放入待分类Mod）
├── Output/                  # 输出目录（分类结果）
├── docs/                    # 文档
│   ├── QUICKSTART.md        # 快速入门
│   ├── USAGE.md             # 详细使用说明
│   └── BUILD_GUIDE.md       # 打包构建指南
└── scripts/                 # 实用脚本
    ├── run.bat/sh           # 启动脚本
    └── build.bat/sh         # 打包脚本
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！❤️

### 如何贡献

1. **Fork 本仓库**
2. **创建功能分支** 
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **提交更改**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **推送到分支**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **开启 Pull Request**

### 可以贡献的内容

- 📝 **添加新的Mod分类规则** - 扩充 `mods_data.json`
- 🐛 **修复Bug** - 提交Issue或直接PR
- ✨ **添加新功能** - 如GUI界面、Web API等
- 📖 **改进文档** - 让新手更容易上手
- 🌍 **翻译支持** - 添加新语言

如果你想为**原 C++ 项目**贡献，请前往 [DHJComical/Minecraft-mod-classifier](https://github.com/DHJComical/Minecraft-mod-classifier)。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢 [DHJComical](https://github.com/DHJComical) 创建的原始 C++ 版本，为本项目提供了灵感和基础设计思路。
