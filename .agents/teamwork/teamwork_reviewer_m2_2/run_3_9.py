import re
from pathlib import Path

txt = Path("ai-book-docs/module3-ai-robot-brain/3-9-multi-sensor-fusion.mdx").read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", txt, re.DOTALL)
print(f"Found {len(blocks)} python blocks in 3-9.")

for i, code in enumerate(blocks):
    print(f"\n--- Testing Block {i+1} ---")
    try:
        exec(code, {"__name__": "__main__"})
        print(f"Block {i+1} ran successfully!")
    except Exception as e:
        print(f"Block {i+1} raised: {type(e).__name__}: {e}")
