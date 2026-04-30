#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据网上资料修正分类差异"""

import json
import re

def normalize_mod_id(name):
    """统一命名规范"""
    name = name.replace('.jar', '')
    name = name.lower()
    name = re.sub(r'[^a-z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name

def load_rules_json(filepath):
    """加载 rules.json"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rules = {}
    for item in data:
        mod_id_raw = item.get('mod_id', '') or item.get('name', '')
        mod_type = item.get('type', '')
        
        if mod_id_raw and mod_type:
            if mod_id_raw.endswith('.jar'):
                mod_id = normalize_mod_id(mod_id_raw)
            else:
                mod_id = mod_id_raw.lower()
            
            rules[mod_id] = mod_type
    
    return rules

def load_mod_rules_json(filepath):
    """加载 mod_rules.json"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rules = {}
    for item in data.get('rules', []):
        mod_id = item.get('mod_id', '')
        mod_type = item.get('type', '')
        confirmed = item.get('confirmed', False)
        if mod_id and mod_type:
            rules[mod_id.lower()] = {
                'type': mod_type,
                'confirmed': confirmed
            }
    
    return rules

def is_major_difference(type1, type2):
    """判断是否是重大差异
    
    重大差异：完全不同的类型（如 client_only vs server_only）
    轻微差异：四个可选类型之间的差异
    """
    # 定义四个可选类型
    optional_types = {
        'client_and_server_required',
        'client_optional_server_optional',
        'client_optional_server_required',
        'client_required_server_optional'
    }
    
    # 如果两个都是可选类型，则是轻微差异
    if type1 in optional_types and type2 in optional_types:
        return False
    
    # 否则是重大差异
    return True

def main():
    rules_path = r'H:\code\Minecraft-mod-classifier\rules.json'
    mod_rules_path = r'H:\code\Minecraft-mod-classifier\config\mod_rules.json'
    
    # 加载数据
    rules1 = load_rules_json(rules_path)  # 网上资料
    rules2 = load_mod_rules_json(mod_rules_path)  # 你的配置
    
    print("=" * 80)
    print("开始修正分类差异")
    print("=" * 80)
    print()
    
    # 找出所有差异（排除已确认的）
    modifications = []
    
    for key in sorted(rules1.keys()):
        if key not in rules2:
            continue
        
        type1 = rules1[key]  # 网上资料
        type2_info = rules2[key]
        type2 = type2_info['type']
        confirmed = type2_info['confirmed']
        
        # 跳过已确认的
        if confirmed:
            continue
        
        # 跳过相同的
        if type1 == type2:
            continue
        
        # 判断差异程度
        major_diff = is_major_difference(type1, type2)
        
        modifications.append({
            'mod_id': key,
            'online_type': type1,
            'current_type': type2,
            'major_diff': major_diff
        })
    
    print(f"找到 {len(modifications)} 个需要修正的差异")
    print()
    
    # 统计
    major_count = sum(1 for m in modifications if m['major_diff'])
    minor_count = len(modifications) - major_count
    
    print(f"重大差异: {major_count} 个（将添加锁死）")
    print(f"轻微差异: {minor_count} 个（不添加锁死）")
    print()
    
    # 询问是否执行
    response = input("是否执行修改？(y/n): ").strip().lower()
    
    if response != 'y':
        print("已取消")
        return
    
    # 加载完整配置
    with open(mod_rules_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    rules_list = config_data.get('rules', [])
    
    # 执行修改
    modified_count = 0
    for mod in modifications:
        mod_id = mod['mod_id']
        online_type = mod['online_type']
        major_diff = mod['major_diff']
        
        # 查找对应的规则
        for rule in rules_list:
            if rule.get('mod_id', '').lower() == mod_id:
                # 修改 type
                old_type = rule.get('type', '')
                rule['type'] = online_type
                
                # 如果是重大差异，添加锁死
                if major_diff:
                    rule['confirmed'] = True
                    rule['reason'] = f"根据网上资料修正（重大差异）: {old_type} → {online_type}"
                else:
                    # 轻微差异，不锁死，但更新 reason
                    if not rule.get('reason'):
                        rule['reason'] = f"根据网上资料修正（轻微差异）: {old_type} → {online_type}"
                
                modified_count += 1
                break
    
    # 保存文件
    with open(mod_rules_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n已修正 {modified_count} 个模组的分类")
    print(f"其中 {major_count} 个已添加锁死")
    print(f"其中 {minor_count} 个未添加锁死")

if __name__ == '__main__':
    main()
