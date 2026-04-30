# GitHub集成功能使用说明

## 功能概述

Minecraft Mod Classifier 现在支持自动生成规则更新补丁文件，帮助社区共享Mod分类数据。程序会在分类完成后、规则同步之前自动生成增量补丁，便于审查和合并。

## 使用流程

### 1. 自动生成补丁

当分类完成并检测到新 Mod 时，程序会自动生成规则更新补丁：

```
[2026-04-30 17:52:23] INFO: 正在生成规则更新补丁...
✓ 成功生成增量补丁: rule_update_patch_20260430_175223.json
  新增规则: 0 条
  更新规则: 72 条
  总计变更: 72 条

📤 如何提交更新：
  方法1（推荐 - 使用合并工具）：
    python src/python/apply_patch.py rule_update_patch_20260430_175223.json

  方法2（手动 - 通过GitHub Issue）：
    1. 打开 GitHub Issues
    2. 创建新Issue，标题：规则数据库更新 - 2026-04-30
    3. 将此JSON文件内容粘贴到Issue中
    4. 维护者会使用工具自动合并
```

### 2. 补丁文件结构

生成的补丁文件包含以下信息：

```json
{
  "version": "2.0",
  "generated_at": "2026-04-30T17:52:23.xxx",
  "description": "Minecraft Mod Classifier 规则数据库增量更新补丁",
  "summary": {
    "total_changes": 72,
    "new_rules": 0,
    "updated_rules": 72
  },
  "new_rules": [],
  "updated_rules": [
    {
      "mod_id": "sodium",
      "changes": {
        "reason": {
          "old": "",
          "new": ""
        }
      }
    }
  ],
  "merge_instructions": [...]
}
```

### 3. 工作流程

1. **分类完成** → 保存 mods_data.json（包含 reason 字段）
2. **生成补丁** → 比较 mods_data.json 和 mod_rules.json
3. **检测差异** → 生成增量补丁文件
4. **同步规则** → 将配置更新至 mod_rules.json

**关键点：**
- 补丁在规则同步**之前**生成，确保能检测到所有变更
- mods_data.json 和 mod_rules.json 都包含 reason 字段（默认为空字符串）
- 只有当检测到新 Mod 时才会生成补丁

## 前提条件

### 必须满足的条件

1. **Python 环境**
   ```bash
   python --version  # 需要 Python 3.7+
   ```

2. **配置文件存在**
   - `config/mods_data.json` - Mod 配置数据库
   - `config/mod_rules.json` - 规则数据库

### 推荐的准备工作

1. **安装依赖**（如需使用 apply_patch.py）
   ```bash
   pip install -r requirements.txt
   ```

2. **了解 Git 基本操作**（可选，用于提交补丁）

## 手动提交流程

如果需要使用补丁文件，可以手动执行：

```bash
# 1. 查看补丁内容
cat rule_update_patch_20260430_175223.json

# 2. 使用合并工具应用补丁
python src/python/apply_patch.py rule_update_patch_20260430_175223.json

# 3. 检查合并结果
git diff config/mod_rules.json

# 4. 提交更改
git add config/mod_rules.json
git commit -m "Update mod rules from patch"
git push
```

## 常见问题

### Q1: 没有生成补丁文件

**解决方案:**
- 确认是否有新 Mod 被检测到（`auto_detected > 0`）
- 检查 `config/mods_data.json` 是否为空
- 查看日志中是否有“正在生成规则更新补丁...”的信息

### Q2: 补丁显示 0 条变更

**解决方案:**
- 这是正常情况，说明 mods_data.json 和 mod_rules.json 完全一致
- 可能原因：所有 Mod 都已存在于规则数据库中
- 或者 reason 字段已经同步

### Q3: 如何应用补丁

**解决方案:**
```bash
# 使用提供的合并工具
python src/python/apply_patch.py <补丁文件名>

# 或手动合并
# 1. 打开补丁文件，复制 new_rules 和 updated_rules
# 2. 手动添加到 config/mod_rules.json
```

### Q4: 不想每次生成都提示

目前补丁生成是自动进行的（无需用户交互）。如需禁用，可以：

