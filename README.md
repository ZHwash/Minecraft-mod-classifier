# Minecraft Mod Classifier

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-v0.1.7--python-orange.svg)](RELEASE_NOTES_v2.1.0.md)

> **v0.1.7-python** - Python重构版本 | 从C++ v0.1.6演进而来

## 🎮 项目简介

一个智能的 Minecraft Mod 分类工具，自动识别和分类 Mod 文件的运行端属性（客户端/服务端），帮助你轻松管理 Mod 文件。

### ✨ 核心特性

**🌍 多语言支持**
- ✅ 中文界面 - 完整的中文用户界面和文件夹名称
- ✅ English Interface - Full English UI and folder names
- ✅ 首次运行交互式选择，设置持久化保存

**🤖 智能双层分类策略**
- 优先使用配置库（快速匹配）
- 自动解析JAR包配置文件（智能学习）
- 自动学习新Mod并更新配置库（持续进化）

**📦 全面支持多种Mod格式**
- ✅ Fabric (`fabric.mod.json`)
- ✅ Forge (`META-INF/mods.toml`)
- ✅ NeoForge (`META-INF/neoforge.mods.toml`)
- ✅ 旧版Forge (`mcmod.info`)

**🔧 高级功能 (v0.1.7-python)**
- ✅ **多版本管理** - 同一Mod的不同版本分别存储配置
- ✅ **Mod端识别** - 区分Fabric/Forge/NeoForge不同加载器
- ✅ **精确匹配** - 基于 `name + version + loader` 的唯一标识系统
- ✅ **未知类型处理** - 无法解析的Mod自动归类为Unknown

**🚀 简单易用**
- 零依赖，仅需Python标准库
- 跨平台支持（Windows/Linux/macOS）
- 可打包为独立可执行文件（无需安装Python）
- 详细的日志和统计信息

---

## 📋 目录

