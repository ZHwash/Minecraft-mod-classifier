#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""找出 reason 为空且 mod_name 与 mod_id 差异很大的条目"""

import json
import re

def is_similar(mod_id, mod_name):
    """判断 mod_id 和 mod_name 是否相似
    
    相似的定义：
    1. mod_name 是 mod_id 的首字母缩写
    2. mod_name 是 mod_id 去除下划线/连字符/空格后的连写（忽略大小写）
    3. mod_id 是 mod_name 的一部分（连续子串，忽略大小写和分隔符）
    4. mod_id 和 mod_name 由相同的单词组成（拆词重组，不区分大小写和顺序）
    """
    if not mod_name:
        return True  # 空值认为是相似的
    
    mod_id_lower = mod_id.lower()
    mod_name_lower = mod_name.lower()
    
    # 规则1：检查是否是首字母缩写
    # 提取 mod_name 中每个单词的首字母
    name_words = mod_name.split()
    if name_words:
        initials = ''.join([word[0] for word in name_words if word]).lower()
        # 如果首字母组合等于 mod_id（去除下划线后），认为是缩写
        id_no_underscore = mod_id_lower.replace('_', '')
        if initials == id_no_underscore:
            return True
    
    # 规则2：检查是否是去除分隔符后的连写
    # 将 mod_name 中的空格、连字符等分隔符去除
    name_compact = re.sub(r'[^a-z0-9]', '', mod_name_lower)
    # 将 mod_id 中的下划线去除
    id_compact = mod_id_lower.replace('_', '')
    
    if name_compact == id_compact:
        return True
    
    # 规则3：检查 mod_id 是否是 mod_name 的一部分（连续子串）
    # 将 mod_name 转换为纯字母数字形式
    name_alnum = re.sub(r'[^a-z0-9]', '', mod_name_lower)
    id_alnum = re.sub(r'[^a-z0-9]', '', mod_id_lower)
    
    if id_alnum and id_alnum in name_alnum:
        return True
    
    # 规则4：检查是否是拆词重组（相同的单词，不同顺序）
    # 将 mod_id 按下划线分割，然后进一步将每个部分按数字/字母边界分割
    id_parts = []
    for part in mod_id_lower.split('_'):
        # 将连续的数字和字母分开，例如 'skinlayers3d' -> ['skinlayers', '3d']
        sub_parts = re.findall(r'[a-z]+|[0-9]+', part)
        id_parts.extend(sub_parts)
    id_words_set = set(id_parts)
    
    # 将 mod_name 按空格、连字符等非字母数字字符分割成单词
    name_words_list = re.findall(r'[a-z0-9]+', mod_name_lower)
    name_words_set = set(name_words_list)
    
    # 如果两个集合相等，说明是相同的单词重组
    if id_words_set and name_words_set and id_words_set == name_words_set:
        return True
    
    # 规则5：检查 mod_id 的所有字母部分是否都在 mod_name 中
    # 提取 mod_id 中的所有纯字母部分
    id_alpha_parts = [part for part in id_parts if part.isalpha()]
    if id_alpha_parts:
        # 检查每个字母部分是否在 mod_name 的某个单词中
        all_found = True
        for alpha_part in id_alpha_parts:
            found = False
            for name_word in name_words_list:
                if alpha_part in name_word or name_word in alpha_part:
                    found = True
                    break
            if not found:
                all_found = False
                break
        
        if all_found:
            return True
    
    # 额外检查：mod_id 是否直接包含在 mod_name 中（或反之）
    if mod_id_lower in mod_name_lower or mod_name_lower in mod_id_lower:
        return True
    
    return False

def main():
    config_path = r'H:\code\Minecraft-mod-classifier\config\mod_rules.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rules = data.get('rules', [])
    
    # 找出 reason 为空且 mod_name 与 mod_id 差异很大的条目
    candidates = []
    
    for i, rule in enumerate(rules):
        mod_id = rule.get('mod_id', '')
        mod_name = rule.get('mod_name', '')
        reason = rule.get('reason', '')
        
        # 只处理 reason 为空的
        if reason != '':
            continue
        
        # 如果 mod_name 为空，跳过
        if not mod_name:
            continue
        
        # 检查是否相似
        if not is_similar(mod_id, mod_name):
            candidates.append({
                'index': i,
                'mod_id': mod_id,
                'mod_name': mod_name,
                'type': rule.get('type', '')
            })
    
    print(f"找到 {len(candidates)} 个候选条目：")
    print("=" * 80)
    
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. mod_id: {candidate['mod_id']}")
        print(f"   mod_name: {candidate['mod_name']}")
        print(f"   type: {candidate['type']}")
        print()
    
    # 生成修改建议
    print("\n" + "=" * 80)
    print("建议修改列表（将这些条目的 mod_name 改为空字符串）：")
    print("=" * 80)
    
    modifications = []
    for candidate in candidates:
        modifications.append({
            'mod_id': candidate['mod_id'],
            'old_name': candidate['mod_name']
        })
    
    # 显示前20个
    for i, mod in enumerate(modifications[:20], 1):
        print(f"{i}. {mod['mod_id']}: '{mod['old_name']}' → ''")
    
    if len(modifications) > 20:
        print(f"... 还有 {len(modifications) - 20} 个")
    
    # 询问是否执行修改
    print("\n" + "=" * 80)
    response = input("是否执行修改？(y/n): ").strip().lower()
    
    if response == 'y':
        # 执行修改
        for candidate in candidates:
            idx = candidate['index']
            rules[idx]['mod_name'] = ''
        
        # 保存文件
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n已修改 {len(candidates)} 个条目的 mod_name 为空字符串")
    else:
        print("\n已取消修改")

if __name__ == '__main__':
    main()
