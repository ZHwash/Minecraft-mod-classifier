#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成规则数据库增量补丁
只包含新增和更新的规则，便于审查和合并
"""

import json
from pathlib import Path
from datetime import datetime
from file_utils import get_resource_path


def generate_incremental_patch(
    source_config: str = "config/mods_data.json",
    target_rules: str = "config/mod_rules.json",
    output_patch: str = None
):
    """
    生成增量补丁文件
    
    Args:
        source_config: 源配置文件路径（mods_data.json）
        target_rules: 目标规则文件路径（mod_rules.json）
        output_patch: 输出补丁文件路径（可选）
    
    Returns:
        补丁文件路径
    """
    # 使用 get_resource_path 获取正确的文件路径
    config_path = get_resource_path(source_config)
    if not config_path.exists():
        print(f"错误: 配置文件 {source_config} 不存在")
        print(f"   尝试路径: {config_path}")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    # 加载目标规则
    rules_path = get_resource_path(target_rules)
    if not rules_path.exists():
        print(f"错误: 规则文件 {target_rules} 不存在")
        print(f"   尝试路径: {rules_path}")
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
                'reason': ''  # reason字段留空，待后期填充
            })
        else:
            # 获取现有规则
            existing = rules_index[mod_id]
            
            # 检查是否为已确认配置，如果是则跳过
            if existing.get('confirmed', False):
                continue
            
            # 检查是否需要更新
            changes = {}
            
            # 检查mod_name
            if mod_name and (not existing.get('mod_name') or existing['mod_name'] != mod_name):
                changes['mod_name'] = {
                    'old': existing.get('mod_name', ''),
                    'new': mod_name
                }
            
            # 检查type
            if mod_type and existing.get('type') != mod_type:
                changes['type'] = {
                    'old': existing.get('type', ''),
                    'new': mod_type
                }
            
            # 检查reason（如果为空则填充）
            if not existing.get('reason') and mod_name:
                changes['reason'] = {
                    'old': '',
                    'new': f'通过JAR配置自动识别: {mod_name}'
                }
            
            if changes:
                updated_rules.append({
                    'mod_id': mod_id,
                    'changes': changes
                })
    
    # 如果没有变更，提示用户
    if not new_rules and not updated_rules:
        print("\n✓ 规则数据库已是最新，无需生成补丁")
        return None
    
    # 生成补丁文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if output_patch is None:
        output_patch = f"rule_update_patch_{timestamp}.json"
    
    patch_data = {
        "version": "2.0",
        "generated_at": datetime.now().isoformat(),
        "description": "Minecraft Mod Classifier 规则数据库增量更新补丁",
        "summary": {
            "total_changes": len(new_rules) + len(updated_rules),
            "new_rules": len(new_rules),
            "updated_rules": len(updated_rules)
        },
        "new_rules": new_rules,
        "updated_rules": updated_rules,
        "merge_instructions": [
            "如何合并此补丁：",
            "1. 将补丁文件放到项目根目录",
            "2. 运行: python src/python/apply_patch.py <补丁文件名>",
            "3. 检查合并结果",
            "4. 提交更新后的 config/mod_rules.json",
            "",
            "或者手动合并：",
            "- 新增规则：添加到 config/mod_rules.json 的 rules 数组末尾",
            "- 更新规则：找到对应的 mod_id，应用 changes 中的变更"
        ]
    }
    
    # 保存补丁文件
    with open(output_patch, 'w', encoding='utf-8') as f:
        json.dump(patch_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 成功生成增量补丁: {output_patch}")
    print(f"  新增规则: {len(new_rules)} 条")
    print(f"  更新规则: {len(updated_rules)} 条")
    print(f"  总计变更: {len(new_rules) + len(updated_rules)} 条")
    print(f"\n📤 如何提交更新：")
    print(f"  方法1（推荐 - 使用合并工具）：")
    print(f"    python src/python/apply_patch.py {output_patch}")
    print(f"\n  方法2（手动 - 通过GitHub Issue）：")
    print(f"    1. 打开 GitHub Issues")
    print(f"    2. 创建新Issue，标题：规则数据库更新 - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"    3. 将此JSON文件内容粘贴到Issue中")
    print(f"    4. 维护者会使用工具自动合并")
    
    return output_patch


if __name__ == "__main__":
    generate_incremental_patch()
