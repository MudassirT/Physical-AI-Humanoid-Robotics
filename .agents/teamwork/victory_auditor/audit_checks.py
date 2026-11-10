import os
import re
import json

base_dir = r"C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main"
docs_dir = os.path.join(base_dir, "ai-book-docs")
backend_dir = os.path.join(base_dir, "backend")

print("=== PROGRAMMATIC AUDIT CHECKS ===")

# 1. Module and chapter enumeration
modules = [
    ("module1-ros2", 14),
    ("module2-digital-twin", 10),
    ("module3-ai-robot-brain", 10),
    ("module4-vla", 10),
    ("module5-kinematics-dynamics", 10),
    ("module6-bipedal-locomotion", 10),
    ("module7-dexterous-manipulation", 8),
    ("module8-robot-learning", 10),
    ("module9-sim-to-real", 8),
    ("module10-hardware-architecture", 8),
    ("module11-safety-ethics", 6),
    ("module12-capstone-frontiers", 6),
]

total_chapters = 0
chapter_details = {}
missing_files = []
invalid_frontmatter = []
categories_checked = {}

for mod_name, expected_count in modules:
    mod_path = os.path.join(docs_dir, mod_name)
    if not os.path.isdir(mod_path):
        missing_files.append(f"Directory missing: {mod_name}")
        continue
    
    # Check _category_.json
    cat_file = os.path.join(mod_path, "_category_.json")
    if os.path.exists(cat_file):
        try:
            with open(cat_file, "r", encoding="utf-8") as f:
                cat_data = json.load(f)
                categories_checked[mod_name] = cat_data.get("label", "")
        except Exception as e:
            categories_checked[mod_name] = f"Error: {e}"
    else:
        categories_checked[mod_name] = "MISSING"

    mdx_files = [f for f in os.listdir(mod_path) if f.endswith(".mdx") or f.endswith(".md")]
    chapter_details[mod_name] = {
        "expected": expected_count,
        "found": len(mdx_files),
        "files": sorted(mdx_files)
    }
    total_chapters += len(mdx_files)

print(f"Total Modules Checked: {len(modules)}")
print(f"Total Chapters Found: {total_chapters} (Expected: 110)")
for mod, details in chapter_details.items():
    status = "OK" if details["found"] == details["expected"] else "MISMATCH"
    print(f"  {mod}: found {details['found']}/{details['expected']} [{status}] (Category: {categories_checked.get(mod)})")

# Check intro.mdx
intro_path = os.path.join(docs_dir, "intro.mdx")
intro_exists = os.path.exists(intro_path)
print(f"intro.mdx present: {intro_exists}")

# 2. Scanning for forbidden tokens in MDX files
forbidden_patterns = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\bPLACEHOLDER\b",
    r"lorem\s+ipsum",
    r"NotImplementedError"
]

findings = []
total_word_count = 0
total_code_blocks = 0
total_math_blocks = 0
quiz_engine_count = 0
chapter_progress_count = 0

all_docs = []
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith(".mdx") or f.endswith(".md"):
            all_docs.append(os.path.join(root, f))

for doc_path in all_docs:
    rel_path = os.path.relpath(doc_path, base_dir)
    with open(doc_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Word count
    words = len(content.split())
    total_word_count += words
    
    # Code blocks
    code_blocks = len(re.findall(r"```", content)) // 2
    total_code_blocks += code_blocks
    
    # KaTeX math blocks: inline $...$ and block $$...$$
    math_inline = len(re.findall(r"(?<!\$)\$(?!\$)[^\n\$]+(?<!\$)\$(?!\$)", content))
    math_blocks = len(re.findall(r"\$\$[\s\S]+?\$\$", content))
    total_math_blocks += (math_inline + math_blocks)

    if "<QuizEngine" in content:
        quiz_engine_count += 1
    if "<ChapterProgress" in content:
        chapter_progress_count += 1

    # Check forbidden
    for pat in forbidden_patterns:
        matches = re.findall(pat, content, re.IGNORECASE if "lorem" in pat else 0)
        if matches:
            findings.append((rel_path, pat, len(matches)))

print("\n--- CONTENT RIGOR METRICS ---")
print(f"Total Documents Scanned: {len(all_docs)}")
print(f"Total Curriculum Word Count: {total_word_count:,}")
print(f"Total Code Blocks: {total_code_blocks:,}")
print(f"Total KaTeX Math Elements: {total_math_blocks:,}")
print(f"Chapters with <QuizEngine />: {quiz_engine_count}")
print(f"Chapters with <ChapterProgress />: {chapter_progress_count}")

print("\n--- FORBIDDEN TOKEN SCAN (MDX) ---")
if findings:
    for path, pat, cnt in findings:
        print(f"  FLAG: {path} contains {cnt} match(es) for pattern '{pat}'")
else:
    print("  CLEAN: 0 forbidden tokens found across all documentation files.")

# 3. Scanning backend for stubs / facades
backend_findings = []
backend_py_files = []
for root, dirs, files in os.walk(backend_dir):
    if ".venv" in root or "__pycache__" in root or ".pytest_cache" in root:
        continue
    for f in files:
        if f.endswith(".py"):
            backend_py_files.append(os.path.join(root, f))

for py_path in backend_py_files:
    rel_path = os.path.relpath(py_path, base_dir)
    with open(py_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        if re.search(r"raise\s+NotImplementedError", line):
            backend_findings.append((rel_path, idx, "raise NotImplementedError", line.strip()))
        elif re.search(r"^\s*pass\s*$", line):
            # check if inside except block or empty function
            backend_findings.append((rel_path, idx, "bare pass", line.strip()))
        elif re.search(r"\bTODO\b", line):
            backend_findings.append((rel_path, idx, "TODO comment", line.strip()))

print("\n--- BACKEND INTEGRITY SCAN ---")
print(f"Backend Python Files Scanned: {len(backend_py_files)}")
if backend_findings:
    for path, lno, kind, text in backend_findings:
        print(f"  NOTICE: {path}:{lno} [{kind}]: {text}")
else:
    print("  CLEAN: 0 stubs / bare pass / TODOs found in backend code.")

print("\n=== AUDIT CHECKS COMPLETE ===")
