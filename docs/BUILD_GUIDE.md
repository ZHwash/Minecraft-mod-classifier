# 打包构建指南

## 📦 快速打包

### Windows

```bash
scripts\build.bat
```

### Linux/macOS

```bash
chmod +x scripts/build.sh
./scripts/build.sh
```

打包完成后，可执行文件位于 `dist/Minecraft-mod-classifier/` 目录。

---

## 🔧 手动打包

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 执行打包

```bash
python -m PyInstaller --name "Minecraft-mod-classifier" \
  --onedir --console \
  --add-data "config/mods_data.json;config" \
  src/python/main.py
```

### 3. 创建压缩包

**Windows:**
```powershell
Compress-Archive -Path dist\Minecraft-mod-classifier\* `
  -DestinationPath release\minecraft-mod-classifier-v0.1.6-windows-x86_64.zip
```

**Linux/macOS:**
```bash
cd dist
tar -czf minecraft-mod-classifier-v0.1.6-linux-x86_64.tar.gz Minecraft-mod-classifier/
```

---

## ❓ 常见问题

### Q: 打包后运行找不到配置文件

**A:** 确保 `config/mods_data.json` 已包含在打包数据中（使用 `--add-data` 参数）

### Q: 如何更新版本号

**A:** 修改以下文件中的版本号：
- `README.md`
- `src/python/i18n.py`
- `docs/QUICKSTART.md`
- `GITHUB_INTEGRATION.md`

### Q: 打包文件太大

**A:** 
- 使用 `--onefile` 单文件模式（启动稍慢）
- 启用 UPX 压缩（`--upx-dir=/path/to/upx`）

---

**详细文档**：[README.md](../README.md)
