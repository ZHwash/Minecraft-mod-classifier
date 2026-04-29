# 项目结构说明

## 📁 目录结构

```
Minecraft-mod-classifier/
│
├── 📄 README.md                    # 项目主文档
├── 📄 LICENSE                      # 许可证文件
├── 📄 requirements.txt             # Python依赖列表
├── 📄 CMakeLists.txt              # C++构建配置（保留供参考）
├── 📄 .gitignore                  # Git忽略规则
│
├── 📂 src/                        # 源代码目录
│   ├── 📂 python/                 # Python源代码
│   │   ├── __init__.py
│   │   ├── main.py                # 主程序入口
│   │   ├── mod_classifier.py      # 核心分类逻辑
│   │   ├── jar_parser.py          # JAR包解析器
│   │   ├── config_manager.py      # 配置管理
│   │   ├── file_utils.py          # 文件工具
│   │   ├── logger.py              # 日志系统
│   │   └── test.py                # 测试脚本
│   │
│   └── 📂 cpp/                    # C++源代码（保留供参考）
│       └── main.cpp
│
├── 📂 scripts/                    # 脚本文件
│   ├── run.bat                    # Windows启动脚本
│   ├── run.sh                     # Linux/macOS启动脚本
│   ├── build.bat                  # Windows打包脚本
│   ├── build.sh                   # Linux/macOS打包脚本
│   └── test_build.bat             # 快速测试打包脚本
│
├── 📂 config/                     # 配置文件
│   ├── mods_data.json             # Mod分类配置数据库
│   └── build.spec                 # PyInstaller打包配置
│
├── 📂 docs/                       # 文档目录
│   ├── QUICKSTART.md              # 快速入门指南 ⭐
│   ├── USAGE.md                   # 详细使用指南
│   ├── BUILD_GUIDE.md             # 打包指南
│   ├── COMPARISON.md              # C++ vs Python对比
│   ├── MIGRATION.md               # 迁移指南
│   ├── PROJECT_SUMMARY.md         # 项目技术总结
│   ├── COMPLETION_SUMMARY.md      # 完成总结
│   ├── CHECKLIST.md               # 检查清单
│   ├── PACKAGING_COMPARISON.md    # 打包方式对比
│   ├── PACKAGING_QUICK_REF.md     # 打包快速参考
│   ├── PACKAGING_SUMMARY.md       # 打包方案总结
│   └── README_PYTHON.md           # Python版本介绍
│
├── 📂 assets/                     # 资源文件
│   └── mods_data.json             # 原始配置数据（备份）
│
├── 📂 Input/                      # 输入目录（运行时创建）
│   └── *.jar                      # 待分类的Mod文件
│
├── 📂 Output/                     # 输出目录（运行时创建）
│   ├── ClientOnly/
│   ├── ServerOnly/
│   ├── ClientRequiredServerOptional/
│   ├── ClientOptionalServerRequired/
│   ├── ClientAndServerRequired/
│   ├── ClientOptionalServerOptional/
│   └── Unknown/
│
└── 📂 .github/                    # GitHub配置
    └── workflows/
        ├── build.yml              # C++版本CI/CD
        └── python-build.yml       # Python版本CI/CD
```

## 📋 目录说明

### `src/` - 源代码
存放所有源代码文件。

**`src/python/`**
- Python版本的主要代码
- 模块化设计，职责清晰
- 包含完整的测试脚本

**`src/cpp/`**
- C++版本的原始代码
- 保留供参考和对比

### `scripts/` - 脚本文件
存放所有可执行脚本。

- **启动脚本**: `run.bat`, `run.sh`
- **打包脚本**: `build.bat`, `build.sh`
- **测试脚本**: `test_build.bat`

### `config/` - 配置文件
存放所有配置和数据文件。

- `mods_data.json`: Mod分类规则数据库
- `build.spec`: PyInstaller打包配置

### `docs/` - 文档
存放所有文档文件，按用途分类。

**核心文档:**
- `QUICKSTART.md` - 新用户必读
- `USAGE.md` - 详细使用说明
- `BUILD_GUIDE.md` - 打包指南

**技术文档:**
- `COMPARISON.md` - 版本对比
- `PROJECT_SUMMARY.md` - 技术总结
- `MIGRATION.md` - 迁移指南

**打包相关:**
- `PACKAGING_*.md` - 打包相关文档

### `assets/` - 资源文件
存放静态资源文件（备份）。

### `Input/` 和 `Output/` - 运行时目录
程序运行时自动创建的目录。
- `Input/`: 放入待分类的Mod文件
- `Output/`: 获取分类结果

## 🚀 快速导航

### 新手用户
1. 阅读 [`README.md`](../README.md)
2. 查看 [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
3. 运行 `scripts/run.bat` (Windows) 或 `scripts/run.sh` (Linux/macOS)

### 开发者
1. 查看 [`src/python/`](src/python/) 源代码
2. 阅读 [`docs/PROJECT_SUMMARY.md`](docs/PROJECT_SUMMARY.md)
3. 运行 `scripts/test_build.bat` 测试打包

### 想要打包？
1. 阅读 [`docs/BUILD_GUIDE.md`](docs/BUILD_GUIDE.md)
2. 运行 `scripts/build.bat` (Windows) 或 `scripts/build.sh` (Linux/macOS)
3. 查看 [`docs/PACKAGING_QUICK_REF.md`](docs/PACKAGING_QUICK_REF.md) 快速获取帮助

## 📝 文件分类原则

| 文件类型 | 存放位置 | 示例 |
|---------|---------|------|
| 源代码 | `src/python/` | `.py` 文件 |
| 脚本 | `scripts/` | `.bat`, `.sh` 文件 |
| 配置 | `config/` | `.json`, `.spec` 文件 |
| 文档 | `docs/` | `.md` 文件 |
| 资源 | `assets/` | 静态资源文件 |
| 根目录 | 项目根目录 | `README.md`, `LICENSE` 等核心文件 |

## 💡 最佳实践

### 添加新文档
- 用户指南 → `docs/`
- 技术规范 → `docs/`
- 更新 `README.md` 中的相关链接

### 添加新脚本
- 启动脚本 → `scripts/`
- 构建脚本 → `scripts/`
- 更新相关文档

### 添加新配置
- 数据配置 → `config/`
- 构建配置 → `config/` 或项目根目录

---

**清晰的项目结构，让开发更高效！** 🎯
