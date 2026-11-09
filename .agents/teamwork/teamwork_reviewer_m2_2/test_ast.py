import glob
import re
import ast
from pathlib import Path

def test_code_syntax(mod_dir):
    files = sorted(glob.glob(f"{mod_dir}/*.mdx"))
    print(f"\nChecking Python AST syntax in {mod_dir}:")
    for f in files:
        txt = Path(f).read_text(encoding="utf-8")
        blocks = re.findall(r"```python\n(.*?)```", txt, re.DOTALL)
        for idx, code in enumerate(blocks):
            try:
                ast.parse(code)
                print(f"  [PASS] {Path(f).name} block {idx+1}: valid Python AST ({len(code.splitlines())} lines)")
            except SyntaxError as e:
                print(f"  [FAIL] {Path(f).name} block {idx+1}: SyntaxError: {e}")
                raise

test_code_syntax("ai-book-docs/module3-ai-robot-brain")
test_code_syntax("ai-book-docs/module4-vla")
print("\nALL PYTHON CODE BLOCKS PASS SYNTAX PARSING!")
