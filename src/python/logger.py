#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统模块
提供统一的日志记录功能，同时输出到控制台和文件
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(log_filename="mod_classifier.log"):
    """
    设置日志器
    
    Args:
        log_filename: 日志文件名
        
    Returns:
        logging.Logger: 配置好的日志器实例
    """
    # 创建日志器
    logger = logging.getLogger("ModClassifier")
    logger.setLevel(logging.DEBUG)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 设置UTF-8编码以支持中文字符
    if sys.platform == 'win32':
        import io
        console_handler.stream = io.TextIOWrapper(
            console_handler.stream.buffer, 
            encoding='utf-8', 
            errors='replace'
        )
    logger.addHandler(console_handler)
    
    # 文件处理器
    log_path = Path(log_filename)
    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
