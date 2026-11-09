import re

with open("ai-book-docs/module2-digital-twin/2-10-digital-twin-data-loop.mdx", "r", encoding="utf-8") as f:
    text = f.read()

# find all $$ ... $$
blocks = re.findall(r"\$\$(.*?)\$\$", text, re.DOTALL)
print(f"Total $$ blocks: {len(blocks)}")
for idx, b in enumerate(blocks):
    print(f"Block {idx}: length={len(b)}, content={repr(b.strip()[:50])}")

# Also check between consecutive $$
print("\nChecking raw text around $$:")
lines = text.splitlines()
for idx, line in enumerate(lines, 1):
    if "$$" in line:
        print(f"Line {idx}: {repr(line)}")
