import os
import re

base_dir = r"C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\ai-book-docs"

paragraphs_seen = {}
duplicates = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".mdx") or f.endswith(".md"):
            path = os.path.join(root, f)
            rel = os.path.relpath(path, base_dir)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                text = fp.read()
            # Split by double newline to get paragraphs
            paras = text.split("\n\n")
            for p in paras:
                clean = p.strip()
                # Exclude standard headers, code blocks, or short strings
                if len(clean) > 150 and not clean.startswith("```") and not clean.startswith("<QuizEngine") and not clean.startswith("<ChapterProgress") and not clean.startswith("---"):
                    # Normalize whitespace
                    norm = " ".join(clean.split())
                    if norm in paragraphs_seen:
                        duplicates.append((rel, paragraphs_seen[norm], norm[:80]))
                    else:
                        paragraphs_seen[norm] = rel

print(f"Total unique long paragraphs indexed: {len(paragraphs_seen)}")
print(f"Total duplicates found across different chapters: {len(duplicates)}")
for dup in duplicates[:10]:
    print(f"  Duplicate between {dup[0]} and {dup[1]}: {dup[2]}...")
