with open('ai-book-docs/module10-hardware-architecture/10-1-humanoid-mechanical-design.mdx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'QuizEngine' in line:
        print(f"Line {idx+1}: {line}")
        for j in range(idx, min(len(lines), idx+30)):
            print(f"{j+1}: {lines[j]}", end='')
