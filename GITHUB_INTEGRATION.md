# GitHub集成功能使用说明

## 功能概述

Minecraft Mod Classifier 现在支持将生成的 `mods_data.json` 文件自动提交到GitHub仓库,帮助社区共享Mod分类数据。

## 使用流程

### 1. 自动提示

当分类完成后,程序会自动询问是否将 `mods_data.json` 提交到GitHub:

```
============================================================
📤 提交到GitHub
============================================================
是否将更新后的mods_data.json提交到GitHub仓库?
这将帮助社区共享Mod分类数据。

是否提交到GitHub? (y/n): 
```

### 2. 输入选项

- **y/yes/是**: 提交到GitHub
- **n/no/否**: 跳过提交

### 3. 自定义提交信息(可选)

如果选择提交,可以输入自定义的commit message:

```
请输入提交信息 (Enter使用默认): 添加了50个新Mod的分类规则
```

如果不输入,系统会自动生成包含mod数量和时间的默认信息。

### 4. 自动执行Git操作

系统会自动执行以下步骤:

1. `git add config/mods_data.json` - 添加文件到暂存区
2. `git commit -m "message"` - 提交更改
3. `git push` - 推送到远程仓库

## 前提条件

### 必须满足的条件

1. **当前目录是Git仓库**
   ```bash
   git init  # 如果还没有初始化
   ```

2. **已配置远程仓库**
   ```bash
   git remote add origin https://github.com/your-username/Minecraft-mod-classifier.git
   ```

3. **有推送权限**
   - 如果是自己的Fork,直接推送
   - 如果是原仓库,需要贡献者权限或通过PR提交

### 推荐的准备工作

1. **配置Git用户信息**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **设置SSH密钥或HTTPS认证**
   ```bash
   # SSH方式(推荐)
   ssh-keygen -t ed25519 -C "your.email@example.com"
   
   # 或使用HTTPS + Personal Access Token
   ```

## 手动提交流程

如果自动提交失败,可以手动执行:

```bash
# 1. 查看更改
git status

# 2. 添加文件
git add config/mods_data.json

# 3. 提交
git commit -m "Update mods_data.json (141 mods) - 2026-04-30 01:50:00"

# 4. 推送
git push origin main
```

## 常见问题

### Q1: 提示"当前目录不是Git仓库"

**解决方案:**
```bash
cd h:\code\Minecraft-mod-classifier
git init
git remote add origin <your-repo-url>
```

### Q2: 推送失败,需要认证

**解决方案:**
- 使用SSH密钥: 确保已添加公钥到GitHub
- 使用HTTPS: 配置Personal Access Token

### Q3: 冲突错误

**解决方案:**
```bash
# 先拉取最新代码
git pull origin main

# 解决冲突后再次提交
git add config/mods_data.json
git commit -m "Merge and update mods_data.json"
git push
```

### Q4: 不想每次都提示

目前每次分类完成都会提示。如需禁用,可以:

1. 修改 `src/python/main.py`,注释掉GitHub集成调用
2. 或者在提示时选择"否",下次仍会询问(暂时无法永久禁用)

## 贡献指南

如果你希望为社区贡献mods_data.json:

1. **Fork原仓库**
   ```
   https://github.com/original-owner/Minecraft-mod-classifier
   ```

2. **在你的Fork中提交**
   - 使用本功能自动提交到你的Fork
   - 或手动创建PR

3. **创建Pull Request**
   - 描述你添加/更新的Mod
   - 说明分类依据
   - 等待维护者审核

## 技术实现

### 核心模块

- `src/python/github_integration.py` - GitHub集成管理器
- `src/python/i18n.py` - 国际化支持(中英文提示)

### 关键方法

```python
class GitHubIntegration:
    def is_git_repository() -> bool          # 检查是否是Git仓库
    def has_uncommitted_changes() -> bool    # 检查是否有未提交更改
    def commit_and_push_mods_data() -> bool  # 提交并推送
    def prompt_user_to_submit() -> bool      # 提示用户并提交
```

## 注意事项

⚠️ **重要提醒:**

1. **隐私安全**: mods_data.json仅包含Mod ID和分类类型,不包含个人信息
2. **数据质量**: 请确保分类准确后再提交,避免污染社区数据
3. **频率限制**: GitHub API有速率限制,不要频繁推送
4. **分支管理**: 建议在独立分支上提交,便于管理多个PR

## 示例输出

### 成功提交

```
[INFO] 正在添加文件: mods_data.json
[INFO] 正在提交...
[INFO] 正在推送到远程仓库...
[INFO] ✅ 成功提交到GitHub!

[OK] ✅ 成功提交到GitHub!
```

### 跳过提交

```
[INFO] 已跳过提交
```

### 提交失败

```
[ERROR] Git push failed: ...
[WARN] 推送失败,请手动执行 git push

[ERROR] ❌ 提交失败
```

---

**版本**: v2.0.0  
**最后更新**: 2026-04-30
