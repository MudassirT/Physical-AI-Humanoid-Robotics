import re
from pathlib import Path

txt = Path("ai-book-docs/module4-vla/4-3-cognitive-planning-with-llms.mdx").read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", txt, re.DOTALL)
code = blocks[0]

print("Executing code from 4-3-cognitive-planning-with-llms.mdx...")
exec(code, {"__name__": "__main__"})
print("Execution completed successfully!")
