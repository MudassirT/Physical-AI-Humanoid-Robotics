import re
from pathlib import Path

txt = Path("ai-book-docs/module4-vla/4-4-multimodal-interaction.mdx").read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", txt, re.DOTALL)
code = blocks[0]

print("Executing code from 4-4-multimodal-interaction.mdx...")
exec(code, {"__name__": "__main__"})
print("Execution completed successfully!")
