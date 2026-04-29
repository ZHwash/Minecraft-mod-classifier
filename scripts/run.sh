#!/bin/bash

echo "========================================"
echo "  Minecraft Mod Classifier"
echo "  Python Version"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.7或更高版本"
    exit 1
fi

echo "[信息] Python版本: $(python3 --version)"
echo "[信息] 正在启动分类器..."
echo ""

# 切换到项目根目录
cd "$(dirname "$0")/.."
python3 src/python/main.py
