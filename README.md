# Minecraft Mod Classifier (Python Version)

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-v2.0.0-orange.svg)](https://github.com/ZHwash/Minecraft-mod-classifier/releases)

> **⚠️ 注意：** 这是 [DHJComical/Minecraft-mod-classifier](https://github.com/DHJComical/Minecraft-mod-classifier) 的 Python 重构版本。原项目使用 C++ 实现，本版本完全重写为 Python，提供更简洁的代码、更好的跨平台支持和更低的贡献门槛。

## 🎮 项目简介

一个智能的 Minecraft Mod 分类工具，自动识别和分类 Mod 文件的运行端属性（客户端/服务端）。

**核心特性：**
- ✅ **三层优先级分类** - JAR配置 > 规则数据库 > Modrinth API
- ✅ **自动学习机制** - 新Mod自动识别并同步至规则数据库
- ✅ **多语言支持** - 中文/English 界面
- ✅ **全面格式支持** - Fabric/Forge/NeoForge
- ✅ **零依赖运行** - 仅需 Python 标准库
- ✅ **小白友好贡献** - 自动生成补丁文件，无需Git知识

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


### 自动 JAR 解析

当配置库中没有该 Mod 时，自动读取 JAR 内部配置文件：
- `fabric.mod.json` (Fabric)
- `META-INF/neoforge.mods.toml` (NeoForge)
- `META-INF/mods.toml` (Forge)
- `mcmod.info` (旧版 Forge)

### 自动学习机制

首次运行时解析 JAR 并保存配置到 `config/mods_data.json`，后续运行直接查询。每次运行后自动将新识别的Mod同步至 `config/mod_rules.json` 规则数据库。

### 🆕 GitHub 集成（新增）

分类完成后，可选择生成规则更新补丁文件：

```bash
# 分类完成后会提示：
🔄 规则数据库更新（推荐）
============================================================
您可以帮助改进分类规则数据库！
我们可以生成一个更新补丁文件，您只需将其提交到GitHub即可。
无需任何技术知识，小白也能轻松贡献！

是否生成规则更新补丁文件? (y/n): y

✓ 成功生成更新补丁: rule_update_patch_20260430_172121.json
  新增规则: 19 条
  更新规则: 150 条
  总计变更: 169 条

📤 如何提交更新：
  方法1（最简单）：
    1. 打开 GitHub Issues: https://github.com/ZHwash/Minecraft-mod-classifier/issues
    2. 点击 'New Issue'
    3. 将此文件内容粘贴进去并提交
```

**前提条件：**
- 无需任何Git或GitHub Token配置
- 生成的JSON补丁文件包含详细的提交说明

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
│   ├── rule_manager.py      # 规则数据库管理
│   ├── modrinth_api.py      # Modrinth API集成
│   ├── file_utils.py        # 文件工具函数
│   ├── logger.py            # 日志系统
│   └── i18n.py              # 国际化支持
├── config/                  # 配置文件
│   ├── mods_data.json       # Mod配置数据库（自动生成）
│   ├── mod_rules.json       # 规则数据库（798条规则）
│   └── settings.json        # 用户设置
├── Input/                   # 输入目录（放入待分类Mod）
├── Output/                  # 输出目录（分类结果）
│   ├── ClientOnly/          # 仅客户端
│   ├── ServerOnly/          # 仅服务端
│   ├── ClientAndServerRequired/  # 双端必需
│   └── ...                  # 其他分类目录
└── docs/                    # 文档
    ├── QUICKSTART.md        # 快速入门
    ├── USAGE.md             # 详细使用说明
    └── BUILD_GUIDE.md       # 打包构建指南
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

- 📝 **添加新的Mod分类规则** - 通过生成补丁文件提交至GitHub Issues
- 🐛 **修复Bug** - 提交Issue或直接PR
- ✨ **添加新功能** - 如GUI界面、Web API等
- 📖 **改进文档** - 让新手更容易上手
- 🌍 **翻译支持** - 添加新语言

**小白友好贡献流程：**
1. 运行分类程序，自动识别新Mod
2. 选择“是”生成规则更新补丁文件
3. 打开生成的JSON文件，复制内容
4. 到GitHub Issues页面粘贴并提交
5. 完成！无需任何Git知识

如果你想为**原 C++ 项目**贡献，请前往 [DHJComical/Minecraft-mod-classifier](https://github.com/DHJComical/Minecraft-mod-classifier)。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢 [DHJComical](https://github.com/DHJComical) 创建的原始 C++ 版本，为本项目提供了灵感和基础设计思路。
