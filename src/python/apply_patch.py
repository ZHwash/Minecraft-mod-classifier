#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用增量补丁到规则数据库
自动合并新增和更新的规则
"""

import json
import sys
from pathlib import Path


def apply_patch(patch_file: str, rules_file: str = "config/mod_rules.json"):
    """
    应用补丁到规则数据库
    
    Args:
        patch_file: 补丁文件路径
        rules_file: 规则数据库文件路径
    
    Returns:
        是否成功
    """
    patch_path = Path(patch_file)
    if not patch_path.exists():
        print(f"错误: 补丁文件 {patch_file} 不存在")
        return False
    
    rules_path = Path(rules_file)
    if not rules_path.exists():
        print(f"错误: 规则文件 {rules_file} 不存在")
        return False
    
    try:
        # 加载补丁
        with open(patch_path, 'r', encoding='utf-8') as f:
            patch_data = json.load(f)
        
        # 加载规则数据库
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
        
        # 构建规则索引
        rules_index = {}
        for i, rule in enumerate(rules_data.get('rules', [])):
            mod_id = rule.get('mod_id', '')
            if mod_id:
                rules_index[mod_id] = (i, rule)
        
        new_count = 0
        updated_count = 0
        
        # 处理新增规则
        for new_rule in patch_data.get('new_rules', []):
            mod_id = new_rule.get('mod_id', '')
            if mod_id and mod_id not in rules_index:
                rules_data['rules'].append(new_rule)
                rules_index[mod_id] = (len(rules_data['rules']) - 1, new_rule)
                new_count += 1
                print(f"  + 新增: {mod_id}")
        
        # 处理更新规则
        for update in patch_data.get('updated_rules', []):
            mod_id = update.get('mod_id', '')
            changes = update.get('changes', {})
            
            if mod_id in rules_index:
                idx, existing_rule = rules_index[mod_id]
                
                # 应用变更
                for field, change in changes.items():
                    old_value = change.get('old', '')
                    new_value = change.get('new', '')
                    existing_rule[field] = new_value
                
                updated_count += 1
                print(f"  ~ 更新: {mod_id} ({', '.join(changes.keys())})")
        
        # 保存更新后的规则数据库
        if new_count > 0 or updated_count > 0:
            with open(rules_path, 'w', encoding='utf-8') as f:
                json.dump(rules_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ 成功应用补丁!")
            print(f"  新增规则: {new_count} 条")
            print(f"  更新规则: {updated_count} 条")
            print(f"  总规则数: {len(rules_data['rules'])} 条")
            print(f"\n已保存到: {rules_file}")
            return True
        else:
            print("\n⚠ 补丁中没有需要应用的变更")
            return True
        
    except Exception as e:
        print(f"✗ 应用补丁失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python apply_patch.py <补丁文件>")
        print("示例: python apply_patch.py rule_update_patch_20260430.json")
        sys.exit(1)
    
    patch_file = sys.argv[1]
    success = apply_patch(patch_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
