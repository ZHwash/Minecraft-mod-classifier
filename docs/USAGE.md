# 使用示例

## 快速开始

### Windows用户

1. 双击 `run.bat` 文件
2. 或者在命令行中运行：
   ```cmd
   python main.py
   ```

### Linux/macOS用户

1. 给脚本添加执行权限：
   ```bash
   chmod +x run.sh
   ```
2. 运行脚本：
   ```bash
   ./run.sh
   ```
3. 或者直接运行：
   ```bash
   python3 main.py
   ```

## 工作流程示例

### 第一次使用

```
程序启动
├─→ 创建 Input/ 目录
├─→ 创建 Output/ 目录及7个子目录
├─→ 创建空的 mods_data.json
└─→ 等待用户在 Input/ 中放入Mod文件
```

### 分类流程

假设 Input/ 目录中有以下文件：
```
Input/
├── jei-1.16.5-7.7.1.118.jar
├── journeymap-1.12.2-5.6.0.jar
└── optifine_1.16.5_hd_u_g8.jar
```

运行程序后的输出：
```
============================================================
开始分类Mod...
============================================================

处理: jei-1.16.5-7.7.1.118.jar
清理后的名称: jei.jar
配置中未找到，尝试解析JAR文件...
✓ 自动检测到类型: client_required_server_optional
✓ 已分类到: ClientRequiredServerOptional

处理: journeymap-1.12.2-5.6.0.jar
清理后的名称: journeymap.jar
配置中未找到，尝试解析JAR文件...
✓ 自动检测到类型: client_only
✓ 已分类到: ClientOnly

处理: optifine_1.16.5_hd_u_g8.jar
清理后的名称: optifine.jar
✓ 在配置中找到: client_only
✓ 已分类到: ClientOnly

============================================================
分类统计:
============================================================
总文件数: 3
成功分类: 3
自动检测: 2
跳过文件: 0
分类失败: 0
============================================================
```

Output/ 目录结构：
```
Output/
├── ClientOnly/
│   ├── journeymap-1.12.2-5.6.0.jar
│   └── optifine_1.16.5_hd_u_g8.jar
├── ClientRequiredServerOptional/
│   └── jei-1.16.5-7.7.1.118.jar
├── ServerOnly/
├── ClientOptionalServerRequired/
├── ClientAndServerRequired/
├── ClientOptionalServerOptional/
└── Unknown/
```

mods_data.json 已自动更新：
```json
[
  {
    "name": "jei.jar",
    "type": "client_required_server_optional"
  },
  {
    "name": "journeymap.jar",
    "type": "client_only"
  }
]
```

### 第二次使用（利用已学习的配置）

当再次运行程序时：
- `jei.jar` 和 `journeymap.jar` 会直接从配置中读取，无需解析JAR
- 新的Mod文件会被自动检测和添加到配置中

## 高级用法

### 手动编辑配置文件

你可以直接编辑 `mods_data.json` 来：
- 修正自动检测错误的类型
- 添加特殊的Mod规则
- 批量导入已有的分类数据

格式示例：
```json
[
  {
    "name": "mod_name.jar",
    "type": "client_only"
  },
  {
    "name": "another_mod.jar",
    "type": "client_and_server_required"
  }
]
```

可用的类型值：
- `client_only` - 仅客户端
- `server_only` - 仅服务端
- `client_required_server_optional` - 客户端必装，服务端可选
- `client_optional_server_required` - 客户端可选，服务端必装
- `client_and_server_required` - 两端都必装
- `client_optional_server_optional` - 两端都可选
- `unknown` - 未知类型

### 查看日志

所有操作都会记录在 `mod_classifier.log` 文件中：
```bash
# Windows
type mod_classifier.log

# Linux/macOS
cat mod_classifier.log
```

## 故障排除

### 问题1：Python未找到

**Windows:**
```
[错误] 未检测到Python，请先安装Python 3.7或更高版本
```

解决方案：
1. 访问 https://www.python.org/downloads/
2. 下载并安装Python
3. 安装时勾选 "Add Python to PATH"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3

# CentOS/RHEL
sudo yum install python3
```

### 问题2：编码问题

如果遇到中文显示乱码：

**Windows:**
```cmd
chcp 65001
python main.py
```

或直接使用 `run.bat`（已自动设置编码）

### 问题3：JAR解析失败

如果某个Mod被标记为 `Unknown`：
1. 检查 `mod_classifier.log` 查看详细错误
2. 确认JAR文件未损坏
3. 手动在 `mods_data.json` 中添加该Mod的分类
4. 提交Issue报告此Mod的信息

## 性能提示

- 首次运行时，每个新Mod都需要解析JAR文件，可能较慢
- 后续运行会直接使用配置库，速度显著提升
- 对于大量Mod（100+），建议分批处理
- 定期备份 `mods_data.json` 以保留学习成果
