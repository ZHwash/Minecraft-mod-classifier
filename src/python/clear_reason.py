#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清空规则数据库中所有规则的reason字段
"""

import json
from pathlib import Path

def clear_reason_field(rules_path: str = "config/mod_rules.json"):
    """清空所有规则的reason字段"""
    rules_file = Path(rules_path)
    
    if not rules_file.exists():
        print(f"错误: 规则文件 {rules_path} 不存在")
        return False
    
    try:
        # 读取规则文件
        with open(rules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rules = data.get('rules', [])
        cleared_count = 0
        
        # 清空所有规则的reason字段
        for rule in rules:
            if 'reason' in rule and rule['reason']:
                rule['reason'] = ''
                cleared_count += 1
        
        # 保存更新后的规则文件
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 成功清空 {cleared_count} 条规则的reason字段")
        print(f"  总规则数: {len(rules)}")
        return True
        
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        return False

if __name__ == "__main__":
    clear_reason_field()
