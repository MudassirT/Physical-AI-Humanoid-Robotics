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

all_files = []
for m in modules:
    all_files.extend(sorted(glob.glob(os.path.join(m, '*.mdx'))))

print(f"Auditing QuizEngine in {len(all_files)} files...")

quiz_stats = []

for fpath in all_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find start of <QuizEngine
    start_idx = content.find('<QuizEngine')
    if start_idx == -1:
        quiz_stats.append({
            'file': fname,
            'found': False,
            'questions': []
        })
        continue
    
    # Find the closing tag: either '/>' or '</QuizEngine>'
    end_self_close = content.find('/>', start_idx)
    end_close_tag = content.find('</QuizEngine>', start_idx)
    
    if end_close_tag != -1 and (end_self_close == -1 or end_close_tag < end_self_close):
        quiz_block = content[start_idx:end_close_tag+13]
    elif end_self_close != -1:
        quiz_block = content[start_idx:end_self_close+2]
    else:
        quiz_block = content[start_idx:]
    
    # Extract questions: find all { id: ... } objects
    # Or count 'id:\s*["\']q' or 'question:'
    questions = re.findall(r'question:\s*["\'](.*?)["\'],', quiz_block)
    options_blocks = re.findall(r'options:\s*\[(.*?)\]', quiz_block, re.DOTALL)
    answers = re.findall(r'correctAnswer:\s*([0-9]+)', quiz_block)
    explanations = re.findall(r'explanation:\s*["\'](.*?)["\']', quiz_block)
    
    quiz_stats.append({
        'file': fname,
        'found': True,
        'q_count': len(questions),
        'opt_count': len(options_blocks),
        'ans_count': len(answers),
        'exp_count': len(explanations),
        'questions': questions,
        'answers': [int(a) for a in answers]
    })

print(f"{'Filename':<40} | {'Questions':<10} | {'Options':<8} | {'Answers':<8} | {'Explanations':<12}")
print("-" * 85)
for qs in quiz_stats:
    print(f"{qs['file']:<40} | {qs['q_count']:<10} | {qs['opt_count']:<8} | {qs['ans_count']:<8} | {qs['exp_count']:<12}")

zero_q = [qs['file'] for qs in quiz_stats if qs['q_count'] == 0]
mismatched = [qs['file'] for qs in quiz_stats if not (qs['q_count'] == qs['opt_count'] == qs['ans_count'] == qs['exp_count'])]

print("\n" + "=" * 60)
print(f"Zero questions files: {zero_q}")
print(f"Mismatched question components: {mismatched}")
print("=" * 60)
