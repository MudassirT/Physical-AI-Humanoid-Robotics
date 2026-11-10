import os
import glob
import json
import re

modules = [
    'ai-book-docs/module6-bipedal-locomotion',
    'ai-book-docs/module7-dexterous-manipulation',
    'ai-book-docs/module8-robot-learning',
    'ai-book-docs/module9-sim-to-real'
]

print("=" * 60)
print("1. MODULE DIRECTORIES AND _category_.json AUDIT")
print("=" * 60)

all_files = []
for m in modules:
    cat_file = os.path.join(m, '_category_.json')
    if os.path.exists(cat_file):
        try:
            with open(cat_file, 'r', encoding='utf-8') as f:
                cat = json.load(f)
                print(f"[PASS] {cat_file} exists. label: '{cat.get('label')}', position: {cat.get('position')}")
        except Exception as e:
            print(f"[FAIL] {cat_file} error parsing JSON: {e}")
    else:
        print(f"[FAIL] {cat_file} DOES NOT EXIST!")
    
    files = sorted(glob.glob(os.path.join(m, '*.mdx')))
    print(f"  -> Found {len(files)} .mdx files in {m}")
    all_files.extend(files)

print(f"\nTotal MDX files in M6-M9: {len(all_files)} (Expected: 36)")
assert len(all_files) == 36, f"Expected 36 files, got {len(all_files)}"

print("\n" + "=" * 60)
print("2. STRUCTURAL AUDIT PER CHAPTER")
print("=" * 60)

stats = []

for filepath in all_files:
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Frontmatter check
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    has_fm = bool(fm_match)
    fm_id = None
    fm_title = None
    if has_fm:
        fm_text = fm_match.group(1)
        id_m = re.search(r"^id:\s*(.+)$", fm_text, re.MULTILINE)
        title_m = re.search(r"^title:\s*(.+)$", fm_text, re.MULTILINE)
        if id_m: fm_id = id_m.group(1).strip()
        if title_m: fm_title = title_m.group(1).strip()
    
    # 2. Components check
    has_progress = "<ChapterProgress" in content
    has_quiz = "<QuizEngine" in content
    
    # 3. Word count & line count
    lines = content.splitlines()
    words = content.split()
    word_count = len(words)
    line_count = len(lines)
    
    # 4. Code blocks check
    code_blocks = re.findall(r"```([a-zA-Z0-9_-]*)\r?\n(.*?)```", content, re.DOTALL)
    num_code_blocks = len(code_blocks)
    code_lines = sum(len(b[1].splitlines()) for b in code_blocks)
    languages = list(set(b[0] for b in code_blocks if b[0]))
    
    # Check for suspicious stubs in code blocks
    suspicious_stubs = []
    for lang, code in code_blocks:
        for line in code.splitlines():
            sline = line.strip()
            if sline in ["pass", "return 0", "return True", "return False", "return None", "..."]:
                # Check if it's an empty function
                pass
            if any(marker in sline.lower() for marker in ["todo:", "fixme:", "implement here", "placeholder"]):
                suspicious_stubs.append(sline)
    
    # 5. Math blocks check
    display_math = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
    inline_math = re.findall(r"\$(.*?)\$", content)
    num_math = len(display_math) + len(inline_math)
    
    # 6. Quiz inspection
    quiz_questions = []
    quiz_match = re.search(r"questions=\{?(\[.*?\])\}?", content, re.DOTALL)
    # alternatively search for questions json/js in QuizEngine props
    # let's find the QuizEngine tag
    qe_match = re.search(r"<QuizEngine\s+([^>]+)/>", content, re.DOTALL)
    quiz_props = qe_match.group(1) if qe_match else ""
    # count questions roughly by "question:"
    q_count = len(re.findall(r"question:\s*['\"]", quiz_props))
    
    stats.append({
        'path': filepath,
        'filename': fname,
        'fm_id': fm_id,
        'fm_title': fm_title,
        'has_fm': has_fm,
        'has_progress': has_progress,
        'has_quiz': has_quiz,
        'q_count': q_count,
        'line_count': line_count,
        'word_count': word_count,
        'num_code_blocks': num_code_blocks,
        'code_lines': code_lines,
        'languages': languages,
        'num_math': num_math,
        'suspicious_stubs': suspicious_stubs
    })

print(f"{'Filename':<35} | {'Lines':<5} | {'Words':<6} | {'Code':<4} | {'CodeL':<5} | {'Math':<4} | {'QuizQ':<5} | {'FM':<3} | {'CP':<3} | {'QE':<3}")
print("-" * 85)
for s in stats:
    print(f"{s['filename']:<35} | {s['line_count']:<5} | {s['word_count']:<6} | {s['num_code_blocks']:<4} | {s['code_lines']:<5} | {s['num_math']:<4} | {s['q_count']:<5} | {str(s['has_fm'])[0]}  | {str(s['has_progress'])[0]}  | {str(s['has_quiz'])[0]}")

print("\n" + "=" * 60)
print("3. AGGREGATE SUMMARY & THRESHOLD VERIFICATION")
print("=" * 60)

total_words = sum(s['word_count'] for s in stats)
total_code_lines = sum(s['code_lines'] for s in stats)
total_code_blocks = sum(s['num_code_blocks'] for s in stats)
total_math = sum(s['num_math'] for s in stats)
total_quiz_q = sum(s['q_count'] for s in stats)

min_words = min(s['word_count'] for s in stats)
max_words = max(s['word_count'] for s in stats)
avg_words = total_words / len(stats)

print(f"Total Words across 36 chapters: {total_words:,}")
print(f"Average Words per chapter: {avg_words:.1f} (min: {min_words}, max: {max_words})")
print(f"Total Code Blocks: {total_code_blocks} ({total_code_lines:,} lines of code)")
print(f"Total Math Expressions: {total_math}")
print(f"Total Quiz Questions: {total_quiz_q}")

missing_fm = [s['filename'] for s in stats if not s['has_fm']]
missing_cp = [s['filename'] for s in stats if not s['has_progress']]
missing_qe = [s['filename'] for s in stats if not s['has_quiz']]
empty_quizzes = [s['filename'] for s in stats if s['q_count'] == 0]
low_words = [s['filename'] for s in stats if s['word_count'] < 500]

print(f"\nMissing Frontmatter: {missing_fm}")
print(f"Missing ChapterProgress: {missing_cp}")
print(f"Missing QuizEngine: {missing_qe}")
print(f"Empty Quizzes: {empty_quizzes}")
print(f"Low Word Count (<500 words): {low_words}")

all_stubs = {s['filename']: s['suspicious_stubs'] for s in stats if s['suspicious_stubs']}
print(f"Suspicious Stubs count: {len(all_stubs)}")
for fn, stubs in all_stubs.items():
    print(f"  {fn}: {stubs}")
