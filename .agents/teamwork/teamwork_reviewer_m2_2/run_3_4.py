import re
from pathlib import Path

txt = Path("ai-book-docs/module3-ai-robot-brain/3-4-nav2-for-bipedal-movement.mdx").read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", txt, re.DOTALL)
code = blocks[0]

print("Executing code from 3-4-nav2-for-bipedal-movement.mdx...")
exec(code, {"__name__": "__main__"})
print("Execution completed successfully!")
