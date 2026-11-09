import glob
import re
from pathlib import Path

def inspect_code_blocks(mod_dir):
    files = sorted(glob.glob(f"{mod_dir}/*.mdx"))
    print(f"\n=== Inspecting Code Blocks in {mod_dir} ===")
    for f in files:
        txt = Path(f).read_text(encoding="utf-8")
        blocks = re.findall(r"```([a-zA-Z0-9_-]+)?\n(.*?)```", txt, re.DOTALL)
        print(f"\nFile: {Path(f).name} (Total blocks: {len(blocks)})")
        for idx, (lang, code) in enumerate(blocks):
            lines = code.strip().splitlines()
            first_few = lines[0] if lines else "EMPTY"
            print(f"  Block {idx+1} [{lang}]: {len(lines)} lines | Starts with: {first_few[:60]}")
            # Check for dummy / facade patterns
            if "TODO" in code or "pass" == code.strip() or "NotImplemented" in code:
                print(f"    WARNING: Potential placeholder in {Path(f).name} block {idx+1}")

inspect_code_blocks("ai-book-docs/module3-ai-robot-brain")
inspect_code_blocks("ai-book-docs/module4-vla")
