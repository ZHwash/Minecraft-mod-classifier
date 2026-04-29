@echo off
chcp 65001 >nul
title Minecraft Mod Classifier - 打包工具

echo ========================================
echo   Minecraft Mod Classifier
echo   Python版本打包工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

echo [步骤1/4] 安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [错误] PyInstaller安装失败
    pause
    exit /b 1
)
echo ✓ PyInstaller安装成功
echo.

echo [步骤2/4] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo ✓ 清理完成
echo.

echo [步骤3/4] 开始打包程序...
pyinstaller --clean ^
    --name "Minecraft-mod-classifier" ^
    --onefile ^
    --console ^
    --add-data "config\mods_data.json;." ^
    --icon=NONE ^
    src\python\main.py

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo ✓ 打包成功
echo.

echo [步骤4/4] 准备发布包...
set RELEASE_DIR=release\Minecraft-mod-classifier

REM 创建发布目录
if exist %RELEASE_DIR% rmdir /s /q %RELEASE_DIR%
mkdir %RELEASE_DIR%

REM 复制可执行文件
copy dist\Minecraft-mod-classifier.exe %RELEASE_DIR%\

REM 复制必要的文件
copy README.md %RELEASE_DIR%\
copy QUICKSTART.md %RELEASE_DIR%\
copy LICENSE %RELEASE_DIR%\

REM 创建Input和Output目录
mkdir %RELEASE_DIR%\Input
mkdir %RELEASE_DIR%\Output
mkdir %RELEASE_DIR%\Output\ClientOnly
mkdir %RELEASE_DIR%\Output\ServerOnly
mkdir %RELEASE_DIR%\Output\ClientRequiredServerOptional
mkdir %RELEASE_DIR%\Output\ClientOptionalServerRequired
mkdir %RELEASE_DIR%\Output\ClientAndServerRequired
mkdir %RELEASE_DIR%\Output\ClientOptionalServerOptional
mkdir %RELEASE_DIR%\Output\Unknown

echo ✓ 发布包准备完成
echo.

echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 发布包位置: %RELEASE_DIR%
echo.
echo 下一步：
echo 1. 测试可执行文件是否正常运行
echo 2. 压缩为zip文件用于发布
echo 3. 上传到GitHub Release
echo.

pause