1. 修改 `src/python/mod_classifier.py`，注释掉 `_generate_patch_before_sync()` 调用
2. 或者在 `classify_mods()` 方法中移除相关代码

## 贡献指南

如果你希望为社区贡献规则更新：

1. **运行分类程序**
   - 将新的 Mod 放入 Input 目录
   - 运行程序进行分类

2. **获取补丁文件**
   - 程序会自动生成 `rule_update_patch_*.json`
   - 检查补丁内容是否正确

3. **提交到 GitHub**
   - 方式1：使用 `apply_patch.py` 合并后提交 PR
   - 方式2：将补丁文件内容粘贴到 GitHub Issue

4. **等待审核**
   - 维护者会审核补丁内容
   - 合并到主分支

## 技术实现

### 核心模块

- `src/python/generate_patch.py` - 补丁生成器
- `src/python/apply_patch.py` - 补丁合并工具
- `src/python/config_manager.py` - 配置管理器（含 reason 字段）
- `src/python/mod_classifier.py` - 分类器（在同步前生成补丁）

### 关键方法

```python
# generate_patch.py
def generate_incremental_patch(
    source_config: str = "config/mods_data.json",
    target_rules: str = "config/mod_rules.json",
    output_patch: str = None
) -> str:
    """生成增量补丁文件"""
    # 比较两个文件，找出差异
    # 返回补丁文件路径

# mod_classifier.py
def _generate_patch_before_sync(self):
    """在同步规则之前生成增量补丁"""
    # 此时 mods_data.json 已更新，但 mod_rules.json 还未同步
    # 可以正确检测到所有变更
```

### 数据结构

**mods_data.json:**
```json
[
  {
    "mod_id": "sodium",
    "mod_name": "Sodium",
    "type": "client_only",
    "reason": ""  // 新增字段，默认为空字符串
  }
]
```

**mod_rules.json:**
```json
{
  "rules": [
    {
      "mod_id": "sodium",
      "mod_name": "Sodium",
      "type": "client_only",
      "reason": ""  // 已清理为空字符串
    }
  ]
}
```

## 注意事项

⚠️ **重要提醒:**

1. **数据一致性**: reason 字段在所有配置中都应存在（即使为空），确保比较时不会遗漏
2. **补丁时机**: 补丁必须在规则同步之前生成，否则无法检测到变更
3. **数据质量**: 请确保分类准确后再提交补丁，避免污染社区数据
4. **频率限制**: 不要频繁生成大量补丁，建议批量处理后一次性提交
5. **备份重要**: 在应用补丁前，建议备份 `config/mod_rules.json`

## 示例输出

### 成功生成补丁

```
[2026-04-30 17:52:23] INFO: 正在生成规则更新补丁...

✓ 成功生成增量补丁: rule_update_patch_20260430_175223.json
  新增规则: 0 条
  更新规则: 72 条
  总计变更: 72 条

📤 如何提交更新：
  方法1（推荐 - 使用合并工具）：
    python src/python/apply_patch.py rule_update_patch_20260430_175223.json

  方法2（手动 - 通过GitHub Issue）：
    1. 打开 GitHub Issues
    2. 创建新Issue，标题：规则数据库更新 - 2026-04-30
    3. 将此JSON文件内容粘贴到Issue中
    4. 维护者会使用工具自动合并
[2026-04-30 17:52:23] INFO: ✓ 增量补丁文件已生成: rule_update_patch_20260430_175223.json
```

### 无需生成补丁

```
[2026-04-30 17:44:45] INFO: 规则数据库已是最新，无需生成补丁
```

### 应用补丁

```
$ python src/python/apply_patch.py rule_update_patch_20260430_175223.json
正在加载补丁文件: rule_update_patch_20260430_175223.json
✓ 补丁文件加载成功
  新增规则: 0 条
  更新规则: 72 条
正在合并补丁...
✓ 成功合并 72 条规则更新
✓ 规则数据库已更新
```

---

**版本**: v2.0.0  
**最后更新**: 2026-04-30  
**主要变更**: 
- 改为自动生成补丁（无需用户交互）
- 在规则同步之前生成补丁
- 添加 reason 字段到所有配置
- 清理 mod_rules.json 中的 reason 内容为空字符串
