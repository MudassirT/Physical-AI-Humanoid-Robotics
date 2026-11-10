import os
import re
import ast
import json

chapters = [
    ('ai-book-docs/module10-hardware-architecture', [
        '10-1-humanoid-mechanical-design.mdx',
        '10-2-actuator-technologies.mdx',
        '10-3-power-electronics-and-motor-control.mdx',
        '10-4-communication-buses.mdx',
        '10-5-compute-platforms.mdx',
        '10-6-sensor-hardware.mdx',
        '10-7-real-time-embedded-software.mdx',
        '10-8-system-integration-and-testing.mdx'
    ]),
    ('ai-book-docs/module11-safety-ethics', [
        '11-1-robot-safety-standards.mdx',
        '11-2-functional-safety-architecture.mdx',
        '11-3-human-robot-interaction-safety.mdx',
        '11-4-ethics-of-autonomous-humanoids.mdx',
        '11-5-privacy-and-data-governance.mdx',
        '11-6-deployment-operations.mdx'
    ]),
    ('ai-book-docs/module12-capstone-frontiers', [
        '12-1-capstone-project-guide.mdx',
        '12-2-research-frontiers-locomotion.mdx',
        '12-3-research-frontiers-ai.mdx',
        '12-4-the-future-of-humanoid-robotics.mdx',
        '12-5-contributing-to-open-source.mdx',
        '12-6-reference-and-bibliography.mdx'
    ])
]

print("=== DEEP VERIFICATION OF M4 CHAPTERS ===")

math_issues = []
all_python_codes = []
all_cpp_codes = []
all_mermaid_diagrams = []

for mod_dir, files in chapters:
    for fname in files:
        fpath = os.path.join(mod_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Strip code blocks
        clean_text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

        # 2. Check $$ blocks
        # find all $$ ... $$
        double_dollar_count = len(re.findall(r'\$\$', clean_text))
        if double_dollar_count % 2 != 0:
            math_issues.append((fname, f"Unbalanced $$ delimiters: {double_dollar_count}"))

        # Remove $$ ... $$ before testing single $
        no_blocks = re.sub(r'\$\$.*?\$\$', '', clean_text, flags=re.DOTALL)

        # In KaTeX, single $ cannot span multiple paragraphs (newlines) typically,
        # but let's check single $ balance
        # Find single $ that are not escaped with \$
        single_dollars = []
        for m in re.finditer(r'(?<!\\)\$', no_blocks):
            single_dollars.append(m.start())
        if len(single_dollars) % 2 != 0:
            math_issues.append((fname, f"Unbalanced single $ delimiters: count={len(single_dollars)}"))

        # 3. Extract python blocks
        py_blocks = re.findall(r'```(?:python|py)\s*\n(.*?)```', content, re.DOTALL)
        for idx, pb in enumerate(py_blocks):
            all_python_codes.append((fname, idx+1, pb))

        # 4. Extract C++ blocks
        cpp_blocks = re.findall(r'```(?:cpp|c\+\+|c)\s*\n(.*?)```', content, re.DOTALL)
        for idx, cb in enumerate(cpp_blocks):
            all_cpp_codes.append((fname, idx+1, cb))

        # 5. Extract Mermaid blocks
        mm_blocks = re.findall(r'```mermaid\s*\n(.*?)```', content, re.DOTALL)
        for idx, mb in enumerate(mm_blocks):
            all_mermaid_diagrams.append((fname, idx+1, mb.strip()))

print(f"Math delimiter issues found: {len(math_issues)}")
for mi in math_issues:
    print(f"  {mi}")

print(f"\nExtracted {len(all_python_codes)} Python code blocks.")
print(f"Extracted {len(all_cpp_codes)} C++ code blocks.")
print(f"Extracted {len(all_mermaid_diagrams)} Mermaid diagrams.")
