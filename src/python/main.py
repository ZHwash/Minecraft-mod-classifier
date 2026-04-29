#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft Mod Classifier - Python Version
自动分类 Minecraft Mod 文件的命令行工具
"""

import sys
import os
from pathlib import Path
from mod_classifier import ModClassifier
from logger import setup_logger
from i18n import i18n


def main():
    """主函数"""
    # 首次运行时询问语言设置
    settings_file = Path('config/settings.json')
    if not settings_file.exists():
        i18n.select_language_interactive()
    
    # 设置日志
    logger = setup_logger()
    
    # 显示启动信息
    print("\n" + "="*60)
    print(f"  {i18n.get('app_name')} {i18n.get('app_version')}")
    print(f"  {i18n.get('app_description')}")
    print("="*60)
    print(f"  {i18n.get('current_language')}: {i18n.get('chinese') if i18n.current_language == 'zh' else i18n.get('english')}")
    print("="*60 + "\n")
    
    logger.info("程序启动")
    
    try:
        # 创建分类器实例
        classifier = ModClassifier()
        
        # 确保输入输出目录存在
        classifier.ensure_directories()
        
        # 加载或创建配置文件
        classifier.load_or_create_config()
        
        # 执行分类
        classifier.classify_mods()
        
        logger.info(i18n.get('completed'))
        print(f"\n[OK] {i18n.get('completed')}")
        
    except Exception as e:
        logger.error(f"{i18n.get('error')}: {str(e)}", exc_info=True)
        print(f"\n[ERROR] {i18n.get('error')}: {str(e)}")
        input(f"\n{i18n.get('press_enter')}")
        return 1
    
    input(f"\n{i18n.get('press_enter')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
