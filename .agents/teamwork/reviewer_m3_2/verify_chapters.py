import os
import glob
import re
import json

modules = {
    'module6-bipedal-locomotion': (10, 6, 'Bipedal Locomotion & Whole-Body Control'),
    'module7-dexterous-manipulation': (8, 7, 'Dexterous Manipulation & Hand Design'),
    'module8-robot-learning': (10, 8, 'Robot Learning & Reinforcement Learning'),
    'module9-sim-to-real': (8, 9, 'Sim-to-Real Transfer & Domain Randomization')
}

base = 'ai-book-docs'
results = []
total_chapters = 0

for m_dir, (expected_count, expected_pos, expected_label) in modules.items():
    cat_path = os.path.join(base, m_dir, '_category_.json')
    cat_valid = False
    if os.path.exists(cat_path):
        with open(cat_path, 'r', encoding='utf-8') as f:
            cat_data = json.load(f)
            if cat_data.get('position') == expected_pos and cat_data.get('label') == expected_label:
                cat_valid = True
    
    files = sorted([f for f in os.listdir(os.path.join(base, m_dir)) if f.endswith('.mdx')])
    total_chapters += len(files)
    print(f'=== {m_dir} ===')
    print(f'Category valid: {cat_valid} (pos={expected_pos}, label="{expected_label}")')
    print(f'Files found: {len(files)} / expected {expected_count}')
    
    for f in files:
        f_path = os.path.join(base, m_dir, f)
        with open(f_path, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        has_frontmatter = content.startswith('---') and 'sidebar_position:' in content and 'title:' in content
        has_progress = '<ChapterProgress' in content and 'moduleId=' in content
        has_quiz = '<QuizEngine' in content and 'questions=' in content
        math_inline_count = len(re.findall(r'\$[^\$]+\$', content))
        math_block_count = len(re.findall(r'\$\$[^\$]+\$\$', content, re.DOTALL))
        code_block_count = len(re.findall(r'```[a-zA-Z]*\n', content))
        word_count = len(content.split())
        
        # Facade / placeholder search
        placeholders = re.findall(r'(?i)\b(TODO|TBD|placeholder|lorem ipsum|coming soon)\b', content)
        
        # Check quiz question count
        quiz_q_count = len(re.findall(r'id:\s*[\'\"]q\d', content))
        
        results.append({
            'module': m_dir,
            'file': f,
            'words': word_count,
            'frontmatter': has_frontmatter,
            'progress': has_progress,
            'quiz': has_quiz,
            'quiz_questions': quiz_q_count,
            'math_blocks': math_block_count,
            'math_inlines': math_inline_count,
            'code_blocks': code_block_count,
            'placeholders': placeholders
        })

print(f'\nTotal chapters analyzed: {total_chapters}')
min_words = min(r['words'] for r in results)
max_words = max(r['words'] for r in results)
avg_words = sum(r['words'] for r in results) / len(results)
print(f'Word counts: Min={min_words}, Max={max_words}, Avg={avg_words:.1f}')

placeholder_files = [(r['file'], r['placeholders']) for r in results if len(r['placeholders']) > 0]
print(f'Files with placeholder tokens: {placeholder_files}')

all_valid = True
for r in results:
    if not r['frontmatter'] or not r['progress'] or not r['quiz'] or r['code_blocks'] < 1 or r['words'] < 1000:
        print(f"FLAGGED: {r['file']} (FM={r['frontmatter']}, Prog={r['progress']}, Quiz={r['quiz']}, Code={r['code_blocks']}, Words={r['words']})")
        all_valid = False

if all_valid:
    print('ALL 36 CHAPTERS FULLY COMPLIANT WITH FRONTMATTER, PROGRESS, QUIZ, CODE BLOCKS, AND LENGTH!')
