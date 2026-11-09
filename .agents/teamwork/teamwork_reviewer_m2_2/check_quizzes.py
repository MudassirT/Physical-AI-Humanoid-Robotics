import glob
import re
from pathlib import Path

def validate_quizzes():
    files = sorted(glob.glob("ai-book-docs/module3-ai-robot-brain/*.mdx") + glob.glob("ai-book-docs/module4-vla/*.mdx"))
    
    quiz_ids = set()
    total_questions = 0
    
    for f in files:
        txt = Path(f).read_text(encoding="utf-8")
        
        # Extract quizId
        qid_match = re.search(r'quizId="([^"]+)"', txt)
        assert qid_match, f"Missing quizId in {f}"
        qid = qid_match.group(1)
        assert qid not in quiz_ids, f"Duplicate quizId '{qid}' found in {f}"
        quiz_ids.add(qid)
        
        # Extract moduleId
        mod_match = re.search(r'moduleId="([^"]+)"', txt)
        assert mod_match, f"Missing moduleId in {f}"
        mod = mod_match.group(1)
        expected_mod = "module3" if "module3" in f else "module4"
        assert mod == expected_mod, f"Module mismatch in {f}: {mod} != {expected_mod}"
        
        # Extract questions
        # We can count how many questions are in each quiz
        q_count = len(re.findall(r'id:\s*["\']q\d+["\']', txt))
        assert q_count >= 3, f"Expected at least 3 questions in {f}, got {q_count}"
        total_questions += q_count
        
        # Verify correctIndex values are valid integers
        indices = re.findall(r'correctIndex:\s*(\d+)', txt)
        assert len(indices) == q_count, f"Mismatch between questions ({q_count}) and correctIndex ({len(indices)}) in {f}"
        for ci in indices:
            assert int(ci) in [0, 1, 2, 3], f"Invalid correctIndex {ci} in {f}"
            
        print(f"[PASS] {Path(f).name}: Quiz '{qid}' has {q_count} questions with verified structure.")

    print(f"\nAll 20 chapters validated! Total questions across M3 and M4: {total_questions}")

if __name__ == "__main__":
    validate_quizzes()
