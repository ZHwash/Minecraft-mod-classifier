#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JAR包配置文件解析器
从JAR文件中提取Mod元数据并判断类型
"""

import zipfile
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any
from logger import setup_logger

logger = setup_logger()


class JarParser:
    """JAR包配置文件解析器"""
    
    # Fabric Mod 配置文件路径
    FABRIC_MOD_JSON = "fabric.mod.json"
    
    # Forge/NeoForge Mod 配置文件路径（支持多种格式）
    FORGE_MODS_TOML_PATHS = [
        "META-INF/mods.toml",          # 标准Forge
        "META-INF/neoforge.mods.toml", # NeoForge
    ]
    MC_MOD_INFO = "mcmod.info"
    
    def __init__(self):
        self.logger = logger
    
    def parse_jar(self, jar_path: Path) -> Optional[Dict[str, Any]]:
        """
        解析JAR文件，提取Mod信息
        
        Args:
            jar_path: JAR文件路径
            
        Returns:
            包含Mod信息的字典，如果解析失败返回None
        """
        try:
            with zipfile.ZipFile(jar_path, 'r') as zip_file:
                file_list = zip_file.namelist()
                
                # 尝试解析Fabric配置
                if self.FABRIC_MOD_JSON in file_list:
                    return self._parse_fabric_mod(zip_file)
                
                # 尝试解析Forge/NeoForge配置（支持多种路径）
                for toml_path in self.FORGE_MODS_TOML_PATHS:
                    if toml_path in file_list:
                        return self._parse_forge_mods_toml(zip_file, toml_path)
                
                # 尝试解析旧版mcmod.info
                if self.MC_MOD_INFO in file_list:
                    return self._parse_mcmod_info(zip_file)
                
                self.logger.warning(f"未在 {jar_path.name} 中找到标准的Mod配置文件")
                return None
                
        except zipfile.BadZipFile:
            self.logger.error(f"{jar_path.name} 不是有效的ZIP/JAR文件")
            return None
        except Exception as e:
            self.logger.error(f"解析 {jar_path.name} 时出错: {str(e)}")
            return None
    
    def _parse_fabric_mod(self, zip_file: zipfile.ZipFile) -> Optional[Dict[str, Any]]:
        """
        解析Fabric Mod配置
        
        Args:
            zip_file: ZIP文件对象
            
        Returns:
            Mod信息字典
        """
        try:
            with zip_file.open(self.FABRIC_MOD_JSON) as f:
                data = json.load(f)
            
            mod_info = {
                'name': data.get('id', ''),
                'version': data.get('version', ''),
                'loader': 'fabric',  # Fabric Mod
                'type': self._infer_mod_type_from_fabric(data)
            }
            
            self.logger.debug(f"解析Fabric Mod: {mod_info['name']}")
            return mod_info
            
        except Exception as e:
            self.logger.error(f"解析fabric.mod.json失败: {str(e)}")
            return None
    
    def _parse_forge_mods_toml(self, zip_file: zipfile.ZipFile, toml_path: str = None) -> Optional[Dict[str, Any]]:
        """
        解析Forge/NeoForge mods.toml配置（简化版，仅提取基本信息）
        
        Args:
            zip_file: ZIP文件对象
            toml_path: TOML文件路径（默认为标准Forge路径）
            
        Returns:
            Mod信息字典
        """
        try:
            if toml_path is None:
                toml_path = self.FORGE_MODS_TOML_PATHS[0]
                
            with zip_file.open(toml_path) as f:
                content = f.read().decode('utf-8')
            
            # 简单的TOML解析（实际项目中建议使用toml库）
            mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', content)
            version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
            
            # 判断是Forge还是NeoForge
            loader = 'neoforge' if 'neoforge.mods.toml' in toml_path else 'forge'
            
            mod_info = {
                'name': mod_id_match.group(1) if mod_id_match else '',
                'version': version_match.group(1) if version_match else '',
                'loader': loader,
                'type': self._infer_mod_type_from_forge(content)
            }
            
            self.logger.debug(f"解析{loader.upper()} Mod: {mod_info['name']}")
            return mod_info
            
        except Exception as e:
            self.logger.error(f"解析mods.toml失败: {str(e)}")
            return None
    
    def _parse_mcmod_info(self, zip_file: zipfile.ZipFile) -> Optional[Dict[str, Any]]:
        """
        解析旧版mcmod.info配置
        
        Args:
            zip_file: ZIP文件对象
            
        Returns:
            Mod信息字典
        """
        try:
            with zip_file.open(self.MC_MOD_INFO) as f:
                data = json.load(f)
            
            # mcmod.info可能是数组或对象
            if isinstance(data, list):
                data = data[0] if data else {}
            
            mod_info = {
                'name': data.get('modid', ''),
                'version': data.get('version', ''),
                'type': self._infer_mod_type_from_legacy(data)
            }
            
            self.logger.debug(f"解析Legacy Mod: {mod_info['name']}")
            return mod_info
            
        except Exception as e:
            self.logger.error(f"解析mcmod.info失败: {str(e)}")
            return None
    
    def _infer_mod_type_from_fabric(self, data: Dict) -> str:
        """
        从Fabric配置推断Mod类型
        
        判断逻辑：
        - 检查depends和suggests字段
        - 如果有服务端相关依赖，可能是服务端Mod
        - 如果只有客户端相关依赖，是客户端Mod
        """
        depends = data.get('depends', {})
        suggests = data.get('suggests', {})
        
        # 常见的服务端API
        server_apis = {'fabric-api', 'fabric', 'server'}
        # 常见的客户端API
        client_apis = {'fabric-renderer', 'cloth-config', 'modmenu'}
        
        has_server_dep = any(api in depends for api in server_apis)
        has_client_dep = any(api in depends for api in client_apis)
        
        # 根据依赖关系推断类型
        if has_client_dep and not has_server_dep:
            return 'client_only'
        elif has_server_dep and not has_client_dep:
            return 'client_optional_server_required'
        else:
            # 默认认为两端都需要
            return 'client_and_server_required'
    
    def _infer_mod_type_from_forge(self, content: str) -> str:
        """
        从Forge/NeoForge配置推断Mod类型
        
        判断逻辑：
        1. 如果有明确的side字段，直接使用
        2. 根据modId和描述关键词推断
        3. 默认策略：客户端需装，服务端可选（更保守的选择）
        """
        # 1. 查找side字段
        side_match = re.search(r'side\s*=\s*"(\w+)"', content)
        
        if side_match:
            side = side_match.group(1).lower()
            if side == 'client':
                return 'client_only'
            elif side == 'server':
                return 'client_optional_server_required'
            else:
                return 'client_and_server_required'
        
        # 2. 提取modId进行关键词匹配
        mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', content)
        if mod_id_match:
            mod_id = mod_id_match.group(1).lower()
            
            # 明显的客户端Mod关键词
            client_keywords = [
                'jei', 'rei', 'emi',          # 物品管理器
                'journeymap', 'xaero', 'minimap',  # 小地图
                'appleskin', 'hud', 'overlay',     # HUD覆盖层
                'mouse', 'keybind', 'control',     # 控制相关
                'shader', 'optifine', 'iris', 'sodium',  # 渲染优化
                'dynamiccrosshair', 'crosshair',     # 准星
                'searchable', 'search',              # 搜索功能
            ]
            
            # 明显的服务端Mod关键词
            server_keywords = [
                'backup', 'performance', 'optimization',
                'world', 'chunk', 'generation',
            ]
            
            # 检查是否包含客户端关键词
            if any(keyword in mod_id for keyword in client_keywords):
                return 'client_required_server_optional'
            
            # 检查是否包含服务端关键词
            if any(keyword in mod_id for keyword in server_keywords):
                return 'client_optional_server_required'
        
        # 3. 默认策略：客户端需装，服务端可选
        # （比两端都需要更保守，避免不必要的服务端安装）
        return 'client_required_server_optional'
    
    def _infer_mod_type_from_legacy(self, data: Dict) -> str:
        """
        从旧版配置推断Mod类型
        """
        # 旧版配置通常没有明确的类型标识
        # 默认返回需要两端的类型
        return 'client_and_server_required'
