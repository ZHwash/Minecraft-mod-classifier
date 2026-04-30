# 快速入门指南

## 🚀 5分钟开始使用

### 版本说明

当前版本：**v2.1.0**

**新增功能**:
- ✅ 多版本Mod管理（同一Mod的不同版本分别存储）
- ✅ Mod端识别（区分Fabric/Forge/NeoForge）
- ✅ 未知类型自动归类
- ✅ **智能规则更新** - 基于在线数据批量更新分类，支持差异分级处理

### 第一步：检查Python环境

打开终端（Windows: CMD/PowerShell，Linux/macOS: Terminal），输入：

```bash
python --version
```

或

```bash
python3 --version
```

**如果显示版本号（如 Python 3.9.7）** → 继续下一步  
**如果提示"未找到命令"** → 需要先安装Python

#### 安装Python

**Windows:**
1. 访问 https://www.python.org/downloads/
2. 下载最新版本的Python
3. 运行安装程序
4. ⚠️ **重要**：勾选 "Add Python to PATH"
5. 点击 "Install Now"

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3
```

**macOS:**
```bash
brew install python3
```

### 第二步：首次运行 - 选择语言

运行程序后，会首先询问界面语言：

```
==================================================
选择语言 / Select Language
==================================================
1. 中文 (Chinese)
2. English
==================================================
请选择 / Please select (1/2): 
```

- 输入 `1` 选择中文
- 输入 `2` 选择English

语言设置会保存，下次运行无需再次选择。

### 第三步：准备Mod文件

1. 在项目文件夹中找到 `Input` 目录
2. 将你要分类的 `.jar` Mod文件复制到 `Input` 目录

例如：
```
Input/
├── jei-1.16.5-7.7.1.118.jar
├── journeymap-1.12.2-5.6.0.jar
```

### 第四步：运行分类器

**Windows用户：**
- 双击 `run.bat` 文件

或在命令行中：
```cmd
python main.py
```

**Linux/macOS用户：**
```bash
python3 main.py
```

### 第五步：查看结果

程序会自动：
1. ✅ 扫描 `Input` 目录中的所有JAR文件
2. ✅ 清理文件名（去除版本号等信息）
3. ✅ 查询配置库或解析JAR文件
4. ✅ 将Mod分类到 `Output` 的子目录中

查看分类结果：
```
Output/
├── ClientOnly/              # 仅客户端Mod
│   └── journeymap-*.jar
├── ServerOnly/              # 仅服务端Mod
├── ClientRequiredServerOptional/  # 客户端必装，服务端可选
│   └── jei-*.jar
├── ClientOptionalServerRequired/  # 客户端可选，服务端必装
├── ClientAndServerRequired/       # 两端都必装
├── ClientOptionalServerOptional/  # 两端都可选
└── Unknown/                 # 未知类型（需手动确认）
```

### 第六步：使用分类好的Mod

从对应的子目录中取出Mod文件，放入你的Minecraft游戏目录：

**客户端Mod** → `.minecraft/mods/`  
**服务端Mod** → 服务器 `mods/` 目录

## 💡 小贴士

### 首次使用 vs 后续使用

**首次使用：**
- 程序会解析每个JAR文件
- 速度较慢（约0.05秒/文件）
- 自动学习并保存新Mod信息

**后续使用：**
- 直接使用已保存的配置
- 速度极快（约0.0001秒/文件）
- 仅新Mod需要解析

### 查看日志

所有操作都会记录在 `mod_classifier.log` 文件中：

```bash
# Windows
type mod_classifier.log

# Linux/macOS
cat mod_classifier.log
```

### 处理Unknown类型的Mod

如果某些Mod被分类到 `Unknown` 目录：

1. 查看日志了解原因
2. 手动确定Mod类型
3. 编辑 `mods_data.json` 添加正确分类
4. 重新运行程序

示例：
```json
[
  {
    "name": "problematic_mod.jar",
    "type": "client_only"
  }
]
```

### 批量处理大量Mod

如果有超过100个Mod：

1. 分批处理（每次50-100个）
2. 等待首次解析完成
3. 后续批次会更快

## ❓ 常见问题

### Q: 程序说"未找到JAR文件"

**A:** 确保：
- Mod文件放在 `Input` 目录
- 文件扩展名是 `.jar`（不是 `.jar.disabled`）

### Q: 某些Mod分类错误

**A:** 
1. 检查 `mod_classifier.log` 查看详情
2. 手动编辑 `mods_data.json` 修正
3. 提交Issue报告此Mod

### Q: 如何清空重新开始？

**A:**
```bash
# 删除输出目录
rm -rf Output/

# 清空配置（保留备份）
cp mods_data.json mods_data_backup.json
echo "[]" > mods_data.json

# 清空输入目录
rm Input/*.jar
```

### Q: 可以自定义分类类型吗？

**A:** 当前版本支持7种预定义类型。如需新增类型，请提交Feature Request.

## 🎯 下一步

- 📖 阅读 [USAGE.md](USAGE.md) 了解高级用法
- 🔍 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解技术细节
- 🤝 参与社区贡献，提交新的Mod分类规则

---

**祝你使用愉快！** 🎮✨
