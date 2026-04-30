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
        
        # 客户端专用标签
        client_only_tags = [
            'optimization', 'utility', 'library', 'fabric-api',
            'adventure', 'cursed', 'storage', 'worldgen'
        ]
        
        # 服务端专用标签
        server_only_tags = [
            'server-utility', 'administration'
        ]
        
        # 检查是否包含客户端专用标签
        has_client_tags = any(tag in categories for tag in client_only_tags)
        
        # 检查是否包含服务端专用标签
        has_server_tags = any(tag in categories for tag in server_only_tags)
        
        # 根据标签组合判断
        if has_client_tags and not has_server_tags:
            # 纯客户端优化/工具类
            if 'optimization' in categories or 'utility' in categories:
                return 'client_only'
        
        if has_server_tags and not has_client_tags:
            return 'server_only'
        
        # 如果有library标签，通常是两端都需要
        if 'library' in categories:
            return 'client_and_server_required'
        
        # 默认情况下，大多数内容mod需要双端同步
        if has_client_tags or has_server_tags:
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
        
        # 从categories推断类型
        categories = project.get('categories', [])
        inferred_type = self.infer_type_from_categories(categories)
        
        if inferred_type:
            self.logger.info(f"[Modrinth API] 基于分类推断类型: {inferred_type}")
            return inferred_type
        
        # 如果没有明确的分类标签，尝试从项目描述中推断
        description = project.get('description', '').lower()
        
        # 客户端特征关键词
        client_keywords = ['client-side', 'client only', 'rendering', 'hud', 'minimap', 
                          'shader', 'optifine', 'sodium', 'iris', 'gui', 'ui']
        
        # 服务端特征关键词
        server_keywords = ['server-side', 'server only', 'performance', 'optimization',
                          'backup', 'admin', 'management']
        
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
