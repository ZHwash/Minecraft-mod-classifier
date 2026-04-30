# 快速入门指南

## 🚀 5分钟开始使用

### 版本说明

当前版本：**v0.1.6**

**核心功能**:
- ✅ 三层优先级分类 - JAR配置 > 规则数据库 > Modrinth API
- ✅ 自动学习机制 - 新Mod自动识别并保存
- ✅ 智能规则更新 - 基于在线数据批量更新分类
- ✅ 增量补丁生成 - 自动生成规则更新补丁

### 第一步：运行程序

**Windows用户：**
```cmd
双击 run.bat
```

**Linux/macOS用户：**
```bash
chmod +x run.sh
./run.sh
```

### 第二步：放入Mod文件

将 `.jar` Mod文件复制到 `Input` 目录：
```
Input/
├── jei-1.16.5.jar
├── journeymap-1.12.2.jar
```

### 第三步：查看结果

程序会自动分类到 `Output` 目录：
```
Output/
├── ClientOnly/              # 仅客户端（小地图、光影）
├── ServerOnly/              # 仅服务端
├── ClientRequiredServerOptional/  # 客户端必装（JEI）
├── ClientAndServerRequired/       # 双端必需
└── Unknown/                 # 需手动确认
```

### 第四步：使用分类好的Mod

- **客户端Mod** → `.minecraft/mods/`
- **服务端Mod** → 服务器 `mods/` 目录

---

## 💡 提示

**首次运行**：会解析JAR文件（较慢）  
**后续运行**：直接使用已保存的配置（极快）

**查看详细文档**：[README.md](../README.md)
