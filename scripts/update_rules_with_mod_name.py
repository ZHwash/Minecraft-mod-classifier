#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新mod_rules.json脚本
为现有规则添加mod_name字段（暂时为空）
"""

import json
from pathlib import Path


def add_mod_name_field(rules_path: str = "config/mod_rules.json"):
    """为mod_rules.json中的所有规则添加mod_name字段"""
    
    rules_file = Path(rules_path)
    
    if not rules_file.exists():
        print(f"文件不存在: {rules_file}")
        return False
    
    try:
        # 读取文件
        with open(rules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rules = data.get('rules', [])
        updated_count = 0
        
        # 为每个规则添加mod_name字段
        for rule in rules:
            if 'mod_name' not in rule:
                rule['mod_name'] = ''  # 暂时为空
                updated_count += 1
        
        # 保存文件
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 成功为 {updated_count} 条规则添加mod_name字段")
        print(f"总规则数: {len(rules)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新失败: {str(e)}")
        return False


if __name__ == "__main__":
    print("正在更新 mod_rules.json...")
    add_mod_name_field()
    print("\n完成！")
