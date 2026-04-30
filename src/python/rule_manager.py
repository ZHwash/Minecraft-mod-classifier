#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则管理模块
负责加载和管理mod_rules.json规则数据库

优先级A: 规则数据库 > 配置文件标识 > Modrinth API检索
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from logger import setup_logger

logger = setup_logger()


class RuleManager:
    """规则管理器"""
    
    def __init__(self, rules_path: str = "config/mod_rules.json"):
        """
        初始化规则管理器
        
        Args:
            rules_path: 规则文件路径
        """
        self.rules_path = Path(rules_path)
        self.rules: List[Dict] = []
        self.logger = logger
    
    def load_rules(self) -> bool:
        """
        加载规则文件
        
        Returns:
            是否成功加载
        """
        if not self.rules_path.exists():
            self.logger.warning(f"规则文件 {self.rules_path} 不存在，使用空规则集")
            return False
        
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.rules = data.get('rules', [])
            self.logger.info(f"成功加载 {len(self.rules)} 条Mod分类规则")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"规则文件JSON格式错误: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"加载规则文件失败: {str(e)}")
            return False
    
    def find_rule(self, mod_id: str) -> Optional[Dict]:
        """
        查找Mod的分类规则（基于mod_id精确匹配）
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            
        Returns:
            规则字典，如果未找到返回None
        """
        for rule in self.rules:
            if rule.get('mod_id', '').lower() == mod_id.lower():
                return rule
        
        return None
    
    def find_rule_by_name(self, mod_name: str) -> Optional[Dict]:
        """
        通过mod_name查找规则（支持模糊匹配）
        
        Args:
            mod_name: Mod名称
            
        Returns:
            规则字典，如果未找到返回None
        """
        if not mod_name:
            return None
        
        # 标准化搜索词
        normalized_name = self._normalize_term(mod_name)
        
        for rule in self.rules:
            rule_name = rule.get('mod_name', '')
            if not rule_name:
                continue
            
            # 标准化规则中的名称
            normalized_rule_name = self._normalize_term(rule_name)
            
            # 精确匹配
            if normalized_name == normalized_rule_name:
                return rule
            
            # 包含匹配
            if normalized_name in normalized_rule_name or normalized_rule_name in normalized_name:
                return rule
        
        return None
    
    def _normalize_term(self, term: str) -> str:
        """
        标准化术语：删除下划线、转换为小写、拆分驼峰命名
        
        Args:
            term: 原始术语
            
        Returns:
            标准化后的术语
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
    
    def get_mod_type(self, mod_id: str, mod_name: str = '') -> Optional[str]:
        """
        获取Mod的类型（基于规则数据库）
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            mod_name: Mod名称（可选，用于辅助匹配）
            
        Returns:
            Mod类型，如果未找到返回None
        """
        # 优先使用mod_id精确匹配
        rule = self.find_rule(mod_id)
        if rule:
            mod_type = rule.get('type')
            reason = rule.get('reason', '')
            if reason:
                self.logger.debug(f"[规则匹配] {mod_id} -> {mod_type} (原因: {reason})")
            else:
                self.logger.debug(f"[规则匹配] {mod_id} -> {mod_type}")
            return mod_type
        
        # 如果mod_id未找到，尝试使用mod_name模糊匹配
        if mod_name:
            rule = self.find_rule_by_name(mod_name)
            if rule:
                mod_type = rule.get('type')
                matched_id = rule.get('mod_id', '')
                self.logger.debug(f"[规则匹配-by-name] {mod_name} -> {mod_type} (匹配到: {matched_id})")
                return mod_type
        
        return None
