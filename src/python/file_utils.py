#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具模块
提供文件名清理、目录创建等通用文件操作功能
"""

import re
from pathlib import Path
from typing import Optional
from logger import setup_logger

logger = setup_logger()


def clean_mod_name(full_filename: str) -> str:
    """
    从完整的Mod文件名中提取干净的名称
    
    处理步骤：
    1. 移除方括号内的内容 [中文译名]
    2. 移除非标准分隔符
    3. 处理混合语言前缀
    4. 移除Minecraft版本号前缀
    5. 移除 "for [加载器]" 模式
    6. 迭代移除末尾的版本号、加载器等后缀
    7. 规范化空格并转换为小写
    
    Args:
        full_filename: 完整的文件名（如 "jei-1.16.5-7.7.1.118.jar"）
        
    Returns:
        清理后的文件名（如 "jei.jar"）
    """
    # 提取主文件名和扩展名
    path = Path(full_filename)
    name_to_clean = path.stem
    primary_extension = path.suffix
    
    # 特殊处理 .jar.disabled 等情况
    if '.jar' in full_filename.lower():
        jar_pos = full_filename.lower().rfind('.jar')
        name_to_clean = full_filename[:jar_pos]
        primary_extension = '.jar'
    
    # 1. 移除方括号内的内容
    name_to_clean = re.sub(r'\[[^\]]*\]', '', name_to_clean)
    
    # 2. 移除非标准分隔符（如 ·）
    name_to_clean = name_to_clean.replace('·', '')
    
    # 3. 处理混合语言前缀（提取英文部分）
    last_non_ascii_pos = -1
    for i in range(len(name_to_clean) - 1, -1, -1):
        if ord(name_to_clean[i]) > 127:
            last_non_ascii_pos = i
            break
    
    if last_non_ascii_pos != -1 and last_non_ascii_pos + 1 < len(name_to_clean):
        suffix_part = name_to_clean[last_non_ascii_pos + 1:]
        if re.search(r'[a-zA-Z]', suffix_part):
            name_to_clean = suffix_part
    
    # 4. 移除文件名开头的Minecraft版本号
    name_to_clean = re.sub(r'^[0-9]+\.[0-9]+(?:\.[0-9]+)*[-_]', '', name_to_clean, flags=re.IGNORECASE)
    
    # 5. 移除 "for [加载器或版本号]" 模式
    name_to_clean = re.sub(r'\s+for\s+[0-9a-zA-Z._-]+', '', name_to_clean, flags=re.IGNORECASE)
    
    # 6. 在加载器和数字之间插入空格
    loader_pattern = r'(forge|fabric|quilt|neoforge|rift|liteloader|nilloader)([0-9])'
    name_to_clean = re.sub(loader_pattern, r'\1 \2', name_to_clean, flags=re.IGNORECASE)
    
    # 7. 迭代移除文件名末尾的版本号、加载器等后缀
    suffix_regex = (
        r'[-_+\s.]+'
        r'(?:'
        r'[a-zA-Z]{0,4}[0-9]+(?:[\._\-][0-9a-zA-Z_+-]+)*'
        r'|mc[0-9]+(?:\.[0-9]+)*'
        r'|forge|fabric|quilt|neoforge|rift|liteloader|nilloader'
        r'|snapshot|pre|rc|beta|alpha|hotfix'
        r'|universal|all|mc'
        r')'
        r'\s*$'
    )
    
    prev_name = ""
    while name_to_clean != prev_name:
        prev_name = name_to_clean
        name_to_clean = re.sub(suffix_regex, '', name_to_clean, flags=re.IGNORECASE)
    
    # 8. 移除多余的空格，并修剪首尾空格和分隔符
    name_to_clean = re.sub(r' +', ' ', name_to_clean)
    name_to_clean = name_to_clean.strip(' -_')
    
    # 9. 转换为小写
    name_to_clean = name_to_clean.lower()
    
    return name_to_clean + primary_extension


def ensure_directory(directory_path: Path) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory_path: 目录路径
        
    Returns:
        是否成功确保目录存在
    """
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"无法创建目录 {directory_path}: {str(e)}")
        return False


def get_jar_files(input_dir: Path) -> list:
    """
    获取输入目录中的所有JAR文件
    
    Args:
        input_dir: 输入目录路径
        
    Returns:
        JAR文件路径列表
    """
    if not input_dir.exists():
        logger.warning(f"输入目录 {input_dir} 不存在")
        return []
    
    jar_files = []
    for file_path in input_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.jar':
            jar_files.append(file_path)
    
    logger.info(f"在 {input_dir} 中找到 {len(jar_files)} 个JAR文件")
    return jar_files
