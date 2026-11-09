with open("ai-book-docs/module2-digital-twin/2-1-introduction-to-digital-twins.mdx", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_code = False
for idx, line in enumerate(lines, 1):
    if line.strip().startswith("```"):
        in_code = not in_code
        continue
    if in_code:
        continue
    dollars = line.count("$")
    if dollars > 0:
        print(f"L{idx} (count={dollars}): {line.strip()}")
