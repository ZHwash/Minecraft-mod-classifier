#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 mod_rules.json 中的 reason 字段内容为空字符串"""

import json

# 加载规则文件
with open('config/mod_rules.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将所有规则的 reason 字段设置为空字符串
count = 0
for rule in data.get('rules', []):
    if 'reason' in rule:
        rule['reason'] = ''
        count += 1
    else:
        # 如果没有 reason 字段，添加一个空字符串
        rule['reason'] = ''
        count += 1

# 保存
with open('config/mod_rules.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已清理 {count} 条规则的 reason 字段内容')
