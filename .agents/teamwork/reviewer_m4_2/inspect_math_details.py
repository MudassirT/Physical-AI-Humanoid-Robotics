import os
import re

files_to_inspect = [
    ("10-3-power-electronics-and-motor-control.mdx", "ai-book-docs/module10-hardware-architecture/10-3-power-electronics-and-motor-control.mdx"),
    ("10-7-real-time-embedded-software.mdx", "ai-book-docs/module10-hardware-architecture/10-7-real-time-embedded-software.mdx"),
    ("11-1-robot-safety-standards.mdx", "ai-book-docs/module11-safety-ethics/11-1-robot-safety-standards.mdx"),
    ("11-3-human-robot-interaction-safety.mdx", "ai-book-docs/module11-safety-ethics/11-3-human-robot-interaction-safety.mdx"),
    ("12-2-research-frontiers-locomotion.mdx", "ai-book-docs/module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx"),
    ("12-3-research-frontiers-ai.mdx", "ai-book-docs/module12-capstone-frontiers/12-3-research-frontiers-ai.mdx")
]

for label, path in files_to_inspect:
    print(f"\n==========================================")
    print(f"FILE: {label}")
    print(f"==========================================")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    blocks = re.findall(r'\$\$(.*?)\$\$', text, re.DOTALL)
    print(f"Total $$ math blocks: {len(blocks)}")
    for i, b in enumerate(blocks[:4]):
        clean_b = "\n".join("  " + line for line in b.strip().split("\n"))
        print(f"Formula {i+1}:\n{clean_b}")
