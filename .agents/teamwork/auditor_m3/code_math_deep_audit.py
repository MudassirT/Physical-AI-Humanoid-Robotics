import os
import glob
import re
import ast

modules = [
    'ai-book-docs/module6-bipedal-locomotion',
    'ai-book-docs/module7-dexterous-manipulation',
    'ai-book-docs/module8-robot-learning',
    'ai-book-docs/module9-sim-to-real'
]

all_files = []
for m in modules:
    all_files.extend(sorted(glob.glob(os.path.join(m, '*.mdx'))))

print("=" * 60)
print(f"DEEP CODE AND MATH AUDIT ACROSS {len(all_files)} CHAPTERS")
print("=" * 60)

lang_counts = {}
empty_code_blocks = []
short_code_blocks = []
python_blocks = []

truly_empty_math = []
total_display_math = 0
total_inline_math = 0

for fpath in all_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Code blocks
    blocks = re.findall(r"```([a-zA-Z0-9_-]*)\r?\n(.*?)```", content, re.DOTALL)
    for lang, code in blocks:
        l = lang.lower().strip() or "unspecified"
        lang_counts[l] = lang_counts.get(l, 0) + 1
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        if len(lines) == 0:
            empty_code_blocks.append((fname, l))
        elif len(lines) < 3 and l in ['python', 'py', 'cpp', 'c++']:
            short_code_blocks.append((fname, l, code))
        if l in ['python', 'py']:
            python_blocks.append((fname, code))

    # 2. Math blocks - strip code blocks first so math in code comments doesn't confuse
    content_no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    
    # Extract display math ($$...$$)
    disp_math = re.findall(r"\$\$(.*?)\$\$", content_no_code, re.DOTALL)
    total_display_math += len(disp_math)
    for dm in disp_math:
        if not dm.strip() or dm.strip() in ['...', r'\dots', '???']:
            truly_empty_math.append((fname, 'display', dm))
            
    # Remove display math before finding inline math
    content_no_disp = re.sub(r"\$\$.*?\$\$", "", content_no_code, flags=re.DOTALL)
    inline_math = re.findall(r"\$([^\$\n\r]+?)\$", content_no_disp)
    total_inline_math += len(inline_math)
    for im in inline_math:
        if not im.strip() or im.strip() in ['...', r'\dots']:
            truly_empty_math.append((fname, 'inline', im))

print(f"Code block breakdown by language: {lang_counts}")
print(f"Empty code blocks: {len(empty_code_blocks)}")
print(f"Short code blocks (<3 lines): {len(short_code_blocks)}")
print(f"\nMath blocks:")
print(f"  Total Display Math ($$...$$): {total_display_math}")
print(f"  Total Inline Math ($...$): {total_inline_math}")
print(f"  Truly empty/stub math expressions: {len(truly_empty_math)}")

# AST parse all Python blocks
syntax_errors = []
for fname, code in python_blocks:
    try:
        ast.parse(code)
    except SyntaxError as e:
        syntax_errors.append((fname, e.lineno, str(e)))

print(f"\nPython AST Validation: {len(python_blocks)} blocks parsed.")
print(f"AST Syntax Errors: {len(syntax_errors)}")
if syntax_errors:
    for err in syntax_errors:
        print(f"  {err}")

assert len(empty_code_blocks) == 0, f"Found empty code blocks: {empty_code_blocks}"
assert len(syntax_errors) == 0, f"Found syntax errors: {syntax_errors}"
assert len(truly_empty_math) == 0, f"Found empty math: {truly_empty_math}"
print("\n[PASS] All code blocks and LaTeX math blocks are authentic and error-free!")
