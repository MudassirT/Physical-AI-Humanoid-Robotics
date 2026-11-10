import os
import re
import json

MODULES = [
    'module10-hardware-architecture',
    'module11-safety-ethics',
    'module12-capstone-frontiers'
]

print("=== QUIZ ENGINE AUDIT ACROSS ALL 20 CHAPTERS ===")

total_questions = 0
malformed_quizzes = []

for mod in MODULES:
    mod_dir = os.path.join('ai-book-docs', mod)
    files = sorted([f for f in os.listdir(mod_dir) if f.endswith('.mdx')])
    for f in files:
        fpath = os.path.join(mod_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Extract the questions array from <QuizEngine questions={[ ... ]} />
        # Match from <QuizEngine questions={[ to ]} />
        match = re.search(r'<QuizEngine\s+questions=\{\s*(\[.*?\])\s*\}\s*/>', content, re.DOTALL)
        if not match:
            malformed_quizzes.append((f, 'No QuizEngine tag or questions prop match'))
            continue
        
        q_text = match.group(1)
        # Parse individual question objects
        # Each object has: id, question, options, correctAnswer, explanation
        q_objs = re.findall(r'\{\s*id:\s*[\'"]([^\'"]+)[\'"],\s*question:\s*[\'"](.*?)[\'"],\s*options:\s*(\[.*?\]),\s*correctAnswer:\s*(\d+),\s*explanation:\s*[\'"](.*?)[\'"]\s*\}', q_text, re.DOTALL)
        
        if not q_objs:
            malformed_quizzes.append((f, 'Failed to extract question objects'))
            continue
        
        total_questions += len(q_objs)
        q_summaries = []
        for q_id, q_question, q_opts_raw, q_correct, q_expl in q_objs:
            opts = re.findall(r'[\'"](.*?)[\'"]', q_opts_raw)
            c_idx = int(q_correct)
            
            # Sanity checks
            if len(opts) < 3:
                malformed_quizzes.append((f, f"Question {q_id} has fewer than 3 options: {len(opts)}"))
            if c_idx < 0 or c_idx >= len(opts):
                malformed_quizzes.append((f, f"Question {q_id} invalid correctAnswer {c_idx} for {len(opts)} options"))
            if len(q_expl.split()) < 8:
                malformed_quizzes.append((f, f"Question {q_id} explanation too short: '{q_expl}'"))
            
            q_summaries.append(f"{q_id}(opts={len(opts)},ans={c_idx},expl_words={len(q_expl.split())})")

        print(f"{mod}/{f}: {len(q_objs)} questions -> {', '.join(q_summaries)}")

print(f"\nTotal questions across 20 chapters: {total_questions}")
if malformed_quizzes:
    print(f"MALFORMED QUIZZES DETECTED ({len(malformed_quizzes)}):")
    for item in malformed_quizzes:
        print(f"  {item}")
else:
    print("ALL QUIZZES ARE FULLY VALID, WELL-FORMED, AND SUBSTANTIVE!")
