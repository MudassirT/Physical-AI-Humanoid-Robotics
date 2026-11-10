import glob
import re

modules = ['module6-bipedal-locomotion', 'module7-dexterous-manipulation', 'module8-robot-learning', 'module9-sim-to-real']

table_pipes = []

for m in modules:
    for path in glob.glob(f'ai-book-docs/{m}/*.mdx'):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_code = False
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            
            # Check if line looks like a table row: starts and ends with '|'
            if stripped.startswith('|') and stripped.endswith('|'):
                # Check if there is an unescaped pipe inside inline math
                # Find all $...$
                math_spans = re.findall(r'\$([^\$\n]+)\$', line)
                # But wait, if an unescaped pipe is present, standard regex might not match across cell boundaries!
                # Let's count unescaped pipes on the line
                # In a table row, if a cell has an unescaped pipe, the row will have more cells than the header row!
                pass

# Let's check table consistency: compare header column count with all row column counts in each table!
inconsistencies = []
for m in modules:
    for path in glob.glob(f'ai-book-docs/{m}/*.mdx'):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_code = False
        in_table = False
        header_cols = 0
        table_start_line = 0
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            
            if stripped.startswith('|') and stripped.endswith('|'):
                # Split by unescaped pipe (lookbehind not backslash)
                # Note: in regex, (?<!\\)\|
                cols = re.split(r'(?<!\\)\|', stripped)
                col_count = len(cols) - 2 # front and back are empty
                if not in_table:
                    in_table = True
                    header_cols = col_count
                    table_start_line = line_no
                else:
                    # Ignore separator row (|---|---|)
                    if re.match(r'^\|[\s\-:]+(\|[\s\-:]+)*\|$', stripped):
                        continue
                    if col_count != header_cols:
                        inconsistencies.append((path, line_no, col_count, header_cols, stripped))
            else:
                in_table = False

print(f"Table column count inconsistencies found: {len(inconsistencies)}")
for p, l, c, h, s in inconsistencies:
    print(f"{p}:{l} (cols: {c}, expected: {h}) -> {s}")
