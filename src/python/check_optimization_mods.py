from modrinth_api import ModrinthAPI

api = ModrinthAPI()
tests = ['distant horizons', 'krypton', 'modernfix', 'ferritecore', 'smooth boot', 'sodium', 'lithium']

print("Mod分类信息：")
print("="*100)
for t in tests:
    p = api.search_project(t)
    if p:
        print(f"{t:25} client={p.get('client_side'):12} server={p.get('server_side'):12}")
        print(f"  Categories: {p.get('categories', [])}")
        print(f"  Description: {p.get('description', '')[:100]}")
        print()
