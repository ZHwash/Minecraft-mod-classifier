#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责读取、保存和更新mods_data.json配置文件

配置结构：
- mod_id: Mod的唯一标识符（必需）
- mod_name: Mod名称（可选）
- type: Mod类型（必需）
- reason: 分类原因说明（可选，默认为空字符串）
- 不再区分版本和加载器（运行位置通常不会改变）
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from logger import setup_logger
from file_utils import ensure_directory, get_resource_path

logger = setup_logger()


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config/mods_data.json"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        # 使用 get_resource_path 获取正确的文件路径
        self.config_path = get_resource_path(config_path)
        self.mods_data: List[Dict[str, str]] = []
        self.logger = logger
        
        # 如果是打包环境且配置文件不存在，尝试从 _internal 复制初始配置
        import sys
        if getattr(sys, 'frozen', False) and not self.config_path.exists():
            internal_config = Path(sys.executable).parent / '_internal' / config_path
            if internal_config.exists():
                try:
                    ensure_directory(self.config_path.parent)
                    shutil.copy2(internal_config, self.config_path)
                    self.logger.info(f"从 _internal 复制初始配置文件")
                except Exception as e:
                    self.logger.warning(f"复制初始配置文件失败: {str(e)}")
    
    def load_config(self) -> bool:
        """
        加载配置文件
        
        Returns:
            是否成功加载
        """
        if not self.config_path.exists():
            self.logger.warning(f"配置文件 {self.config_path} 不存在")
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 兼容旧版本配置，确保包含mod_name和reason字段
            self.mods_data = []
            for mod in data:
                simplified = {
                    'mod_id': mod.get('mod_id', ''),
                    'mod_name': mod.get('mod_name', ''),  # 新增字段，默认为空
                    'type': mod.get('type', 'unknown'),
                    'reason': mod.get('reason', '')  # 新增字段，默认为空
                }
                self.mods_data.append(simplified)
            
            self.logger.info(f"成功加载 {len(self.mods_data)} 条Mod配置")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON格式错误: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {str(e)}")
            return False
    
    def save_config(self) -> bool:
        """
        保存配置文件
        
        Returns:
            是否成功保存
        """
        try:
            # 确保目录存在
            ensure_directory(self.config_path.parent)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.mods_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"成功保存 {len(self.mods_data)} 条Mod配置")
            return True
            
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {str(e)}")
            return False
    
    def create_default_config(self) -> bool:
        """
        创建默认的空配置文件
        
        Returns:
            是否成功创建
        """
        try:
            self.mods_data = []
            return self.save_config()
        except Exception as e:
            self.logger.error(f"创建默认配置失败: {str(e)}")
            return False
    
    def find_mod(self, mod_id: str) -> Optional[Dict[str, str]]:
        """
        查找Mod配置（仅基于mod_id）
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            
        Returns:
            Mod配置字典，如果未找到返回None
        """
        for mod in self.mods_data:
            if mod.get('mod_id', '').lower() == mod_id.lower():
                return mod
        
        return None
    
    def add_mod(self, mod_id: str, mod_type: str, mod_name: str = '') -> bool:
        """
        添加新的Mod配置
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            mod_type: Mod类型
            mod_name: Mod名称（可选）
            
        Returns:
            是否成功添加
        """
        # 检查是否已存在相同配置
        existing = self.find_mod(mod_id)
        if existing:
            self.logger.debug(f"Mod {mod_id} 已存在于配置中")
            return False
        
        new_mod = {
            'mod_id': mod_id,
            'mod_name': mod_name,
            'type': mod_type,
            'reason': ''  # 初始化为空字符串，后续可填充
        }
        
        self.mods_data.append(new_mod)
        self.logger.info(f"添加新Mod配置: {mod_id} ({mod_name}) -> {mod_type}")
        return True
    
    def update_mod(self, mod_id: str, mod_type: str, mod_name: str = '') -> bool:
        """
        更新Mod配置
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            mod_type: 新的Mod类型
            mod_name: 新的Mod名称（可选）
            
        Returns:
            是否成功更新
        """
        target = self.find_mod(mod_id)
        if target:
            old_type = target['type']
            target['type'] = mod_type
            if mod_name:
                target['mod_name'] = mod_name
            # 确保 reason 字段存在
            if 'reason' not in target:
                target['reason'] = ''
            self.logger.info(f"更新Mod配置: {mod_id} ({old_type} -> {mod_type})")
            return True
        
        self.logger.warning(f"Mod {mod_id} 不存在，无法更新")
        return False
    
    def get_mod_count(self) -> int:
        """获取配置中的Mod数量"""
        return len(self.mods_data)