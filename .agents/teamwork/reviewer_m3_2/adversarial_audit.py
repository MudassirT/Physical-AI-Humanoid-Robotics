import os
import re
import ast

modules_info = {
    'module6-bipedal-locomotion': 10,
    'module7-dexterous-manipulation': 8,
    'module8-robot-learning': 10,
    'module9-sim-to-real': 8
}

base = 'ai-book-docs'
findings = []

for mod_dir, expected_total in modules_info.items():
    files = sorted([f for f in os.listdir(os.path.join(base, mod_dir)) if f.endswith('.mdx')])
    for f in files:
        fpath = os.path.join(base, mod_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()

        # 1. Check ChapterProgress totalChapters
        prog_match = re.search(r'<ChapterProgress\s+[^>]*totalChapters=\{(\d+)\}', content)
        if not prog_match:
            findings.append((f, 'MISSING_PROGRESS_TOTAL', 'No totalChapters found in ChapterProgress'))
        else:
            total_val = int(prog_match.group(1))
            if total_val != expected_total:
                findings.append((f, 'WRONG_PROGRESS_TOTAL', f'Found totalChapters={total_val}, expected {expected_total}'))

        # 2. Check QuizEngine structure
        quiz_match = re.search(r'<QuizEngine\s+([^>]+)/>', content, re.DOTALL)
        if not quiz_match:
            findings.append((f, 'MISSING_QUIZ', 'No QuizEngine component found'))
        else:
            q_block = quiz_match.group(1)
            if 'passThreshold=' not in q_block:
                findings.append((f, 'MISSING_QUIZ_THRESHOLD', 'Quiz missing passThreshold'))

        # 3. Check Python code block syntax with ast.parse
        py_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        for idx, code in enumerate(py_blocks):
            try:
                ast.parse(code)
            except SyntaxError as e:
                # Some might be partial pseudocode or snippets, let's flag
                findings.append((f, 'PYTHON_SYNTAX_ERROR', f'Block {idx+1}: {e.msg} at line {e.lineno}'))

        # 4. Check for references / citations section
        has_citations = bool(re.search(r'(?i)##\s+.*(reference|citation|literature)', content))
        if not has_citations:
            findings.append((f, 'MISSING_CITATIONS', 'No literature/references section found'))

        # 5. Check for lab / hands-on project
        has_lab = bool(re.search(r'(?i)##\s+.*(lab|hands-on|exercise|project)', content))
        if not has_lab:
            findings.append((f, 'MISSING_LAB', 'No lab/project section found'))

        # 6. Check for mermaid diagrams
        has_mermaid = '```mermaid' in content
        if not has_mermaid:
            findings.append((f, 'MISSING_MERMAID', 'No mermaid diagram found'))

print(f"Total findings: {len(findings)}")
for f, cat, desc in findings:
    print(f"[{cat}] {f}: {desc}")

if len(findings) == 0:
    print("ALL ADVERSARIAL STRESS TESTS PASSED WITH ZERO VIOLATIONS!")
