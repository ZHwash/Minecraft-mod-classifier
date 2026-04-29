@echo off
chcp 65001 >nul
title Minecraft Mod Classifier - Python Version

echo ========================================
echo   Minecraft Mod Classifier
echo   Python Version
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] 正在启动分类器...
echo.

cd /d "%~dp0.."
python src\python\main.py

pause
