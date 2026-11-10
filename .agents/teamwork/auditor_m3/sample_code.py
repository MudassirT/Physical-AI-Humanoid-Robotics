import os
import glob
import re

modules = [
    'ai-book-docs/module6-bipedal-locomotion',
    'ai-book-docs/module7-dexterous-manipulation',
    'ai-book-docs/module8-robot-learning',
    'ai-book-docs/module9-sim-to-real'
]

print("=" * 60)
print("SAMPLING REAL PYTHON IMPLEMENTATIONS IN M6-M9")
print("=" * 60)

for m in modules:
    print(f"\n--- MODULE: {os.path.basename(m)} ---")
    files = sorted(glob.glob(os.path.join(m, '*.mdx')))
    # Pick 2 files per module to display snippets
    sample_files = [files[1], files[3]]
    for sf in sample_files:
        print(f"\nFile: {os.path.basename(sf)}")
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()
        py_blocks = re.findall(r"```python\r?\n(.*?)```", content, re.DOTALL)
        for i, code in enumerate(py_blocks):
            lines = code.strip().splitlines()
            print(f"  Code block {i+1} ({len(lines)} lines):")
            # Print first 10 lines
            for l in lines[:10]:
                print(f"    {l}")
            if len(lines) > 10:
                print("    ...")
            # Print last 5 lines
            for l in lines[-5:]:
                print(f"    {l}")
