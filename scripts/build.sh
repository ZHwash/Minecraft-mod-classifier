#!/bin/bash

echo "========================================"
echo "  Minecraft Mod Classifier"
echo "  Python版本打包工具"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.7或更高版本"
    exit 1
fi

echo "[步骤1/4] 安装PyInstaller..."
pip3 install pyinstaller
if [ $? -ne 0 ]; then
    echo "[错误] PyInstaller安装失败"
    exit 1
fi
echo "✓ PyInstaller安装成功"
echo ""

echo "[步骤2/4] 清理旧的构建文件..."
rm -rf build dist *.spec
echo "✓ 清理完成"
echo ""

echo "[步骤3/4] 开始打包程序..."
pyinstaller --clean \
    --name "Minecraft-mod-classifier" \
    --onefile \
    --console \
    --add-data "config/mods_data.json:." \
    src/python/main.py

if [ $? -ne 0 ]; then
    echo "[错误] 打包失败"
    exit 1
fi
echo "✓ 打包成功"
echo ""

echo "[步骤4/4] 准备发布包..."
RELEASE_DIR="release/Minecraft-mod-classifier"

# 创建发布目录
rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

# 复制可执行文件
cp dist/Minecraft-mod-classifier "$RELEASE_DIR/"

# 复制必要的文件
cp README.md "$RELEASE_DIR/"
cp QUICKSTART.md "$RELEASE_DIR/"
cp LICENSE "$RELEASE_DIR/"

# 创建Input和Output目录
mkdir -p "$RELEASE_DIR/Input"
mkdir -p "$RELEASE_DIR/Output/ClientOnly"
mkdir -p "$RELEASE_DIR/Output/ServerOnly"
mkdir -p "$RELEASE_DIR/Output/ClientRequiredServerOptional"
mkdir -p "$RELEASE_DIR/Output/ClientOptionalServerRequired"
mkdir -p "$RELEASE_DIR/Output/ClientAndServerRequired"
mkdir -p "$RELEASE_DIR/Output/ClientOptionalServerOptional"
mkdir -p "$RELEASE_DIR/Output/Unknown"

# 添加执行权限
chmod +x "$RELEASE_DIR/Minecraft-mod-classifier"

echo "✓ 发布包准备完成"
echo ""

echo "========================================"
echo "  打包完成！"
echo "========================================"
echo ""
echo "发布包位置: $RELEASE_DIR"
echo ""
echo "下一步："
echo "1. 测试可执行文件是否正常运行"
echo "2. 压缩为tar.gz文件用于发布"
echo "3. 上传到GitHub Release"
echo ""
