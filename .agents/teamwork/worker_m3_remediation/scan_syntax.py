import glob
import re

modules = ['module6-bipedal-locomotion', 'module7-dexterous-manipulation', 'module8-robot-learning', 'module9-sim-to-real']

valid_tags = {
    'ChapterProgress', 'QuizEngine', 'Admonition', 'Tabs', 'TabItem',
    'Details', 'summary', 'br', 'br/', 'span', 'div', 'p', 'b', 'i',
    'code', 'table', 'tr', 'td', 'th', 'thead', 'tbody', 'hr', 'hr/'
}

raw_lt_found = []
questionable_tags = []

for m in modules:
    for path in glob.glob(f'ai-book-docs/{m}/*.mdx'):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_code_block = False
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Check for '<'
            if '<' in line:
                # Remove math blocks $...$ and $$...$$
                line_no_math = re.sub(r'\$\$.*?\$\$', '', line)
                line_no_math = re.sub(r'\$.*?\$', '', line_no_math)
                # Raw '<' followed by space or number or symbol (not tag)
                if re.search(r'<(?![a-zA-Z\/!])', line_no_math):
                    raw_lt_found.append((path, line_no, stripped))
                # Check tags
                matches = re.findall(r'<([a-zA-Z0-9_\/!-]+)', line_no_math)
                for tag in matches:
                    clean_tag = tag.strip('/').split()[0]
                    if clean_tag and clean_tag not in valid_tags and not clean_tag.startswith('!--'):
                        questionable_tags.append((path, line_no, clean_tag, stripped))

print(f"Total raw '<' found: {len(raw_lt_found)}")
for p, l, s in raw_lt_found:
    print(f"RAW LT: {p}:{l} -> {s}")

print(f"\nTotal questionable tags found: {len(questionable_tags)}")
for p, l, t, s in questionable_tags:
    print(f"TAG <{t}>: {p}:{l} -> {s}")
