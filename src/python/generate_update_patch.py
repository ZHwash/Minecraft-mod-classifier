#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成规则数据库更新补丁
让用户可以无需任何技术知识就能贡献规则更新
"""

import json
from pathlib import Path
from datetime import datetime


def generate_update_patch(
    source_config: str = "config/mods_data.json",
    target_rules: str = "config/mod_rules.json",
    output_patch: str = None
):
    """
    生成规则数据库更新补丁文件
    
    Args:
        source_config: 源配置文件路径（mods_data.json）
        target_rules: 目标规则文件路径（mod_rules.json）
        output_patch: 输出补丁文件路径（可选）
    
    Returns:
        补丁文件路径
    """
    # 加载源配置
    config_path = Path(source_config)
    if not config_path.exists():
        print(f"错误: 配置文件 {source_config} 不存在")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    # 加载目标规则
    rules_path = Path(target_rules)
    if not rules_path.exists():
        print(f"错误: 规则文件 {target_rules} 不存在")
        return None
    
    with open(rules_path, 'r', encoding='utf-8') as f:
        rules_data = json.load(f)
    
    # 构建规则索引
    rules_index = {}
    for rule in rules_data.get('rules', []):
        mod_id = rule.get('mod_id', '')
        if mod_id:
            rules_index[mod_id] = rule
    
    # 找出需要新增或更新的规则
    new_rules = []
    updated_rules = []
    
    for mod_config in config_data:
        mod_id = mod_config.get('mod_id', '')
        mod_name = mod_config.get('mod_name', '')
        mod_type = mod_config.get('type', 'unknown')
        
        if not mod_id:
            continue
        
        if mod_id not in rules_index:
            # 新规则
            new_rules.append({
                'mod_id': mod_id,
                'mod_name': mod_name,
                'type': mod_type,
                'reason': f'通过JAR配置自动识别: {mod_name}'
            })
        else:
            # 检查是否需要更新
            existing = rules_index[mod_id]
            needs_update = False
            
            # 检查mod_name
            if mod_name and (not existing.get('mod_name') or existing['mod_name'] != mod_name):
                needs_update = True
            
            # 检查type
            if mod_type and existing.get('type') != mod_type:
                needs_update = True
            
            # 检查reason
            if not existing.get('reason'):
                needs_update = True
            
            if needs_update:
                updated_rule = {
                    'mod_id': mod_id,
                    'changes': {}
                }
                
                if mod_name and (not existing.get('mod_name') or existing['mod_name'] != mod_name):
                    updated_rule['changes']['mod_name'] = {
                        'old': existing.get('mod_name', ''),
                        'new': mod_name
                    }
                
                if mod_type and existing.get('type') != mod_type:
                    updated_rule['changes']['type'] = {
                        'old': existing.get('type', ''),
                        'new': mod_type
                    }
                
                if not existing.get('reason'):
                    updated_rule['changes']['reason'] = {
                        'old': '',
                        'new': f'通过JAR配置自动识别: {mod_name}'
                    }
                
                updated_rules.append(updated_rule)
    
    # 生成补丁文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if output_patch is None:
        output_patch = f"rule_update_patch_{timestamp}.json"
    
    patch_data = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "description": "Minecraft Mod Classifier 规则数据库更新补丁",
        "summary": {
            "total_changes": len(new_rules) + len(updated_rules),
            "new_rules": len(new_rules),
            "updated_rules": len(updated_rules)
        },
        "new_rules": new_rules,
        "updated_rules": updated_rules,
        "instructions": [
            "如何将此补丁应用到规则数据库：",
            "1. 打开 https://github.com/ZHwash/Minecraft-mod-classifier",
            "2. 点击 'Issues' 标签",
            "3. 点击 'New Issue' 按钮",
            "4. 标题填写：规则数据库更新 - {日期}",
            "5. 将此JSON文件的内容粘贴到Issue内容中",
            "6. 提交Issue即可",
            "",
            "或者：",
            "1. 在GitHub上Fork此仓库",
            "2. 将新规则添加到 config/mod_rules.json",
            "3. 创建Pull Request"
        ]
    }
    
    # 保存补丁文件
    with open(output_patch, 'w', encoding='utf-8') as f:
        json.dump(patch_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 成功生成更新补丁: {output_patch}")
    print(f"  新增规则: {len(new_rules)} 条")
    print(f"  更新规则: {len(updated_rules)} 条")
    print(f"  总计变更: {len(new_rules) + len(updated_rules)} 条")
    print(f"\n📤 如何提交更新：")
    print(f"  方法1（最简单）：")
    print(f"    1. 打开 GitHub Issues: https://github.com/ZHwash/Minecraft-mod-classifier/issues")
    print(f"    2. 点击 'New Issue'")
    print(f"    3. 将此文件内容粘贴进去并提交")
    print(f"\n  方法2（推荐开发者）：")
    print(f"    1. Fork 仓库")
    print(f"    2. 应用补丁到 config/mod_rules.json")
    print(f"    3. 创建 Pull Request")
    
    return output_patch


if __name__ == "__main__":
    generate_update_patch()
