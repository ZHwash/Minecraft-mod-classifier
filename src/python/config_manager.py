#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责读取、保存和更新mods_data.json配置文件

配置结构升级：
- 支持多版本：通过version字段区分
- 支持多Mod端：通过loader字段区分（forge/fabric/neoforge）
- 唯一标识：name + version + loader
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from logger import setup_logger

logger = setup_logger()


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config/mods_data.json"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.mods_data: List[Dict[str, str]] = []
        self.logger = logger
    
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
                self.mods_data = json.load(f)
            
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
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
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
    
    def _generate_mod_key(self, name: str, version: str = "", loader: str = "") -> str:
        """
        生成Mod的唯一标识键
        
        Args:
            name: Mod名称
            version: 版本号
            loader: Mod加载器类型
            
        Returns:
            唯一标识键
        """
        key_parts = [name.lower()]
        if version:
            key_parts.append(version.lower())
        if loader:
            key_parts.append(loader.lower())
        return "|".join(key_parts)
    
    def find_mod(self, clean_name: str, version: str = "", loader: str = "") -> Optional[Dict[str, str]]:
        """
        查找Mod配置（支持版本和Mod端匹配）
        
        Args:
            clean_name: 清理后的Mod文件名（小写）
            version: 版本号（可选）
            loader: Mod加载器类型（可选）
            
        Returns:
            Mod配置字典，如果未找到返回None
        """
        target_key = self._generate_mod_key(clean_name, version, loader)
        
        # 首先尝试精确匹配（name + version + loader）
        for mod in self.mods_data:
            mod_key = self._generate_mod_key(
                mod.get('name', ''),
                mod.get('version', ''),
                mod.get('loader', '')
            )
            if mod_key == target_key:
                return mod
        
        # 如果没有版本和loader信息，尝试仅按名称匹配
        if not version and not loader:
            for mod in self.mods_data:
                if mod.get('name', '').lower() == clean_name.lower():
                    # 检查是否有更精确的匹配（有版本或loader）
                    # 如果有，优先使用无版本/无loader的记录
                    if not mod.get('version') and not mod.get('loader'):
                        return mod
        
        return None
    
    def add_mod(self, name: str, mod_type: str, version: str = "", loader: str = "") -> bool:
        """
        添加新的Mod配置
        
        Args:
            name: Mod名称
            mod_type: Mod类型
            version: 版本号（可选）
            loader: Mod加载器类型（可选）
            
        Returns:
            是否成功添加
        """
        # 检查是否已存在相同配置
        existing = self.find_mod(name, version, loader)
        if existing:
            self.logger.debug(f"Mod {name} (v{version}, {loader}) 已存在于配置中")
            return False
        
        new_mod = {
            'name': name,
            'type': mod_type
        }
        
        # 只在有值时添加version和loader字段
        if version:
            new_mod['version'] = version
        if loader:
            new_mod['loader'] = loader
        
        self.mods_data.append(new_mod)
        
        version_info = f" v{version}" if version else ""
        loader_info = f" [{loader.upper()}]" if loader else ""
        self.logger.info(f"添加新Mod配置: {name}{version_info}{loader_info} -> {mod_type}")
        return True
    
    def update_mod(self, name: str, mod_type: str, version: str = "", loader: str = "") -> bool:
        """
        更新Mod配置
        
        Args:
            name: Mod名称
            mod_type: 新的Mod类型
            version: 版本号（可选）
            loader: Mod加载器类型（可选）
            
        Returns:
            是否成功更新
        """
        target = self.find_mod(name, version, loader)
        if target:
            old_type = target['type']
            target['type'] = mod_type
            
            version_info = f" v{version}" if version else ""
            loader_info = f" [{loader.upper()}]" if loader else ""
            self.logger.info(f"更新Mod配置: {name}{version_info}{loader_info} ({old_type} -> {mod_type})")
            return True
        
        self.logger.warning(f"Mod {name} 不存在，无法更新")
        return False
    
    def get_mod_count(self) -> int:
        """获取配置中的Mod数量"""
        return len(self.mods_data)