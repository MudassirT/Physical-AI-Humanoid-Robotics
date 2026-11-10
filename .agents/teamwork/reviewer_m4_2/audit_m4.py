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

print("AUDITING FRONTMATTER, COMPONENTS, CODE, AND MATH...")
total_chapters = 0
total_python_blocks = 0
total_cpp_blocks = 0
total_rust_blocks = 0
total_bash_blocks = 0
py_syntax_errors = []
np_trapz_warnings = []
mermaid_blocks = []
unclosed_fences = []
math_delimiter_warnings = []
word_counts = {}

for mod_dir, files in chapters:
    cat_path = os.path.join(mod_dir, '_category_.json')
    if not os.path.exists(cat_path):
        print(f"ERROR: missing _category_.json in {mod_dir}")
    else:
        with open(cat_path, 'r', encoding='utf-8') as f:
            try:
                cat_data = json.load(f)
                print(f"Directory: {mod_dir} -> Category: '{cat_data.get('label')}' (position: {cat_data.get('position')})")
            except Exception as e:
                print(f"ERROR in {cat_path}: {e}")

    for fname in files:
        total_chapters += 1
        path = os.path.join(mod_dir, fname)
        if not os.path.exists(path):
            print(f"ERROR: Missing file {path}")
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        words = len(content.split())
        word_counts[fname] = words

        # Check frontmatter
        if not content.startswith('---'):
            print(f"ERROR: {fname} missing frontmatter delimiter")
        fm_match = re.match(r'^---\r?\n(.*?)\r?\n---', content, re.DOTALL)
        if not fm_match:
            print(f"ERROR: {fname} malformed frontmatter")
        else:
            fm_text = fm_match.group(1)
            if 'title:' not in fm_text or 'sidebar_position:' not in fm_text:
                print(f"ERROR: {fname} missing title or sidebar_position in frontmatter")

        # Check components
        has_cp = '<ChapterProgress' in content
        has_qe = '<QuizEngine' in content
        if not has_cp:
            print(f"WARNING: {fname} missing <ChapterProgress />")
        if not has_qe:
            print(f"WARNING: {fname} missing <QuizEngine />")

        # Check code fence balance
        fences = re.findall(r'^```', content, flags=re.MULTILINE)
        if len(fences) % 2 != 0:
            unclosed_fences.append((fname, len(fences)))

        # Python blocks
        py_matches = re.findall(r'```(?:python|py)\s*\n(.*?)```', content, re.DOTALL)
        for i, code in enumerate(py_matches):
            total_python_blocks += 1
            if 'np.trapz' in code:
                np_trapz_warnings.append((fname, f"block {i+1} has np.trapz"))
            try:
                ast.parse(code)
            except SyntaxError as e:
                py_syntax_errors.append((fname, f"block {i+1}: {e}"))

        # C++ blocks
        cpp_matches = re.findall(r'```(?:cpp|c\+\+|c)\s*\n(.*?)```', content, re.DOTALL)
        total_cpp_blocks += len(cpp_matches)

        # Rust blocks
        rust_matches = re.findall(r'```(?:rust)\s*\n(.*?)```', content, re.DOTALL)
        total_rust_blocks += len(rust_matches)

        # Bash blocks
        bash_matches = re.findall(r'```(?:bash|sh|shell|powershell)\s*\n(.*?)```', content, re.DOTALL)
        total_bash_blocks += len(bash_matches)

        # Mermaid blocks
        mm_matches = re.findall(r'```mermaid\s*\n(.*?)```', content, re.DOTALL)
        for i, mm in enumerate(mm_matches):
            mermaid_blocks.append((fname, i+1, mm.strip()))

        # Math delimiters ($ and $$ balance)
        # Remove code blocks first so code with $ doesn't interfere
        prose_only = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Count $$
        double_dollars = len(re.findall(r'\$\$', prose_only))
        if double_dollars % 2 != 0:
            math_delimiter_warnings.append((fname, f"Unbalanced $$ ({double_dollars})"))
        # Count single $ (excluding $$)
        single_dollar_prose = re.sub(r'\$\$.*?\$\$', '', prose_only, flags=re.DOTALL)
        single_dollars = len(re.findall(r'(?<!\$)\$(?!\$)', single_dollar_prose))
        if single_dollars % 2 != 0:
            math_delimiter_warnings.append((fname, f"Unbalanced single $ ({single_dollars})"))

print(f"\nAUDIT SUMMARY:")
print(f"Total Chapters checked: {total_chapters} / 20")
print(f"Total Python blocks: {total_python_blocks}")
print(f"Total C++ blocks: {total_cpp_blocks}")
print(f"Total Rust blocks: {total_rust_blocks}")
print(f"Total Bash blocks: {total_bash_blocks}")
print(f"Python syntax errors: {len(py_syntax_errors)}")
for err in py_syntax_errors:
    print(f"  SYNTAX ERROR: {err}")
print(f"NumPy 2.0 np.trapz deprecations: {len(np_trapz_warnings)}")
for w in np_trapz_warnings:
    print(f"  NP.TRAPZ: {w}")
print(f"Unclosed code fences: {len(unclosed_fences)}")
for u in unclosed_fences:
    print(f"  UNCLOSED FENCE: {u}")
print(f"Math delimiter warnings: {len(math_delimiter_warnings)}")
for m in math_delimiter_warnings:
    print(f"  MATH: {m}")
print(f"Total Mermaid diagrams: {len(mermaid_blocks)}")

print("\nWORD COUNTS:")
for fname, count in word_counts.items():
    print(f"  {fname}: {count} words")
