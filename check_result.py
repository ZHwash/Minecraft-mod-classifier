import json

data = json.load(open('config/mod_rules.json', 'r', encoding='utf-8'))
tests = ['jei', 'sodium', 'create', 'distanthorizons', 'lithostitched']

print("更新后的分类结果：")
print("="*80)
for r in data['rules']:
    if r['mod_id'] in tests:
        print(f"{r['mod_id']:25} {r['type']:40} | {r.get('mod_name', '')}")
