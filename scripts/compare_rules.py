#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""比对 rules.json 和 mod_rules.json 的分类差异"""

import json
import os
from collections import defaultdict

def normalize_mod_id(name):
    """统一命名规范：转换为小写，空格和特殊字符替换为下划线"""
    # 去除 .jar 后缀
    name = name.replace('.jar', '')
    # 转换为小写
    name = name.lower()
    # 将空格、连字符等特殊字符替换为下划线
    import re
    name = re.sub(r'[^a-z0-9_]', '_', name)
    # 去除多余的下划线
    name = re.sub(r'_+', '_', name)
    # 去除首尾下划线
    name = name.strip('_')
    return name

def load_rules_json(filepath):
    """加载 rules.json (数组格式)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 转换为 {mod_id: type} 字典
    rules = {}
    for item in data:
        # 支持两种格式：旧格式使用 name，新格式使用 mod_id
        mod_id_raw = item.get('mod_id', '') or item.get('name', '')
        mod_type = item.get('type', '')
        
        if mod_id_raw and mod_type:
            # 如果是文件名格式（带.jar），需要转换
            if mod_id_raw.endswith('.jar'):
                mod_id = normalize_mod_id(mod_id_raw)
            else:
                # 已经是 mod_id 格式，直接转小写
                mod_id = mod_id_raw.lower()
            
            rules[mod_id] = mod_type
    
    return rules

def load_mod_rules_json(filepath):
    """加载 mod_rules.json (对象格式，使用 mod_id 字段)"""
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

def compare_rules(rules1, rules2):
    """比对两个规则集的差异"""
    differences = []
    only_in_rules1 = []
    only_in_rules2 = []
    
    all_keys = set(list(rules1.keys()) + list(rules2.keys()))
    
    for key in sorted(all_keys):
        in_rules1 = key in rules1
        in_rules2 = key in rules2
        
        if in_rules1 and in_rules2:
            type1 = rules1[key]
            type2_info = rules2[key]
            type2 = type2_info['type']
            confirmed = type2_info['confirmed']
            
            # 跳过已确认的条目
            if confirmed:
                continue
            
            # 类型不同才记录
            if type1 != type2:
                differences.append({
                    'mod_id': key,
                    'rules_json': type1,
                    'mod_rules_json': type2,
                    'confirmed': confirmed
                })
        elif in_rules1 and not in_rules2:
            only_in_rules1.append(key)
        elif not in_rules1 and in_rules2:
            only_in_rules2.append(key)
    
    return differences, only_in_rules1, only_in_rules2

def main():
    rules_path = r'H:\code\Minecraft-mod-classifier\rules.json'
    mod_rules_path = r'H:\code\Minecraft-mod-classifier\config\mod_rules.json'
    
    print("=" * 80)
    print("开始比对 rules.json 和 mod_rules.json")
    print("=" * 80)
    print()
    
    # 加载数据
    rules1 = load_rules_json(rules_path)
    rules2 = load_mod_rules_json(mod_rules_path)
    
    print(f"rules.json 条目数: {len(rules1)}")
    print(f"mod_rules.json 条目数: {len(rules2)}")
    print()
    
    # 比对
    differences, only_in_1, only_in_2 = compare_rules(rules1, rules2)
    
    # 输出差异
    print("=" * 80)
    print(f"【分类差异】共 {len(differences)} 个模组分类不一致:")
    print("=" * 80)
    
    if differences:
        for i, diff in enumerate(differences, 1):
            confirmed_mark = " [已锁死]" if diff['confirmed'] else ""
            print(f"{i}. {diff['mod_id']}")
            print(f"   rules.json:         {diff['rules_json']}")
            print(f"   mod_rules.json:     {diff['mod_rules_json']}{confirmed_mark}")
            print()
    else:
        print("无差异")
        print()
    
    # 输出只在 rules.json 中的
    print("=" * 80)
    print(f"【仅在 rules.json 中】共 {len(only_in_1)} 个模组:")
    print("=" * 80)
    if only_in_1:
        for i, mod_id in enumerate(only_in_1[:50], 1):  # 只显示前50个
            print(f"{i}. {mod_id}: {rules1[mod_id]}")
        if len(only_in_1) > 50:
            print(f"... 还有 {len(only_in_1) - 50} 个未显示")
    else:
        print("无")
    print()
    
    # 输出只在 mod_rules.json 中的
    print("=" * 80)
    print(f"【仅在 mod_rules.json 中】共 {len(only_in_2)} 个模组:")
    print("=" * 80)
    if only_in_2:
        for i, mod_id in enumerate(only_in_2[:50], 1):  # 只显示前50个
            type_info = rules2[mod_id]
            confirmed_mark = " [已锁死]" if type_info['confirmed'] else ""
            print(f"{i}. {mod_id}: {type_info['type']}{confirmed_mark}")
        if len(only_in_2) > 50:
            print(f"... 还有 {len(only_in_2) - 50} 个未显示")
    else:
        print("无")
    print()
    
    # 统计信息
    print("=" * 80)
    print("【统计摘要】")
    print("=" * 80)
    print(f"共同模组数: {len(rules1) + len(rules2) - len(only_in_1) - len(only_in_2)}")
    print(f"分类一致数: {len(rules1) + len(rules2) - len(only_in_1) - len(only_in_2) - len(differences)}")
    print(f"分类差异数: {len(differences)}")
    print(f"仅 rules.json: {len(only_in_1)}")
    print(f"仅 mod_rules.json: {len(only_in_2)}")
    print("=" * 80)

if __name__ == '__main__':
    main()
