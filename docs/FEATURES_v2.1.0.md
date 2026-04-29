# 功能增强说明 - v2.1.0

## 📋 需求实现总结

### ✅ 需求1：无法读取JAR配置时分类为未知

**实现状态**: 已完成

**实现细节**:
- 当`jar_parser.parse_jar()`返回`None`时，Mod被标记为`unknown`类型
- 日志输出: `[FAIL] 无法解析JAR文件，标记为未知类型`
- 文件会被复制到 `Output/Unknown/` 目录

**示例**:
```python
if mod_info:
    mod_type = mod_info['type']
    # ... 正常处理
else:
    self.logger.warning("[FAIL] 无法解析JAR文件，标记为未知类型")
    mod_type = 'unknown'
```

---

### ✅ 需求2：多版本Mod按版本存储

**实现状态**: 已完成

**实现细节**:
- 配置文件结构升级，每个Mod记录包含`version`字段
- 唯一标识: `name + version + loader`
- 相同Mod的不同版本会被分别存储

**配置示例**:
```json
[
  {
    "name": "appleskin",
    "type": "client_only",
    "version": "3.0.9",
    "loader": "neoforge"
  },
  {
    "name": "appleskin",
    "type": "client_only",
    "version": "3.0.9+mc26.1",
    "loader": "fabric"
  }
]
```

**查找逻辑**:
- 优先精确匹配（name + version + loader）
- 如果没有版本信息，回退到仅按名称匹配

---

### ✅ 需求3：不同Mod端分别存储

**实现状态**: 已完成

**实现细节**:
- 配置文件新增`loader`字段，标识Mod加载器类型
- 支持的Mod端:
  - `fabric` - Fabric Mod Loader
  - `forge` - Forge Mod Loader
  - `neoforge` - NeoForge Mod Loader
- 相同Mod在不同Mod端会被分别存储

**解析逻辑**:
```python
# Fabric Mod
mod_info = {
    'name': data.get('id', ''),
    'version': data.get('version', ''),
    'loader': 'fabric',  # ← 新增
    'type': self._infer_mod_type_from_fabric(data)
}

# Forge/NeoForge Mod
loader = 'neoforge' if 'neoforge.mods.toml' in toml_path else 'forge'
mod_info = {
    'name': mod_id_match.group(1),
    'version': version_match.group(1),
    'loader': loader,  # ← 新增
    'type': self._infer_mod_type_from_forge(content)
}
```

---

## 🔧 技术实现

### 修改的文件

1. **`src/python/config_manager.py`**
   - 新增 `_generate_mod_key()` 方法生成唯一标识
   - 更新 `find_mod()` 支持版本和loader参数
   - 更新 `add_mod()` 保存版本和loader信息
   - 更新 `update_mod()` 支持精确更新

2. **`src/python/jar_parser.py`**
   - `_parse_fabric_mod()`: 添加 `'loader': 'fabric'`
   - `_parse_forge_mods_toml()`: 根据TOML路径判断是`forge`还是`neoforge`
   - 返回的字典包含完整的 `name`, `version`, `loader`, `type` 信息

3. **`src/python/mod_classifier.py`**
   - `_process_jar_file()`: 传递版本和loader信息到配置管理器
   - 日志输出显示版本和Mod端信息

### 向后兼容性

- ✅ 旧配置文件仍可正常加载（没有version/loader字段的记录）
- ✅ 查找时如果没有提供版本/loader，会回退到仅按名称匹配
- ✅ 新添加的记录会自动包含version和loader字段

---

## 📊 测试验证

### 测试结果

```
【需求1】无法读取JAR配置时分类为未知
✓ 所有可解析的Mod正确分类
✓ 无法解析的Mod标记为unknown

【需求2 & 3】多版本和多Mod端分别存储
✓ appleskin v3.0.9 [NEOFORGE] -> client_only
✓ appleskin v3.0.9+mc26.1 [FABRIC] -> client_only
✓ appleskin v1.0.14 [FORGE] -> client_only
✓ jei v19.27.0 [NEOFORGE] -> client_required_server_optional
✓ jei v19.27.0 [FABRIC] -> client_required_server_optional

【验证】查找特定版本和Mod端的Mod
✓ 找到: appleskin v3.0.9 [NEOFORGE] -> client_only
✓ 找到: appleskin v3.0.9+mc26.1 [FABRIC] -> client_only
✓ 找到: jei v19.27.0 [FABRIC] -> client_required_server_optional
```

---

## 💡 使用示例

### 场景1：同一Mod的不同版本

用户有两个版本的AppleSkin：
- `appleskin-neoforge-mc1.21-3.0.9.jar` (NeoForge版)
- `appleskin-fabric-mc1.20-3.0.8.jar` (Fabric版)

**结果**: 两个版本会被分别存储，互不影响

### 场景2：同一版本的不同Mod端

用户有：
- `jei-1.21.1-neoforge-19.27.0.jar`
- `jei-1.21.1-fabric-19.27.0.jar`

**结果**: 虽然版本号相同，但因loader不同会被分别存储

### 场景3：无法解析的Mod

用户有一个非标准结构的JAR文件

**结果**: 被分类到 `Output/Unknown/` 目录

---

## 🎯 优势

1. **精确分类**: 区分同一Mod的不同版本和Mod端
2. **避免冲突**: 不会因为文件名相似而误用配置
3. **灵活扩展**: 未来可以基于loader进行更智能的分类
4. **向后兼容**: 旧数据仍然可用，平滑过渡

---

## 📝 注意事项

1. **配置文件大小**: 随着Mod数量增加，配置文件会变大（但JSON格式很高效）
2. **版本提取**: 某些Mod的版本号可能是占位符（如`${file.jarVersion}`），这是正常的
3. **查找优先级**: 精确匹配 > 模糊匹配，确保准确性

---

**版本**: v2.1.0  
**更新日期**: 2026-04-29  
**状态**: ✅ 已测试通过
