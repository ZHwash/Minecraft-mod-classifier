#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具模块
提供文件和目录操作的实用函数
"""

import sys
from pathlib import Path
from typing import List, Optional


def ensure_directory(dir_path: Path) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        dir_path: 目录路径
        
    Returns:
        是否成功（True表示目录已存在或创建成功）
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败 {dir_path}: {str(e)}")
        return False


def get_resource_path(relative_path: str) -> Path:
    """
    获取资源文件的绝对路径（兼容开发环境和PyInstaller打包环境）
    
    Args:
        relative_path: 相对路径（相对于项目根目录）
        
    Returns:
        资源的绝对路径
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的环境
        # 可执行文件在 dist/Minecraft-mod-classifier/
        # 用户数据应该保存在可执行文件同级目录，而不是 _internal
        base_path = Path(sys.executable).parent
    else:
        # 开发环境
        # 从 src/python/ 向上两级到项目根目录
        base_path = Path(__file__).parent.parent.parent
    
    return base_path / relative_path


def get_jar_files(directory: Path) -> List[Path]:
    """
    获取目录中所有的JAR文件
    
    Args:
        directory: 目标目录
        
    Returns:
        JAR文件路径列表
    """
    if not directory.exists() or not directory.is_dir():
        return []
    
    jar_files = list(directory.glob('*.jar'))
    # 按文件名排序
    jar_files.sort(key=lambda x: x.name.lower())
    
    return jar_files
