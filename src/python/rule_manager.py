#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则管理模块
负责加载和管理mod_rules.json规则数据库

优先级B: 规则数据库 > 配置文件标识 > 关键词匹配
"""

import json
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
        查找Mod的分类规则
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            
        Returns:
            规则字典，如果未找到返回None
        """
        for rule in self.rules:
            if rule.get('mod_id', '').lower() == mod_id.lower():
                return rule
        
        return None
    
    def get_mod_type(self, mod_id: str) -> Optional[str]:
        """
        获取Mod的类型（基于规则数据库）
        
        Args:
            mod_id: Mod的唯一标识符(modId)
            
        Returns:
            Mod类型，如果未找到返回None
        """
        rule = self.find_rule(mod_id)
        if rule:
            mod_type = rule.get('type')
            reason = rule.get('reason', '')
            if reason:
                self.logger.debug(f"[规则匹配] {mod_id} -> {mod_type} (原因: {reason})")
            else:
                self.logger.debug(f"[规则匹配] {mod_id} -> {mod_type}")
            return mod_type
        
        return None
