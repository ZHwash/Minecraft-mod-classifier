#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成分类差异报告 - 排除已修改的模组"""

import json

def normalize_mod_id(name):
    """统一命名规范：转换为小写，空格和特殊字符替换为下划线"""
    name = name.replace('.jar', '')
    name = name.lower()
    import re
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

def main():
    rules_path = r'H:\code\Minecraft-mod-classifier\rules.json'
    mod_rules_path = r'H:\code\Minecraft-mod-classifier\config\mod_rules.json'
    
    # 加载数据
    rules1 = load_rules_json(rules_path)
    rules2 = load_mod_rules_json(mod_rules_path)
    
    # 找出所有差异（排除已确认的）
    differences = []
    all_keys = set(list(rules1.keys()) + list(rules2.keys()))
    
    for key in sorted(all_keys):
        if key in rules1 and key in rules2:
            type1 = rules1[key]
            type2_info = rules2[key]
            type2 = type2_info['type']
            confirmed = type2_info['confirmed']
            
            # 跳过已确认的条目
            if confirmed:
                continue
            
            if type1 != type2:
                differences.append({
                    'mod_id': key,
                    'rules_json': type1,
                    'mod_rules_json': type2,
                    'confirmed': confirmed
                })
    
    remaining_diffs = differences  # 已经排除了 confirmed 的条目
    
    # 生成报告
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("Minecraft Mod 分类差异报告")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append(f"总差异数（排除已确认）: {len(remaining_diffs)}")
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("剩余分类差异列表")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # 按类型分组统计
    type_changes = {}
    for diff in remaining_diffs:
        change_key = f"{diff['rules_json']} → {diff['mod_rules_json']}"
        if change_key not in type_changes:
            type_changes[change_key] = []
        type_changes[change_key].append(diff['mod_id'])
    
    report_lines.append("【变更类型统计】")
    report_lines.append("-" * 80)
    for change_type, mods in sorted(type_changes.items()):
        report_lines.append(f"\n{change_type}: {len(mods)} 个模组")
        for mod_id in sorted(mods)[:10]:  # 只显示前10个
            report_lines.append(f"  - {mod_id}")
        if len(mods) > 10:
            report_lines.append(f"  ... 还有 {len(mods) - 10} 个")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("【详细差异列表】")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    for i, diff in enumerate(remaining_diffs, 1):
        confirmed_mark = " [已锁死]" if diff['confirmed'] else ""
        report_lines.append(f"{i}. {diff['mod_id']}{confirmed_mark}")
        report_lines.append(f"   rules.json (网上资料):     {diff['rules_json']}")
        report_lines.append(f"   mod_rules.json (你的配置): {diff['mod_rules_json']}")
        report_lines.append("")
    
    # 写入文件
    output_path = r'H:\code\Minecraft-mod-classifier\classification_differences.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"报告已生成: {output_path}")
    print(f"剩余差异数: {len(remaining_diffs)}")

if __name__ == '__main__':
    main()
