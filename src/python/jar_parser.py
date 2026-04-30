#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JAR包配置文件解析器
从JAR文件中提取Mod元数据并判断类型

三层优先级判断（带验证机制）：
A. JAR配置文件标识 (side/environment字段) - 最高优先级
B. 规则数据库 (mod_rules.json) - 中等优先级
   - 如果规则的reason来自JAR配置 → 直接使用
   - 如果规则的reason来自API/手动 → 需要重新解析JAR验证（降级到优先级A）
C. Modrinth API检索 - 最低优先级
无法判断则归类为unknown，由用户手动确认

补充设定：
有些模组API返回的信息可能与实际不一致，因此添加保底措施：
规则配置中"reason"非读取JAR配置文件得到的需要重新读取JAR进行验证。
验证完毕后分类，最后同步信息修改至规则配置。
"""

import zipfile
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any
from logger import setup_logger
from rule_manager import RuleManager
from modrinth_api import ModrinthAPI

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
    
    def __init__(self, skip_rules: bool = False):
        self.logger = logger
        self.rule_manager = RuleManager()
        self.skip_rules = skip_rules  # 是否跳过规则数据库检查（用于强制重新分类）
        if not skip_rules:
            self.rule_manager.load_rules()  # 加载规则数据库
        self.modrinth_api = ModrinthAPI()  # 初始化Modrinth API客户端
    
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
        解析Fabric fabric.mod.json配置
        
        Args:
            zip_file: ZIP文件对象
            
        Returns:
            Mod信息字典
        """
        try:
            with zip_file.open(self.FABRIC_MOD_JSON) as f:
                data = json.loads(f.read().decode('utf-8'))
            
            mod_id = data.get('id', '')
            mod_name = data.get('name', '')
            version = data.get('version', '')
            
            # 优先级A: 读取environment字段 (内部会先检查优先级B)
            mod_type = self._infer_mod_type_from_fabric(data)
            
            mod_info = {
                'mod_id': mod_id,
                'mod_name': mod_name,
                'version': version,
                'loader': 'fabric',
                'type': mod_type
            }
            
            self.logger.debug(f"解析Fabric Mod: {mod_id} ({mod_name})")
            return mod_info
            
        except Exception as e:
            self.logger.error(f"解析fabric.mod.json失败: {str(e)}")
            return None
    
    def _parse_forge_mods_toml(self, zip_file: zipfile.ZipFile, toml_path: str = None) -> Optional[Dict[str, Any]]:
        """
        解析Forge/NeoForge mods.toml配置
        
        Args:
            zip_file: ZIP文件对象
            toml_path: TOML文件路径
            
        Returns:
            Mod信息字典
        """
        try:
            if toml_path is None:
                toml_path = self.FORGE_MODS_TOML_PATHS[0]
                
            with zip_file.open(toml_path) as f:
                content = f.read().decode('utf-8')
            
            # 从[[mods]]块中提取主modId(而不是从dependencies块中)
            mod_id = self._extract_main_mod_id(content)
            
            # 提取modName（displayName或modId）
            mod_name = self._extract_mod_name(content)
            
            # 提取版本号(从第一个version字段)
            version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
            
            # 判断是Forge还是NeoForge
            loader = 'neoforge' if 'neoforge.mods.toml' in toml_path else 'forge'
            
            # 优先级A: 读取dependencies中的side字段 (内部会先检查优先级B)
            mod_type = self._infer_mod_type_from_forge(content)
            
            mod_info = {
                'mod_id': mod_id,
                'mod_name': mod_name,
                'version': version_match.group(1) if version_match else '',
                'loader': loader,
                'type': mod_type
            }
            
            self.logger.debug(f"解析{loader.upper()} Mod: {mod_info['mod_id']} ({mod_info['mod_name']})")
            return mod_info
            
        except Exception as e:
            self.logger.error(f"解析mods.toml失败: {str(e)}")
            return None
    
    def _extract_main_mod_id(self, content: str) -> str:
        """
        从TOML内容中提取主modId(从[[mods]]块中)
        
        Args:
            content: TOML文件内容
            
        Returns:
            主modId,如果未找到返回空字符串
        """
        # 查找[[mods]]块
        mods_pattern = r'\[\[mods\]\](.*?)(?=\[\[|$)'
        mods_matches = re.findall(mods_pattern, content, re.DOTALL)
        
        # 从第一个[[mods]]块中提取modId
        for mod_block in mods_matches:
            mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', mod_block)
            if mod_id_match:
                return mod_id_match.group(1)
        
        # 如果没有找到[[mods]]块,尝试直接匹配(兼容旧格式)
        mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', content)
        return mod_id_match.group(1) if mod_id_match else ''
    
    def _extract_mod_name(self, content: str) -> str:
        """
        从TOML内容中提取mod名称
        
        Args:
            content: TOML文件内容
            
        Returns:
            mod名称，如果未找到则返回空字符串
        """
        # 优先使用displayName
        display_name_match = re.search(r'displayName\s*=\s*"([^"]+)"', content)
        if display_name_match:
            return display_name_match.group(1)
        
        # 其次使用modId作为fallback
        mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', content)
        if mod_id_match:
            return mod_id_match.group(1)
        
        return ''
    
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
                data = json.loads(f.read().decode('utf-8'))
            
            # mcmod.info可能是数组或对象
            if isinstance(data, list):
                data = data[0] if data else {}
            
            mod_id = data.get('modid', '')
            mod_name = data.get('name', '')
            version = data.get('version', '')
            
            # Legacy配置没有明确的类型标识，使用关键词匹配 (内部会先检查优先级B)
            mod_type = self._infer_mod_type_from_legacy(mod_id)
            
            mod_info = {
                'mod_id': mod_id,
                'mod_name': mod_name,
                'version': version,
                'loader': 'forge',
                'type': mod_type
            }
            
            self.logger.debug(f"解析Legacy Mod: {mod_id} ({mod_name})")
            return mod_info
            
        except Exception as e:
            self.logger.error(f"解析mcmod.info失败: {str(e)}")
            return None
    
    def _infer_mod_type_from_fabric(self, data: Dict) -> str:
        """
        从Fabric配置推断Mod类型（三层优先级）
        
        判断逻辑：
        1. 优先检查规则数据库（优先级A）
           - 如果规则已确认（confirmed=true）→ 直接使用
           - 如果规则未确认 → 需要验证（降级到优先级B）
        2. 读取environment字段（优先级B）
        3. 使用Modrinth API检索（优先级C）
        4. 无法判断则返回unknown
        """
        mod_id = data.get('id', '')
        mod_name = data.get('name', '')
        
        # 优先级A: 检查规则数据库（如果启用）
        if not self.skip_rules:
            rule = self.rule_manager.find_rule(mod_id)
            if rule:
                # 如果规则已确认，直接信任
                if rule.get('confirmed', False):
                    mod_type = rule.get('type')
                    self.logger.debug(f"[优先级A-已确认规则] {mod_id} -> {mod_type}")
                    return mod_type
                else:
                    # 未确认的规则，需要验证（降级到优先级B）
                    self.logger.debug(f"[优先级A-未确认规则] {mod_id}，将重新解析JAR验证")
        
        # 优先级B: 读取environment字段
        env = data.get('environment', '').lower()
        if env == 'client':
            return 'client_only'
        elif env == 'server':
            return 'server_only'
        elif env == '*':
            return 'client_and_server_required'
        
        # 优先级C: 使用Modrinth API检索
        api_type = self.modrinth_api.classify_mod_via_api(mod_name, mod_id)
        if api_type:
            return api_type
        
        # 无法判断，返回unknown
        return 'unknown'
    
    def _infer_mod_type_from_forge(self, content: str) -> str:
        """
        从Forge/NeoForge配置推断Mod类型（三层优先级）
        
        判断逻辑：
        1. 优先检查规则数据库（优先级A）
           - 如果规则已确认（confirmed=true）→ 直接使用
           - 如果规则未确认 → 需要验证（降级到优先级B）
        2. 检查核心依赖(minecraft/neoforge/forge/fabric)的side字段（优先级B-1）
           - 如果核心依赖中有任何一个是CLIENT → client_only
           - 如果核心依赖中有任何一个是SERVER → server_only
           - 如果核心依赖全是BOTH → client_and_server_required
        3. 如果核心依赖无法判断(如缺失),再检查其他业务依赖（优先级B-2）
        4. 使用Modrinth API检索（优先级C）
        5. 无法判断则返回unknown
        """
        # 提取modId用于规则匹配
        mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', content)
        if not mod_id_match:
            return 'unknown'
        
        mod_id = mod_id_match.group(1)
        
        # 提取modName用于辅助匹配
        mod_name = self._extract_mod_name(content)
        
        # 优先级A: 检查规则数据库（如果启用）
        if not self.skip_rules:
            rule = self.rule_manager.find_rule(mod_id)
            if rule:
                # 如果规则已确认，直接信任
                if rule.get('confirmed', False):
                    mod_type = rule.get('type')
                    self.logger.debug(f"[优先级A-已确认规则] {mod_id} -> {mod_type}")
                    return mod_type
                else:
                    # 未确认的规则，需要验证（降级到优先级B）
                    self.logger.debug(f"[优先级A-未确认规则] {mod_id}，将重新解析JAR验证")
        
        # 解析所有dependencies块
        # 注意: [[dependencies.XXX]]中的XXX是当前mod的ID，不是依赖的ID
        # 需要从每个块内的modId字段获取真正的依赖ID
        deps_pattern = r'\[\[dependencies\.[^\]]+\]\](.*?)(?=\[\[|$)'
        deps_matches = re.findall(deps_pattern, content, re.DOTALL)
        
        # 分类依赖项
        core_deps = []  # 核心依赖: minecraft, neoforge, forge, fabric
        other_deps = []  # 其他业务依赖
        
        for dep_content in deps_matches:
            # 从块内提取真正的依赖modId
            dep_mod_id_match = re.search(r'modId\s*=\s*"([^"]+)"', dep_content)
            side_match = re.search(r'side\s*=\s*"(\w+)"', dep_content)
            
            if dep_mod_id_match and side_match:
                dep_mod_id = dep_mod_id_match.group(1).lower()
                side = side_match.group(1).upper()
                
                # 判断是否为核心依赖
                if dep_mod_id in ['minecraft', 'neoforge', 'forge', 'fabric']:
                    core_deps.append(side)
                else:
                    other_deps.append(side)
        
        # 优先级B-1: 检查核心依赖的side字段
        if core_deps:
            # 如果核心依赖中有任何一个是CLIENT
            if any(side == 'CLIENT' for side in core_deps):
                return 'client_only'
            # 如果核心依赖中有任何一个是SERVER
            elif any(side == 'SERVER' for side in core_deps):
                return 'server_only'
            # 如果核心依赖全是BOTH
            elif all(side == 'BOTH' for side in core_deps):
                return 'client_and_server_required'
            # 核心依赖混合情况(如既有BOTH又有其他)，继续检查其他依赖
        
        # 优先级B-2: 检查其他业务依赖的side字段
        if other_deps:
            # 如果所有业务依赖都是CLIENT
            if all(side == 'CLIENT' for side in other_deps):
                return 'client_only'
            # 如果所有业务依赖都是SERVER
            elif all(side == 'SERVER' for side in other_deps):
                return 'server_only'
            # 如果所有业务依赖都是BOTH
            elif all(side == 'BOTH' for side in other_deps):
                return 'client_and_server_required'
            # 混合情况，无法判断
        
        # 优先级C: 使用Modrinth API检索
        api_type = self.modrinth_api.classify_mod_via_api(mod_name, mod_id)
        if api_type:
            return api_type
        
        # 无法判断，返回unknown
        return 'unknown'
    
    def _infer_mod_type_from_legacy(self, mod_id: str) -> str:
        """
        从Legacy配置推断Mod类型（三层优先级）
        
        判断逻辑：
        1. 优先检查规则数据库（优先级A）
           - 如果规则已确认（confirmed=true）→ 直接使用
           - 如果规则未确认 → 需要验证（降级到优先级C）
        2. 使用Modrinth API检索（优先级C）
        3. 无法判断则返回unknown
        """
        # 优先级A: 检查规则数据库（如果启用）
        if not self.skip_rules:
            rule = self.rule_manager.find_rule(mod_id)
            if rule:
                # 如果规则已确认，直接信任
                if rule.get('confirmed', False):
                    mod_type = rule.get('type')
                    self.logger.debug(f"[优先级A-已确认规则] {mod_id} -> {mod_type}")
                    return mod_type
                else:
                    # 未确认的规则，需要验证（降级到优先级C）
                    self.logger.debug(f"[优先级A-未确认规则] {mod_id}，将使用API验证")
        
        # 优先级C: 使用Modrinth API检索
        api_type = self.modrinth_api.classify_mod_via_api('', mod_id)
        if api_type:
            return api_type
        
        # Legacy配置没有明确的类型标识，返回unknown
        return 'unknown'
    
