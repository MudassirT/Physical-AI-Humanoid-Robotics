import os
import json

for mod in ['module10-hardware-architecture', 'module11-safety-ethics', 'module12-capstone-frontiers']:
    p = os.path.join('ai-book-docs', mod, '_category_.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            print(f"{mod}/_category_.json:")
            print(json.dumps(json.load(f), indent=2))
    else:
        print(f"MISSING: {p}")
