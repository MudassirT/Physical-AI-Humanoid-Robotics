import re

with open('ai-book-docs/module12-capstone-frontiers/12-1-capstone-project-guide.mdx', 'r', encoding='utf-8') as f:
    content = f.read()

cbs = re.findall(r'```python\r?\n(.*?)\r?\n```', content, re.DOTALL)
for i, cb in enumerate(cbs):
    print(f"--- Code block {i+1} ---")
    for idx, line in enumerate(cb.splitlines()[:60]):
        print(f"{idx+1}: {line}")
