import os
import re

# Load diagrams from verify_m4_deep
from verify_m4_deep import all_mermaid_diagrams

print(f"Validating {len(all_mermaid_diagrams)} Mermaid diagrams...")

diagram_types = [
    'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
    'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'journey',
    'gantt', 'pie', 'gitGraph', 'C4Context', 'mindmap', 'timeline', 'quadrantChart'
]

errors = []

for fname, idx, diagram in all_mermaid_diagrams:
    lines = [l.strip() for l in diagram.split('\n') if l.strip() and not l.strip().startswith('%%')]
    if not lines:
        errors.append((fname, idx, "Empty mermaid diagram"))
        continue

    first_line = lines[0]
    # Check valid diagram header
    has_valid_header = any(first_line.startswith(dtype) for dtype in diagram_types)
    if not has_valid_header:
        errors.append((fname, idx, f"Unknown mermaid header: '{first_line}'"))

    # Check bracket pairing
    bracket_pairs = {
        '[': ']',
        '(': ')',
        '{': '}'
    }

    # Inspect line by line for obvious syntax hazards
    for line_num, line in enumerate(lines, 1):
        # Check quotes balance
        quote_count = line.count('"')
        if quote_count % 2 != 0:
            errors.append((fname, idx, f"Unbalanced double-quotes at line {line_num}: {line}"))

        # If line contains node definition without quotes, check for nested unquoted brackets
        # e.g. Node[Some (text)] without quotes around Some (text)
        # In mermaid: ID["label (with parens)"] is valid.
        # But ID[label (with parens)] can cause mermaid parser errors.
        unquoted_match = re.search(r'\w+\[([^"\]]*\([^\)]*\)[^"\]]*)\]', line)
        if unquoted_match:
            errors.append((fname, idx, f"Unquoted parens inside bracket label at line {line_num}: {line}"))

print(f"Mermaid validation completed. Errors found: {len(errors)}")
for err in errors:
    print("  ERROR:", err)
