with open('ai-book-docs/module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx', 'r', encoding='utf-8') as f:
    c = f.read()

import re
cb = re.findall(r'```python\r?\n(.*?)\r?\n```', c, re.DOTALL)[0]
for idx, line in enumerate(cb.splitlines()):
    print(f"{idx+1}: {line}")
