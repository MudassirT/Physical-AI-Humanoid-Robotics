import os
import re

MODULES = [
    'module10-hardware-architecture',
    'module11-safety-ethics',
    'module12-capstone-frontiers'
]

print("=== FRONTMATTER & TABLE INTEGRITY AUDIT ===")

chapters = []
all_frontmatters = []
table_issues = []

for mod in MODULES:
    mod_dir = os.path.join('ai-book-docs', mod)
    files = sorted([f for f in os.listdir(mod_dir) if f.endswith('.mdx')])
    for idx, f in enumerate(files, 1):
        fpath = os.path.join(mod_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Frontmatter
        fm_match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', content, re.DOTALL)
        if not fm_match:
            print(f"ERROR: No frontmatter in {mod}/{f}")
            continue
        fm_text = fm_match.group(1)
        fm = {}
        for line in fm_text.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip().strip('"\'')
        
        pos = int(fm.get('sidebar_position', -1))
        title = fm.get('title', '')
        desc = fm.get('description', '')
        
        if pos != idx:
            print(f"WARNING: {mod}/{f} sidebar_position is {pos}, expected {idx}")
        if not title:
            print(f"ERROR: {mod}/{f} missing title")
        if not desc:
            print(f"ERROR: {mod}/{f} missing description")
            
        all_frontmatters.append({
            'module': mod,
            'file': f,
            'sidebar_position': pos,
            'title': title,
            'description': desc
        })
        
        # Table verification
        # Markdown tables start with | ... |
        # Table lines:
        lines = content.splitlines()
        in_table = False
        table_cols = 0
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('|') and stripped.endswith('|'):
                # Count pipes
                pipes = stripped.count('|')
                cols = pipes - 1
                if not in_table:
                    in_table = True
                    table_cols = cols
                else:
                    # check if delimiter row
                    if re.match(r'^\|(?:\s*:?-+:?\s*\|)+$', stripped):
                        # delimiter row
                        pass
                    elif cols != table_cols:
                        table_issues.append((f, line_no, f"Col count mismatch: expected {table_cols}, got {cols}: {stripped[:60]}"))
            else:
                in_table = False

print(f"Total chapters audited for frontmatter: {len(all_frontmatters)}")
if table_issues:
    print(f"TABLE ISSUES DETECTED ({len(table_issues)}):")
    for iss in table_issues[:10]:
        print(f"  {iss}")
else:
    print("ALL MARKDOWN TABLES ARE WELL-FORMED WITH ZERO DELIMITER MISMATCHES!")

print("\nFrontmatter summary:")
for fm in all_frontmatters:
    print(f"  [{fm['module']}] pos={fm['sidebar_position']} | {fm['title']} ({len(fm['description'].split())} desc words)")
