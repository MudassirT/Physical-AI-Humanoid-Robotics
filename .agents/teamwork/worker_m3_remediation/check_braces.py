import glob
import re

modules = ['module6-bipedal-locomotion', 'module7-dexterous-manipulation', 'module8-robot-learning', 'module9-sim-to-real']

suspicious_braces = []

for m in modules:
    for path in glob.glob(f'ai-book-docs/{m}/*.mdx'):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove code blocks
        content_no_code = re.sub(r'```[\s\S]*?```', '', content)
        # Remove display math $$ ... $$
        content_no_display_math = re.sub(r'\$\$[\s\S]*?\$\$', '', content_no_code)
        # Remove inline math $ ... $
        content_no_math = re.sub(r'\$[^\$\n]+?\$', '', content_no_display_math)
        # Remove QuizEngine block <QuizEngine ... />
        content_no_quiz = re.sub(r'<QuizEngine[\s\S]*?\/>', '', content_no_math)
        # Remove ChapterProgress <ChapterProgress ... />
        content_no_progress = re.sub(r'<ChapterProgress[\s\S]*?\/>', '', content_no_quiz)
        
        # Check for remaining '{' or '}'
        lines = content_no_progress.splitlines()
        for line_no, line in enumerate(lines, 1):
            if '{' in line or '}' in line:
                # Exclude import statements
                if line.strip().startswith('import '):
                    continue
                # Exclude frontmatter delimiters (---)
                suspicious_braces.append((path, line_no, line.strip()))

print(f"Suspicious braces found: {len(suspicious_braces)}")
for p, l, s in suspicious_braces:
    print(f"{p}:{l} -> {s}")