- [快速开始](#-快速开始)
- [功能特性](#-功能特性详解)
- [使用方法](#-使用方法)
- [项目结构](#-项目结构)
- [技术细节](#-技术细节)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## 🚀 快速开始

### 方式一：使用独立可执行文件（推荐 ⭐）

**无需安装Python！开箱即用！**

#### Windows 用户

1. **下载Release版本**
   - 访问 [Releases页面](https://github.com/DHJComical/Minecraft-mod-classifier/releases)
   - 下载 `minecraft-mod-classifier-v0.1.7-python-windows-x86_64.zip`

2. **解压并运行**
   ```powershell
   # 解压压缩包
   # 双击 Minecraft-mod-classifier.exe
   ```

3. **准备Mod文件**
   - 将所有 `.jar` Mod文件放入 `Input` 目录

4. **获取结果**
   - 程序运行后，从 `Output` 目录的子文件夹中获取分类好的Mod

#### Linux/macOS 用户

```bash
# 1. 下载并解压
tar -xzf minecraft-mod-classifier-v0.1.7-python-linux-x86_64.tar.gz
cd Minecraft-mod-classifier

# 2. 添加执行权限
chmod +x Minecraft-mod-classifier

# 3. 准备Mod文件
mkdir -p Input
# 将 .jar 文件复制到 Input/ 目录

# 4. 运行
./Minecraft-mod-classifier

# 5. 从 Output/ 目录获取结果
```

---

### 方式二：使用Python源码

需要 **Python 3.7 或更高版本**。

#### 步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/DHJComical/Minecraft-mod-classifier.git
   cd Minecraft-mod-classifier
   ```

2. **准备Mod文件**
   - 将所有 `.jar` Mod文件放入 `Input` 目录

3. **运行分类器**
   
   **Windows:**
   ```cmd
   # 方式1: 使用启动脚本（推荐）
   scripts\run.bat
   
   # 方式2: 直接运行
   python src\python\main.py
   ```
   
   **Linux/macOS:**
   ```bash
   # 方式1: 使用启动脚本（推荐）
   chmod +x scripts/run.sh
   ./scripts/run.sh
   
   # 方式2: 直接运行
   python3 src/python/main.py
   ```

4. **获取结果**
   - 从 `Output` 目录的子文件夹中取出分类好的Mod

---

### 📺 第一次使用？

查看 **[docs/QUICKSTART.md](docs/QUICKSTART.md)** 获取详细的5分钟入门指南！

包含：
- ✅ Python环境检查与安装
- ✅ 首次运行的语言选择
- ✅ 完整的操作流程演示
- ✅ 常见问题解答

---

### 🔨 想要自己打包？

查看 **[docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md)** 了解如何将Python源码打包为独立可执行文件。

包含：
- ✅ PyInstaller打包教程
- ✅ 一键打包脚本使用说明
- ✅ GitHub Actions自动化构建
- ✅ 各平台打包注意事项

---

## ✨ 功能特性详解

### 1. 🌍 多语言支持

首次运行时可选择界面语言，设置保存在 `config/settings.json`：

**中文界面示例：**
```
============================================================
  Minecraft Mod 分类器 v0.1.7-python
  自动分类 Minecraft Mod 文件的命令行工具
============================================================
  当前语言: 中文
============================================================

[OK] 程序启动
[OK] 在 Input 中找到 142 个JAR文件
[OK] ✓ 已分类到: 仅客户端
```

**English Interface Example:**
```
============================================================
  Minecraft Mod Classifier v0.1.7-python
  Command-line tool for automatic classification of Minecraft Mods
============================================================
  Current Language: English
============================================================

[OK] Program started
[OK] Found 142 JAR files in Input
[OK] ✓ Classified to: ClientOnly
```

---

### 2. 🤖 智能分类系统

支持 **7种Mod类型**，覆盖所有使用场景：

| 类型（中文） | Type (English) | 说明 | 典型示例 |
|------------|----------------|------|---------|
| 仅客户端 | ClientOnly | 仅客户端需要 | 小地图、光影、HUD、按键绑定 |
| 仅服务端 | ServerOnly | 仅服务端需要 | 备份插件、性能优化、世界生成 |
| 客户端必需-服务端可选 | ClientRequiredServerOptional | 客户端必装，服务端可选 | JEI、REI、物品管理器 |
| 客户端可选-服务端必需 | ClientOptionalServerRequired | 客户端可选，服务端必装 | 世界生成Mod、数据结构 |
| 客户端和服务端必需 | ClientAndServerRequired | 两端都必须安装 | 大多数内容Mod（方块、生物等） |
| 客户端和服务端可选 | ClientOptionalServerOptional | 两端都可选 | 配置库、API库 |
| 未知类型 | Unknown | 无法自动识别 | 需手动确认或编辑配置 |

---

### 3. 🧹 智能文件名清洗

自动清理Mod文件名中的干扰信息，提高匹配准确率：

**处理规则：**
```javascript
// 移除版本号
"jei-1.16.5-7.7.1.118.jar" → "jei.jar"

// 移除MC版本标识
"mod-1.12.2.jar" → "mod.jar"
"mod-mc1.16.5.jar" → "mod.jar"

// 移除中文括号及内容
"[我的模组]mod.jar" → "mod.jar"
"[苹果皮]appleskin.jar" → "appleskin.jar"

// 移除加载器标识
"mod-forge.jar" → "mod.jar"
"mod-fabric.jar" → "mod.jar"
"mod-neoforge.jar" → "mod.jar"

// 组合处理
"[机械动力]create-1.21.1-6.0.10-neoforge.jar" 
→ "create.jar"
```

---

### 4. 🔍 自动JAR解析

当配置库中没有该Mod时，自动读取JAR内部的配置文件：

**支持的配置文件：**

```
mod.jar
├── fabric.mod.json          ← Fabric Mod
│   ├── id: "modid"
│   ├── version: "1.0.0"
│   └── depends/suggests     ← 用于类型推断
│
├── META-INF/
│   ├── mods.toml            ← Forge Mod
│   │   ├── modId = "modid"
│   │   ├── version = "1.0.0"
│   │   └── side = "CLIENT"  ← 直接指定类型
│   │
│   └── neoforge.mods.toml   ← NeoForge Mod
│       └── (同上)
│
└── mcmod.info               ← 旧版Forge
    ├── modid: "modid"
    └── version: "1.0.0"
```

**解析流程：**
```python
parse_jar(jar_path)
  ├→ 检查 fabric.mod.json
  │   └→ 提取modId、version、loader='fabric'
  │   └→ 根据depends推断类型
  │
  ├→ 检查 META-INF/neoforge.mods.toml
  │   └→ 提取modId、version、loader='neoforge'
  │   └→ 读取side字段确定类型
  │
  ├→ 检查 META-INF/mods.toml
  │   └→ 提取modId、version、loader='forge'
  │   └→ 读取side字段确定类型
  │
  └→ 检查 mcmod.info
      └→ 提取modId、version
      └→ 默认标记为client_and_server_required
```

---

### 5. 📚 自动学习机制

**首次运行（学习阶段）：**
```
新Mod detected!
  ↓
解析JAR文件
  ↓
提取 modId, version, loader
  ↓
推断类型（基于配置文件）
  ↓
保存到 config/mods_data.json ✓
  ↓
分类完成
```

**后续运行（快速匹配）：**
```
已知Mod
  ↓
查询配置文件（精确匹配 name+version+loader）
  ↓
直接使用已学习的类型（超快！）✓
  ↓
分类完成
```

**性能对比：**
- 首次运行（含JAR解析）：~0.05秒/文件
- 后续运行（配置查询）：~0.0001秒/文件
- **速度提升：500倍！** 🚀

---

### 6. 📊 详细日志与统计

**实时日志输出：**
```log
[2026-04-29 18:15:30] INFO: 程序启动
[2026-04-29 18:15:30] INFO: 检查目录结构...
[2026-04-29 18:15:30] INFO: 目录结构检查完成
[2026-04-29 18:15:30] INFO: 加载配置文件...
[2026-04-29 18:15:30] INFO: 成功加载 142 条Mod配置
[2026-04-29 18:15:30] INFO: ============================================================
[2026-04-29 18:15:30] INFO: 开始分类Mod...
[2026-04-29 18:15:30] INFO: ============================================================
[2026-04-29 18:15:30] INFO: 在 Input 中找到 142 个JAR文件
[2026-04-29 18:15:30] INFO: 
处理: appleskin-neoforge-mc1.21-3.0.9.jar
[2026-04-29 18:15:30] INFO: ✓ 在配置中找到: client_only
[2026-04-29 18:15:30] INFO: ✓ 已分类到: 仅客户端
```

**结束统计：**
```
============================================================
分类统计:
============================================================
总文件数: 142
成功分类: 142
自动检测新Mod: 7
失败: 0
============================================================
```

**日志文件：**
- 所有操作记录在 `mod_classifier.log`
- 便于排查问题和追踪分类历史

---

## 📖 使用方法

### 基本工作流程

```
┌─────────────────┐
│  放置Mod文件     │
│  到 Input/ 目录  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  运行分类器      │
│  main.py / .exe │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  程序自动分类     │
│  （智能学习）    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  从 Output/ 获取 │
│  分类好的Mod     │
└─────────────────┘
```

### 高级用法

#### 1️⃣ 手动编辑配置

编辑 `config/mods_data.json` 来修正或添加分类：

```json
[
  {
    "name": "jei",
    "type": "client_required_server_optional",
    "version": "19.27.0",
    "loader": "neoforge"
  },
  {
    "name": "jei",
    "type": "client_required_server_optional",
    "version": "19.27.0",
    "loader": "fabric"
  }
]
```

**配置字段说明：**
- `name`: Mod名称（必填）
- `type`: Mod类型（必填）
- `version`: 版本号（可选，v0.1.7新增）
- `loader`: Mod加载器（可选，v0.1.7新增：fabric/forge/neoforge）

---

#### 2️⃣ 切换语言

编辑 `config/settings.json`：

```json
{
  "language": "zh-CN"  // 或 "en-US"
}
```

或删除该文件，下次运行时会重新询问。

---

#### 3️⃣ 批量处理大量Mod

对于 **100+ Mod文件**：

1. **分批处理**（建议每次50-100个）
2. **首次运行较慢**（需要解析JAR并学习）
3. **后续运行极快**（直接查询配置）
4. **查看日志**了解哪些是新Mod

**性能数据：**
- 100个Mod（首次）：~5-10秒
- 100个Mod（后续）：<1秒
- 1000个Mod（首次）：~50-100秒
- 1000个Mod（后续）：<5秒

---

#### 4️⃣ 重置配置

```bash
# Windows PowerShell
Remove-Item config\mods_data.json

# Linux/macOS
rm config/mods_data.json
```

然后重新运行，程序会重新学习所有Mod。

---

## 📁 项目结构

```
Minecraft-mod-classifier/
│
├── 📄 README.md                      # 本文件 - 项目主文档
├── 📄 LICENSE                        # MIT许可证
├── 📄 requirements.txt               # Python依赖（实际上为空）
├── 📄 RELEASE_NOTES_v2.1.0.md       # 发布说明
│
├── 📂 src/python/                    # Python源代码
│   ├── __init__.py
│   ├── main.py                       # 🚀 主程序入口
│   ├── mod_classifier.py             # 🎯 核心分类逻辑
│   ├── jar_parser.py                 # 🔍 JAR包解析器
│   ├── config_manager.py             # ⚙️ 配置管理器
│   ├── file_utils.py                 # 📁 文件工具函数
│   ├── logger.py                     # 📝 日志系统
│   └── i18n.py                       # 🌍 国际化支持
│
├── 📂 scripts/                       # 实用脚本
│   ├── run.bat / run.sh              # 启动脚本
│   ├── build.bat / build.sh          # 打包脚本
│   └── test_build.bat                # 测试打包
│
├── 📂 config/                        # 配置文件
│   ├── mods_data.json                # Mod配置数据库（自动生成）
│   └── settings.json                 # 用户设置（语言等）
│
├── 📂 docs/                          # 文档目录
│   ├── QUICKSTART.md                 # ⭐ 快速入门指南
│   ├── USAGE.md                      # 📖 详细使用说明
│   ├── BUILD_GUIDE.md                # 🔨 打包构建指南
│   ├── PROJECT_STRUCTURE.md          # 🏗️ 项目结构说明
│   ├── FEATURES_v2.1.0.md            # ✨ v0.1.7新功能详解
│   └── CLEANUP_AND_RELEASE_SUMMARY.md # 📋 清理与发布总结
│
├── 📂 Input/                         # 📥 输入目录（放入待分类Mod）
│   └── *.jar
│
├── 📂 Output/                        # 📤 输出目录（分类结果）
│   ├── ClientOnly/                   # 仅客户端
│   ├── ServerOnly/                   # 仅服务端
│   ├── ClientRequiredServerOptional/ # 客户端必需-服务端可选
│   ├── ClientOptionalServerRequired/ # 客户端可选-服务端必需
│   ├── ClientAndServerRequired/      # 客户端和服务端必需
│   ├── ClientOptionalServerOptional/ # 客户端和服务端可选
│   └── Unknown/                      # 未知类型（v0.1.7新增）
│
├── 📂 release/                       # 发布包目录
│   ├── Minecraft-mod-classifier/     # 解压后的程序目录
│   ├── minecraft-mod-classifier-*.zip # 压缩发布包
│   └── RELEASE_CHECKLIST.md          # 发布检查清单
│
├── 📂 dist/                          # PyInstaller构建输出（临时）
├── 📂 build/                         # PyInstaller构建缓存（临时）
│
└── mod_classifier.log                # 运行时日志文件
```

**详细说明请查看：** [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---

## 🔧 技术细节

### 架构设计

```
┌──────────────────────┐
│   main.py            │ ← 程序入口 & 用户交互
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  mod_classifier.py   │ ← 业务逻辑协调器
└──┬───┬────┬────┬─────┘
   │   │    │    │
   ▼   ▼    ▼    ▼
┌────┐┌────┐┌────┐┌────┐
│JP  ││CM  ││FU  ││LG  │
└────┘└────┘└────┘└────┘

JP: JarParser      (jar_parser.py)    - JAR解析
CM: ConfigManager  (config_manager.py) - 配置管理
FU: FileUtils      (file_utils.py)     - 文件操作
LG: Logger         (logger.py)         - 日志系统
```

### JAR解析流程

```python
JarParser.parse_jar(jar_path)
  │
  ├→ 打开ZIP文件
  │
  ├→ 检查 fabric.mod.json
  │   ├→ 解析JSON
  │   ├→ 提取: id, version, loader='fabric'
  │   └→ 调用 _infer_mod_type_from_fabric()
  │
  ├→ 检查 META-INF/neoforge.mods.toml
  │   ├→ 读取TOML内容
  │   ├→ 提取: modId, version, loader='neoforge'
  │   └→ 调用 _infer_mod_type_from_forge()
  │
  ├→ 检查 META-INF/mods.toml
  │   ├→ 读取TOML内容
  │   ├→ 提取: modId, version, loader='forge'
  │   └→ 调用 _infer_mod_type_from_forge()
  │
  └→ 检查 mcmod.info
      ├→ 解析JSON
      ├→ 提取: modid, version
      └→ 默认类型: client_and_server_required
```

### 类型推断逻辑

#### Fabric Mod
```python
_infer_mod_type_from_fabric(data):
  depends = data.get('depends', {})
  
  # 常见客户端API
  client_apis = {'fabric-renderer', 'cloth-config', 'modmenu'}
  
  # 常见服务端API
  server_apis = {'fabric-api', 'fabric', 'server'}
  
  if has_client_dep and not has_server_dep:
    return 'client_only'
  elif has_server_dep and not has_client_dep:
    return 'client_optional_server_required'
  else:
    return 'client_and_server_required'
```

#### Forge/NeoForge Mod
```python
_infer_mod_type_from_forge(content):
  # 1. 查找side字段
  side_match = re.search(r'side\s*=\s*"(\w+)"', content)
  
  if side_match:
    side = side_match.group(1).lower()
    if side == 'client':
      return 'client_only'
    elif side == 'server':
      return 'client_optional_server_required'
  
  # 2. 关键词匹配（modId）
  client_keywords = ['jei', 'rei', 'minimap', 'hud', ...]
  server_keywords = ['backup', 'world', 'chunk', ...]
  
  if matches_client_keyword:
    return 'client_required_server_optional'
  
  # 3. 默认策略
  return 'client_required_server_optional'  # 更保守的选择
```

### 配置唯一标识系统 (v0.1.7)

**标识格式：** `name|version|loader`

**示例：**
```
appleskin|3.0.9|neoforge
appleskin|3.0.8|fabric
jei|19.27.0|neoforge
jei|19.27.0|fabric
```

**查找优先级：**
1. 精确匹配（name + version + loader）
2. 模糊匹配（仅name，向后兼容）

---

## ❓ 常见问题

### Q1: Python版本和原C++版本有什么区别？

**A:** Python版本是v0.1.6 C++版本的重构升级：

| 特性 | C++ v0.1.6 | Python v0.1.7 |
|------|-----------|--------------|
| JAR解析 | ❌ 不支持 | ✅ 完整支持 |
| 自动学习 | ❌ 无 | ✅ 有 |
| 多版本管理 | ❌ 无 | ✅ 有 |
| Mod端识别 | ❌ 无 | ✅ 有 |
| 代码量 | ~800行 | ~600行 |
| 编译需求 | ✅ 需要 | ❌ 不需要 |
| 跨平台 | ⚠️ 需分别编译 | ✅ 直接运行 |
| 社区贡献门槛 | 高（需C++知识） | 低（Python易学） |

**推荐使用Python版本！** 🚀

---

### Q2: 某些Mod分类错误怎么办？

**A:** 有三种解决方法：

1. **查看日志了解详情**
   ```bash
   cat mod_classifier.log
   # 或
   type mod_classifier.log
   ```

2. **手动编辑配置修正**
   ```json
   // config/mods_data.json
   {
     "name": "problematic_mod",
     "type": "correct_type_here",
     "version": "1.0.0",
     "loader": "neoforge"
   }
   ```

3. **提交Issue报告**
   - 提供Mod文件名
   - 提供期望的分类类型
   - 附上相关日志

---

### Q3: 如何清空重新开始？

**A:**
```bash
# Windows PowerShell
Remove-Item -Recurse Output\*
Remove-Item config\mods_data.json
Remove-Item Input\*.jar

# Linux/macOS
rm -rf Output/*
rm config/mods_data.json
rm Input/*.jar
```

然后重新运行，程序会从头开始学习。

---

### Q4: 为什么有些Mod被标记为Unknown？

**A:** 可能原因：
1. JAR文件损坏或非标准格式
2. 缺少标准的配置文件（fabric.mod.json等）
3. 配置文件格式不正确

**解决方法：**
- 检查Mod文件是否完整
- 手动编辑 `config/mods_data.json` 添加分类
- 从Output/Unknown/目录手动移动文件

---

### Q5: 配置文件会越来越大吗？

**A:** 是的，但不用担心：
- JSON格式非常高效
- 1000个Mod的配置约100KB
- 10000个Mod约1MB
- 对性能影响微乎其微

**优化建议：**
- 定期清理不再使用的Mod配置
- 保持配置文件整洁

---

### Q6: 支持其他语言吗？

**A:** 目前支持：
- ✅ 中文 (zh-CN)
- ✅ 英文 (en-US)

未来计划：
- 🔄 日语 (ja-JP)
- 🔄 韩语 (ko-KR)
- 🔄 俄语 (ru-RU)

欢迎贡献翻译！

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

---

### 可以贡献的内容

- 📝 **添加新的Mod分类规则** - 扩充 `mods_data.json`
- 🐛 **修复Bug** - 提交Issue或直接PR
- ✨ **添加新功能** - 如GUI界面、Web API等
- 📖 **改进文档** - 让新手更容易上手
- 🌍 **翻译支持** - 添加新语言
- 🎨 **优化UI** - 改进用户体验

---

### 开发环境搭建

```bash
# 1. 克隆仓库
git clone https://github.com/DHJComical/Minecraft-mod-classifier.git
cd Minecraft-mod-classifier

# 2. 运行测试
python src/python/main.py

# 3. 修改代码...

# 4. 测试修改
python src/python/main.py

# 5. 打包测试
scripts/build.bat  # Windows
./scripts/build.sh # Linux/macOS
```

---

### 代码规范

- ✅ 使用清晰的变量名和函数名
- ✅ 添加必要的注释
- ✅ 遵循PEP 8 Python编码规范
- ✅ 保持代码简洁易读
- ✅ 测试后再提交

---

## 📊 性能数据

| 指标 | 数值 | 说明 |
|------|------|------|
| 启动时间 | ~0.3秒 | 冷启动 |
| 文件名清洗 | ~0.001秒/文件 | 正则表达式 |
| JAR解析 | ~0.05秒/文件 | ZIP读取+JSON解析 |
| 配置查询 | ~0.0001秒/文件 | 字典查找 |
| 100个Mod分类（首次） | ~5-10秒 | 含JAR解析 |
| 100个Mod分类（后续） | <1秒 | 纯配置查询 |
| 内存占用 | ~30MB | 运行时 |
| 可执行文件大小 | ~17MB | 解压后 |
| 压缩发布包 | ~8MB | zip格式 |

---

## 📄 许可证

本项目采用 **MIT 许可证** 

详见 [LICENSE](LICENSE) 文件

**你可以：**
- ✅ 自由使用
- ✅ 自由修改
- ✅ 自由分发
- ✅ 商业使用

**只需：**
- 保留原始许可证和版权声明

---

## 🙏 致谢

感谢以下项目和贡献者：

- **[nlohmann/json](https://github.com/nlohmann/json)** - C++版本的JSON库（原C++版本使用）
- **[PyInstaller](https://www.pyinstaller.org/)** - Python打包工具
- **所有Mod开发者** - 创造了精彩的Minecraft生态
- **所有贡献者和用户** - 你们的反馈让这个项目更好

---

## 📞 联系方式

- 📧 **Issue**: https://github.com/DHJComical/Minecraft-mod-classifier/issues
- 💬 **讨论区**: GitHub Discussions
- 📖 **Wiki**: 查看 docs/ 目录

---

## 🌟 支持项目

**如果这个项目对你有帮助，请给它一个Star！** ⭐

你的支持是我们持续开发的动力！

---

<p align="center">
  <strong>让Mod管理变得简单高效</strong> 🎮✨
</p>

<p align="center">
  Made with ❤️ by the Minecraft Community
</p>
