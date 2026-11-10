import os
import re

MODULES = [
    'module10-hardware-architecture',
    'module11-safety-ethics',
    'module12-capstone-frontiers'
]

print("=== DEEP CODE BLOCK AUDIT ACROSS ALL 20 CHAPTERS ===")

total_code_blocks = 0
total_code_lines = 0

for mod in MODULES:
    mod_dir = os.path.join('ai-book-docs', mod)
    files = sorted([f for f in os.listdir(mod_dir) if f.endswith('.mdx')])
    print(f"\n--- {mod} ({len(files)} chapters) ---")
    for f in files:
        fpath = os.path.join(mod_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        cbs = re.findall(r'```([a-zA-Z0-9_\-\+]*)\r?\n(.*?)\r?\n```', content, re.DOTALL)
        total_code_blocks += len(cbs)
        
        cb_summaries = []
        for idx, (lang, code) in enumerate(cbs):
            lines = code.splitlines()
            total_code_lines += len(lines)
            
            # Check for dummy stubs: if code has < 3 lines or only print/pass
            non_empty = [l.strip() for l in lines if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('//')]
            is_trivial = False
            if len(non_empty) <= 2 and any(l in ['pass', 'return', '...'] for l in non_empty):
                is_trivial = True
            
            cb_summaries.append(f"#{idx+1}({lang or 'txt'}, {len(lines)}L{' [TRIVIAL]' if is_trivial else ''})")
            
            if is_trivial:
                print(f"  WARNING: Trivial block in {f} #{idx+1}: {code}")

        print(f"  {f}: {len(cbs)} blocks, {sum(len(c.splitlines()) for _, c in cbs)} lines | {', '.join(cb_summaries)}")

print(f"\nTotal code blocks: {total_code_blocks}")
print(f"Total code lines: {total_code_lines}")
