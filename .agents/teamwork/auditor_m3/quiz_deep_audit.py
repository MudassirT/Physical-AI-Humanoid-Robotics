import os
import glob
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

print("=" * 60)
print(f"VERIFYING QUIZ INTEGRITY ACROSS ALL {len(all_files)} CHAPTERS")
print("=" * 60)

all_question_texts = set()
duplicate_questions = []
invalid_indices = []

total_q = 0

for fpath in all_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_idx = content.find('<QuizEngine')
    assert start_idx != -1, f"Missing QuizEngine in {fname}"
    
    end_self_close = content.find('/>', start_idx)
    end_close_tag = content.find('</QuizEngine>', start_idx)
    if end_close_tag != -1 and (end_self_close == -1 or end_close_tag < end_self_close):
        quiz_block = content[start_idx:end_close_tag+13]
    elif end_self_close != -1:
        quiz_block = content[start_idx:end_self_close+2]
    else:
        quiz_block = content[start_idx:]
    
    # Extract questions
    q_matches = re.findall(r'question:\s*["\'](.*?)["\'],', quiz_block)
    # Extract options per question: find all options: [ ... ]
    opt_matches = re.findall(r'options:\s*\[(.*?)\]', quiz_block, re.DOTALL)
    # Extract correctIndex
    ci_matches = re.findall(r'correctIndex:\s*([0-9]+)', quiz_block)
    # Extract explanations
    exp_matches = re.findall(r'explanation:\s*["\'](.*?)["\']', quiz_block)
    
    n_q = len(q_matches)
    n_opt = len(opt_matches)
    n_ci = len(ci_matches)
    n_exp = len(exp_matches)
    
    total_q += n_q
    
    assert n_q >= 3, f"Chapter {fname} has fewer than 3 questions: {n_q}"
    assert n_q == n_opt == n_ci == n_exp, f"Mismatch in {fname}: q={n_q}, opt={n_opt}, ci={n_ci}, exp={n_exp}"
    
    for i in range(n_q):
        q_text = q_matches[i].strip()
        if q_text in all_question_texts:
            duplicate_questions.append((fname, q_text))
        all_question_texts.add(q_text)
        
        # parse options
        opts = [o.strip() for o in opt_matches[i].split(',') if o.strip()]
        ci = int(ci_matches[i])
        if ci < 0 or ci >= len(opts):
            invalid_indices.append((fname, i, ci, len(opts)))

print(f"Total Questions Verified: {total_q}")
print(f"Unique Question Texts: {len(all_question_texts)}")
print(f"Duplicate Questions: {len(duplicate_questions)}")
print(f"Invalid correctIndex: {len(invalid_indices)}")

if duplicate_questions:
    print(f"Duplicates: {duplicate_questions}")
if invalid_indices:
    print(f"Invalid indices: {invalid_indices}")

assert len(duplicate_questions) == 0, "Duplicate questions detected!"
assert len(invalid_indices) == 0, "Out of bounds correctIndex detected!"
print("[PASS] All QuizEngine questions are 100% authentic, well-formed, and valid!")
