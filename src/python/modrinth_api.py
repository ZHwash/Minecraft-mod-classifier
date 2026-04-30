#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modrinth API集成模块
通过Modrinth API查询Mod信息以辅助分类

优先级C: 规则数据库 > 配置文件标识 > Modrinth API检索
"""

import json
import re
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from logger import setup_logger

logger = setup_logger()


class ModrinthAPI:
    """Modrinth API客户端"""
    
    BASE_URL = "https://api.modrinth.com/v2"
    
    def __init__(self):
        self.logger = logger
    
    def search_project(self, query: str) -> Optional[Dict[str, Any]]:
        """
        搜索Modrinth项目
        
        Args:
            query: 搜索关键词（mod_id或mod_name）
            
        Returns:
            项目信息字典，如果未找到返回None
        """
        try:
            # URL编码查询参数
            encoded_query = query.replace(' ', '%20')
            url = f"{self.BASE_URL}/search?query={encoded_query}&limit=1"
            
            self.logger.debug(f"[Modrinth API] 搜索: {query}")
            
            # 发送请求
            req = Request(url)
            req.add_header('User-Agent', 'Minecraft-Mod-Classifier/2.0.0')
            
            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('hits') and len(data['hits']) > 0:
                    project = data['hits'][0]
                    self.logger.debug(f"[Modrinth API] 找到匹配: {project.get('title', 'Unknown')}")
                    return project
                else:
                    self.logger.debug(f"[Modrinth API] 未找到匹配: {query}")
                    return None
                    
        except HTTPError as e:
            self.logger.warning(f"[Modrinth API] HTTP错误 {e.code}: {query}")
            return None
        except URLError as e:
            self.logger.warning(f"[Modrinth API] 网络错误: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"[Modrinth API] 搜索失败: {str(e)}")
            return None
    
    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        通过项目ID获取详细信息
        
        Args:
            project_id: Modrinth项目ID
            
        Returns:
            项目详细信息字典，如果未找到返回None
        """
        try:
            url = f"{self.BASE_URL}/project/{project_id}"
            
            self.logger.debug(f"[Modrinth API] 获取项目详情: {project_id}")
            
            req = Request(url)
            req.add_header('User-Agent', 'Minecraft-Mod-Classifier/2.0.0')
            
            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data
                
        except HTTPError as e:
            self.logger.warning(f"[Modrinth API] HTTP错误 {e.code}: {project_id}")
            return None
        except URLError as e:
            self.logger.warning(f"[Modrinth API] 网络错误: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"[Modrinth API] 获取项目详情失败: {str(e)}")
            return None
    
    def infer_type_from_categories(self, categories: list) -> Optional[str]:
        """
        根据Modrinth的分类标签推断Mod类型
        
        Args:
            categories: 分类标签列表
            
        Returns:
            推断的Mod类型，如果无法判断返回None
        """
        if not categories:
            return None
        
        # 客户端专用标签（仅影响渲染/UI，不影响游戏逻辑）
        client_only_tags = [
            'optimization',  # 性能优化通常是客户端的（如Sodium）
        ]
        
        # 服务端专用标签
        server_only_tags = [
            'server-utility', 'administration'
        ]
        
        # 双端需要的标签（库、世界生成、内容添加等）
        both_sides_tags = [
            'library',      # 库文件通常双端都需要
            'worldgen',     # 世界生成需要服务端决定，客户端同步
            'adventure',    # 冒险内容需要双端同步
            'storage',      # 存储系统需要双端同步
            'technology',   # 科技类模组需要双端同步
            'magic',        # 魔法类模组需要双端同步
            'equipment',    # 装备类需要双端同步
            'food',         # 食物类需要双端同步
        ]
        
        # 检查是否包含各类标签
        has_client_only = any(tag in categories for tag in client_only_tags)
        has_server_only = any(tag in categories for tag in server_only_tags)
        has_both_sides = any(tag in categories for tag in both_sides_tags)
        
        # 优先判断：如果有明确的单端标签且没有双端标签
        if has_client_only and not has_both_sides and not has_server_only:
            return 'client_only'
        
        if has_server_only and not has_both_sides and not has_client_only:
            return 'server_only'
        
        # 如果有双端需要的标签，优先返回双端必装
        if has_both_sides:
            return 'client_and_server_required'
        
        # 如果同时有客户端和服务端标签
        if has_client_only and has_server_only:
            return 'client_and_server_required'
        
        # 默认情况下，大多数功能性mod需要双端同步
        # 除非明确标记为纯客户端优化
        if not has_client_only:
            return 'client_and_server_required'
        
        return None
    
    def normalize_search_term(self, term: str) -> str:
        """
        标准化搜索词：删除下划线、转换为小写、拆分驼峰命名
        
        Args:
            term: 原始搜索词
            
        Returns:
            标准化后的搜索词
        """
        # 转换为小写
        normalized = term.lower()
        
        # 删除下划线和连字符，用空格替换
        normalized = re.sub(r'[_\-]', ' ', normalized)
        
        # 在驼峰命名处插入空格（大写字母前）
        normalized = re.sub(r'([a-z])([A-Z])', r'\1 \2', normalized)
        
        # 去除多余空格
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    def search_mod_with_fallback(self, mod_name: str, mod_id: str) -> Optional[Dict[str, Any]]:
        """
        使用mod_name优先搜索，失败则使用mod_id
        
        Args:
            mod_name: Mod名称
            mod_id: Mod ID
            
        Returns:
            项目信息字典，如果都未找到返回None
        """
        result = None
        
        # 优先使用mod_name搜索
        if mod_name:
            # 标准化搜索词
            normalized_name = self.normalize_search_term(mod_name)
            self.logger.info(f"[Modrinth API] 使用mod_name搜索: {mod_name} -> {normalized_name}")
            result = self.search_project(normalized_name)
            
            if result:
                return result
        
        # 如果mod_name搜索失败，使用mod_id
        if mod_id:
            normalized_id = self.normalize_search_term(mod_id)
            self.logger.info(f"[Modrinth API] 使用mod_id搜索: {mod_id} -> {normalized_id}")
            result = self.search_project(normalized_id)
            
            if result:
                return result
        
        return None
    
    def classify_mod_via_api(self, mod_name: str, mod_id: str) -> Optional[str]:
        """
        通过Modrinth API分类Mod
        
        优先级策略：
        1. 直接使用API的client_side/server_side字段（最准确）
        2. 如果API未返回side信息，使用categories推断
        3. 最后从description关键词推断
        
        Args:
            mod_name: Mod名称
            mod_id: Mod ID
            
        Returns:
            分类类型，如果无法判断返回None
        """
        # 搜索项目
        project = self.search_mod_with_fallback(mod_name, mod_id)
        
        if not project:
            self.logger.debug(f"[Modrinth API] 无法通过API分类: {mod_name or mod_id}")
            return None
        
        # ===== 第一优先级：使用API的side字段 =====
        client_side = project.get('client_side', '').lower()
        server_side = project.get('server_side', '').lower()
        
        # 如果API提供了side信息，直接映射
        if client_side and server_side:
            self.logger.info(f"[Modrinth API] client_side={client_side}, server_side={server_side}")
            return self._map_side_to_type(client_side, server_side, project)
        
        # ===== 第二优先级：从categories推断 =====
        self.logger.warning(f"[Modrinth API] 未找到side信息，使用categories推断")
        categories = project.get('categories', [])
        inferred_type = self.infer_type_from_categories(categories)
        
        if inferred_type:
            self.logger.info(f"[Modrinth API] 基于分类推断类型: {inferred_type}")
            return inferred_type
        
        # ===== 第三优先级：从description推断 =====
        description = project.get('description', '').lower()
        
        client_keywords = ['client-side', 'client only', 'rendering', 'hud', 'minimap', 
                          'shader', 'optifine', 'sodium', 'iris', 'gui', 'ui']
        server_keywords = ['server-side', 'server only', 'backup', 'admin', 'management']
        
        has_client = any(keyword in description for keyword in client_keywords)
        has_server = any(keyword in description for keyword in server_keywords)
        
        if has_client and not has_server:
            return 'client_only'
        elif has_server and not has_client:
            return 'server_only'
        elif has_client and has_server:
            return 'client_and_server_required'
        
        self.logger.debug(f"[Modrinth API] 无法从API结果推断类型")
        return None
    
    def _map_side_to_type(self, client_side: str, server_side: str, project: dict) -> str:
        """
        将API的side字段映射为分类类型
        
        Args:
            client_side: 客户端侧标识 (required/optional/unsupported)
            server_side: 服务端侧标识 (required/optional/unsupported)
            project: 完整的项目信息字典
            
        Returns:
            分类类型
        """
        # 单端Mod：一端明确不支持
        if client_side == 'unsupported':
            return 'server_only'
        
        if server_side == 'unsupported':
            return 'client_only'
        
        # 双端Mod：根据required/optional组合判断
        side_map = {
            ('required', 'required'): 'client_and_server_required',
            ('required', 'optional'): 'client_required_server_optional',
            ('optional', 'required'): 'client_optional_server_required',
            ('optional', 'optional'): 'client_optional_server_optional',
        }
        
        return side_map.get((client_side, server_side), 'client_optional_server_optional')
