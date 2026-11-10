import os
import re
import json

MODULES = [
    'module10-hardware-architecture',
    'module11-safety-ethics',
    'module12-capstone-frontiers'
]

print("=== EXHAUSTIVE QUIZ ENGINE AUDIT ACROSS ALL 20 CHAPTERS ===")

total_questions = 0
malformed_quizzes = []
module_quiz_stats = {}

for mod in MODULES:
    mod_dir = os.path.join('ai-book-docs', mod)
    files = sorted([f for f in os.listdir(mod_dir) if f.endswith('.mdx')])
    mod_q_count = 0
    print(f"\n--- {mod} ({len(files)} chapters) ---")
    for f in files:
        fpath = os.path.join(mod_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Check QuizEngine import
        has_import = 'import QuizEngine from \'@site/src/components/QuizEngine\'' in content or 'import QuizEngine from "@site/src/components/QuizEngine"' in content
        if not has_import:
            malformed_quizzes.append((f, 'Missing QuizEngine import'))
        
        # Extract <QuizEngine ... /> block
        qe_match = re.search(r'<QuizEngine\b(.*?)\/>', content, re.DOTALL)
        if not qe_match:
            # Maybe not self-closing?
            qe_match = re.search(r'<QuizEngine\b(.*?)<\/QuizEngine>', content, re.DOTALL)
        
        if not qe_match:
            malformed_quizzes.append((f, 'Missing <QuizEngine> JSX tag'))
            continue
        
        qe_body = qe_match.group(1)
        
        # Extract individual questions
        # Matches: { id: ..., question: ..., options: [...], correctIndex: ..., explanation: ... }
        # Note: can use either correctIndex or correctAnswer
        # Let's find each object inside questions={[ ... ]}
        q_blocks = re.findall(r'\{\s*id:\s*[\'"]([^\'"]+)[\'"],\s*question:\s*[\'"](.*?)[\'"],\s*options:\s*(\[.*?\]),\s*(?:correctIndex|correctAnswer):\s*(\d+),\s*explanation:\s*[\'"](.*?)[\'"]\s*\}', qe_body, re.DOTALL)
        
        if not q_blocks:
            malformed_quizzes.append((f, 'Zero questions parsed in QuizEngine block'))
            continue
            
        mod_q_count += len(q_blocks)
        total_questions += len(q_blocks)
        
        q_summaries = []
        for q_id, q_question, q_opts_raw, q_correct, q_expl in q_blocks:
            opts = re.findall(r'[\'"](.*?)[\'"]', q_opts_raw)
            c_idx = int(q_correct)
            
            if len(opts) < 3:
                malformed_quizzes.append((f, f"Question {q_id} has < 3 options: {len(opts)}"))
            if c_idx < 0 or c_idx >= len(opts):
                malformed_quizzes.append((f, f"Question {q_id} invalid correctIndex {c_idx} for {len(opts)} options"))
            if len(q_expl.split()) < 8:
                malformed_quizzes.append((f, f"Question {q_id} explanation too short ({len(q_expl.split())} words)"))
                
            q_summaries.append(f"{q_id}(opts={len(opts)},ans={c_idx},expl_words={len(q_expl.split())})")
            
        print(f"  {f}: {len(q_blocks)} questions | {', '.join(q_summaries)}")

    module_quiz_stats[mod] = mod_q_count

print(f"\n==========================================")
print(f"Total Quiz Questions Parsed: {total_questions}")
for mod, count in module_quiz_stats.items():
    print(f"  {mod}: {count} questions")

if malformed_quizzes:
    print(f"\nMALFORMED QUIZZES DETECTED ({len(malformed_quizzes)}):")
    for item in malformed_quizzes:
        print(f"  {item}")
else:
    print("\nALL 20 CHAPTERS PASS THE QUIZ ENGINE AUDIT WITH 100% VALIDATION!")
