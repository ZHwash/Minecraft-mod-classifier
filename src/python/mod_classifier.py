#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mod分类器核心模块
整合所有功能，实现完整的Mod分类流程
"""

import shutil
from pathlib import Path
from typing import Dict, Optional
from logger import setup_logger
from config_manager import ConfigManager
from jar_parser import JarParser
from file_utils import ensure_directory, get_jar_files
from i18n import i18n


class ModClassifier:
    """Mod分类器"""
    
    # Mod类型枚举
    MOD_TYPES = [
        'client_only',
        'server_only',
        'client_required_server_optional',
        'client_optional_server_required',
        'client_and_server_required',
        'client_optional_server_optional',
        'unknown'
    ]
    
    def __init__(self, input_dir: str = "Input", output_dir: str = "Output", 
                 config_path: str = "config/mods_data.json"):
        """
        初始化分类器
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            config_path: 配置文件路径
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.config_manager = ConfigManager(config_path)
        self.jar_parser = JarParser()
        self.logger = setup_logger()
        
        # 统计信息
        self.stats = {
            'total': 0,
            'classified': 0,
            'auto_detected': 0,
            'failed': 0
        }
    
    def ensure_directories(self):
        """确保输入输出目录存在"""
        self.logger.info("检查目录结构...")
        
        # 创建输入目录
        if not ensure_directory(self.input_dir):
            raise Exception(f"无法创建输入目录: {self.input_dir}")
        
        # 创建输出目录及所有子目录
        if not ensure_directory(self.output_dir):
            raise Exception(f"无法创建输出目录: {self.output_dir}")
        
        for mod_type in self.MOD_TYPES:
            subdir = self.output_dir / i18n.get_folder_name(mod_type)
            if not ensure_directory(subdir):
                raise Exception(f"无法创建子目录: {subdir}")
        
        self.logger.info("目录结构检查完成")
    
    def load_or_create_config(self):
        """加载或创建配置文件"""
        self.logger.info("加载配置文件...")
        
        if not self.config_manager.load_config():
            self.logger.info("配置文件不存在或格式错误，创建默认配置")
            if not self.config_manager.create_default_config():
                raise Exception("无法创建默认配置文件")
        
        self.logger.info(f"当前配置包含 {self.config_manager.get_mod_count()} 条Mod记录")
    
    def classify_mods(self):
        """执行Mod分类"""
        self.logger.info("=" * 60)
        self.logger.info("开始分类Mod...")
        self.logger.info("=" * 60)
        
        # 获取所有JAR文件
        jar_files = get_jar_files(self.input_dir)
        
        if not jar_files:
            self.logger.warning("输入目录中没有找到JAR文件")
            return
        
        self.stats['total'] = len(jar_files)
        
        # 处理每个JAR文件
        for jar_path in jar_files:
            self._process_jar_file(jar_path)
        
        # 保存更新后的配置
        if self.stats['auto_detected'] > 0:
            self.logger.info(f"检测到 {self.stats['auto_detected']} 个新Mod，保存配置...")
            self.config_manager.save_config()
        
        # 输出统计信息
        self._print_statistics()
    
    def _process_jar_file(self, jar_path: Path):
        """
        处理单个JAR文件
        
        Args:
            jar_path: JAR文件路径
        """
        filename = jar_path.name
        
        self.logger.info(f"\n处理: {filename}")
        
        # 1. 解析JAR文件获取modId和类型（三层优先级判断）
        mod_info = self.jar_parser.parse_jar(jar_path)
        
        if not mod_info:
            self.logger.warning(f"无法解析 {filename}，跳过")
            self.stats['failed'] += 1
            return
        
        mod_id = mod_info.get('mod_id', '')
        mod_type = mod_info.get('type', 'unknown')
        
        if not mod_id:
            self.logger.warning(f"{filename} 中未找到modId，跳过")
            self.stats['failed'] += 1
            return
        
        self.logger.debug(f"Mod ID: {mod_id}, 推断类型: {mod_type}")
        
        # 2. 在配置中查找（仅基于mod_id）
        mod_config = self.config_manager.find_mod(mod_id)
        
        if mod_config:
            # 配置中存在，直接使用
            mod_type = mod_config['type']
            self.logger.info(f"[OK] 在配置中找到: {mod_type}")
        else:
            # 3. 配置中不存在，使用解析结果中的类型（来自三层优先级判断）
            self.logger.info(f"[OK] 自动检测到类型: {mod_type}")
            
            # 添加到配置中（仅mod_id和type）
            if self.config_manager.add_mod(mod_id, mod_type):
                self.stats['auto_detected'] += 1
        
        # 4. 复制文件到对应目录
        self._copy_to_output(jar_path, mod_type)
        self.stats['classified'] += 1
    
    def _copy_to_output(self, source_path: Path, mod_type: str):
        """
        复制文件到输出目录
        
        Args:
            source_path: 源文件路径
            mod_type: Mod类型
        """
        target_dir_name = i18n.get_folder_name(mod_type)
        target_path = self.output_dir / target_dir_name / source_path.name
        
        # 检查目标文件是否已存在
        if target_path.exists():
            self.logger.info(f"⊙ 文件已存在（已分类）: {target_dir_name}")
            self.stats['classified'] += 1  # 计入已分类，而不是跳过
            return
        
        try:
            # 复制文件
            shutil.copy2(source_path, target_path)
            self.logger.info(f"✓ 已分类到: {target_dir_name}")
            self.stats['classified'] += 1
            
        except Exception as e:
            self.logger.error(f"✗ 复制文件失败: {str(e)}")
            self.stats['failed'] += 1
    
    def _print_statistics(self):
        """打印统计信息"""
        self.logger.info("\n" + "=" * 60)
        self.logger.info(i18n.get('completed'))
        self.logger.info("=" * 60)
        self.logger.info(f"{i18n.get('total_processed').format(self.stats['total'])}")
        self.logger.info(f"{i18n.get('total_success').format(self.stats['classified'])}")
        self.logger.info(f"自动检测新Mod: {self.stats['auto_detected']}")
        self.logger.info(f"{i18n.get('total_failed').format(self.stats['failed'])}")
        self.logger.info("=" * 60)
