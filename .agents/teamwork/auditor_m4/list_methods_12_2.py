with open('ai-book-docs/module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx', 'r', encoding='utf-8') as f:
    c = f.read()

import re
cbs = re.findall(r'```python\r?\n(.*?)\r?\n```', c, re.DOTALL)
for i, cb in enumerate(cbs):
    print(f"Code block {i+1}:")
    for line in cb.splitlines():
        if line.startswith('class ') or line.startswith('def '):
            print(" ", line)
