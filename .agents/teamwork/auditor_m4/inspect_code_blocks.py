import re

def inspect_file(filepath):
    print(f"=== INSPECTING {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    code_blocks = re.findall(r'```([a-zA-Z0-9_\-\+]*)\r?\n(.*?)\r?\n```', content, re.DOTALL)
    for i, (lang, code) in enumerate(code_blocks):
        if 'pass' in code or '...' in code or 'TODO' in code or 'NotImplemented' in code:
            print(f"\n--- Code block #{i+1} ({lang}, {len(code.splitlines())} lines) ---")
            for line_no, line in enumerate(code.splitlines(), 1):
                if any(k in line for k in ['pass', '...', 'TODO', 'NotImplemented']):
                    print(f"  Line {line_no}: {line}")
            print("\nFull code block:")
            print(code)

inspect_file('ai-book-docs/module11-safety-ethics/11-6-deployment-operations.mdx')
inspect_file('ai-book-docs/module12-capstone-frontiers/12-1-capstone-project-guide.mdx')
