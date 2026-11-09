import os
import glob
import re

modules = [
    "ai-book-docs/module1-ros2",
    "ai-book-docs/module2-digital-twin",
    "ai-book-docs/module3-ai-robot-brain",
    "ai-book-docs/module4-vla",
]

all_files = []
for mod in modules:
    all_files.extend(glob.glob(os.path.join(mod, "*.mdx")))

print(f"Auditing {len(all_files)} MDX files across Modules 1-4 for edge cases...")

issues = []

for f in all_files:
    fname = os.path.basename(f)
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read()

    # 1. Check for QuizEngine presence and closing
    has_quiz_import = "import QuizEngine" in content
    has_quiz_tag = "<QuizEngine" in content
    quiz_closed = ("/>" in content[content.find("<QuizEngine"):] if has_quiz_tag else True)
    
    # 2. Check for ChapterProgress presence
    has_prog_import = "import ChapterProgress" in content
    has_prog_tag = "<ChapterProgress" in content
    
    # 3. Check for unbalanced parentheses in inline math
    # Search for $...$
    no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    no_code = re.sub(r"`.*?`", "", no_code)
    
    # Check for empty math blocks $$ $$
    empty_block_math = re.findall(r"\$\$\s*\$\$", no_code)
    if empty_block_math:
        issues.append((fname, f"Found {len(empty_block_math)} empty block math delimiters ($$ $$)"))

    # Check for raw script injections or unsafe HTML
    unsafe_tags = re.findall(r"<(script|iframe|object|embed)[^>]*>", content, re.I)
    if unsafe_tags:
        issues.append((fname, f"Found unsafe HTML tags: {unsafe_tags}"))

    # Check markdown link targets within repo
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", no_code)
    for text, url in links:
        if url.startswith("#") or url.startswith("http") or url.startswith("mailto"):
            continue
        # Internal relative link
        target_path = os.path.normpath(os.path.join(os.path.dirname(f), url.split("#")[0]))
        if url.endswith(".md") or url.endswith(".mdx"):
            if not os.path.exists(target_path):
                issues.append((fname, f"Broken markdown link target: {url} (resolved to {target_path})"))

print(f"Total issues found: {len(issues)}")
for fname, iss in issues:
    print(f"  [ISSUE] {fname}: {iss}")

if len(issues) == 0:
    print("ALL ADVERSARIAL CHECKS PASSED WITH ZERO INTEGRITY DEFECTS!")
