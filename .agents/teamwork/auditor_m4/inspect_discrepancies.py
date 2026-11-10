import re

def show_code(path, pattern, max_lines=40):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    cb = re.findall(r'```python\r?\n(.*?)\r?\n```', c, re.DOTALL)[0]
    match = re.search(pattern, cb)
    if match:
        start = match.start()
        lines = cb[start:].splitlines()[:max_lines]
        print(f"=== {path} ({pattern}) ===")
        for idx, l in enumerate(lines):
            print(f"{idx+1}: {l}")

show_code('ai-book-docs/module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx', r'def compute_landing_forces')
show_code('ai-book-docs/module12-capstone-frontiers/12-4-the-future-of-humanoid-robotics.mdx', r'def project_required_data_hours')
show_code('ai-book-docs/module12-capstone-frontiers/12-6-reference-and-bibliography.mdx', r'def parse_and_insert_bibtex')
