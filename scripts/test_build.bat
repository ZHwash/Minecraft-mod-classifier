@echo off
chcp 65001 >nul
title Minecraft Mod Classifier - 快速测试打包

echo ========================================
echo   快速测试打包（开发模式）
echo ========================================
echo.

REM 检查PyInstaller是否安装
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo [步骤1/3] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✓ 清理完成
echo.

echo [步骤2/3] 快速打包（调试模式）...
pyinstaller --clean ^
    --name "Minecraft-mod-classifier-test" ^
    --onedir ^
    --console ^
    --add-data "config\mods_data.json;." ^
    src\python\main.py

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo ✓ 打包成功
echo.

echo [步骤3/3] 测试运行...
echo.
echo 即将运行打包后的程序...
echo 按Ctrl+C可中止
echo.
pause

dist\Minecraft-mod-classifier-test\Minecraft-mod-classifier-test.exe

echo.
echo ========================================
echo   测试完成！
echo ========================================
echo.
echo 如需正式打包，请运行 build.bat
echo.

pause
