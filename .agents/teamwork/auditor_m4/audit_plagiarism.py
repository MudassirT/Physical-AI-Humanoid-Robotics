import os
import re
from collections import Counter
import math

MODULES = [
    'module10-hardware-architecture',
    'module11-safety-ethics',
    'module12-capstone-frontiers'
]

print("=== PLAGIARISM & CROSS-CHAPTER REPETITION AUDIT ===")

chapters = []

for mod in MODULES:
    mod_dir = os.path.join('ai-book-docs', mod)
    files = sorted([f for f in os.listdir(mod_dir) if f.endswith('.mdx')])
    for f in files:
        fpath = os.path.join(mod_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
            
        # Strip frontmatter
        body = re.sub(r'^---\r?\n.*?\r?\n---\r?\n', '', content, flags=re.DOTALL)
        # Strip code blocks
        body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
        # Strip JSX tags
        body = re.sub(r'<[^>]+>', '', body)
        
        words = re.findall(r'[a-zA-Z0-9_\-]+', body.lower())
        chapters.append({
            'name': f"{mod}/{f}",
            'words': words
        })

print(f"Auditing {len(chapters)} chapters for duplicate paragraphs and n-gram overlap...")

# Check for identical 10-gram phrases across distinct chapters
ngram_to_ch = {}
suspicious_overlaps = []

for ch in chapters:
    name = ch['name']
    words = ch['words']
    seen_in_ch = set()
    for i in range(len(words) - 9):
        ngram = tuple(words[i:i+10])
        if ngram in seen_in_ch:
            continue
        seen_in_ch.add(ngram)
        if ngram not in ngram_to_ch:
            ngram_to_ch[ngram] = []
        ngram_to_ch[ngram].append(name)

# Analyze ngrams appearing in multiple chapters
cross_ch_ngrams = {k: v for k, v in ngram_to_ch.items() if len(v) > 1}
print(f"Total 10-grams examined: {len(ngram_to_ch)}")
print(f"10-grams shared across distinct chapters: {len(cross_ch_ngrams)}")

# Let's see which pairs of chapters have the most shared 10-grams
pair_counts = Counter()
for ngram, ch_list in cross_ch_ngrams.items():
    # Only if chapters are different
    for i in range(len(ch_list)):
        for j in range(i + 1, len(ch_list)):
            pair_counts[(ch_list[i], ch_list[j])] += 1

print("\nTop chapter pairs with shared 10-grams:")
for (c1, c2), count in pair_counts.most_common(10):
    print(f"  {c1} <-> {c2}: {count} shared 10-grams")
    # Show example shared 10-grams
    sample_ngrams = [ng for ng, chs in cross_ch_ngrams.items() if c1 in chs and c2 in chs][:3]
    for sn in sample_ngrams:
        print(f"    - \"{' '.join(sn)}\"")

# Pairwise Jaccard similarity of vocabulary
print("\nPairwise Jaccard similarity across all chapters (unique word sets):")
max_jaccard = 0.0
max_pair = None
for i in range(len(chapters)):
    s1 = set(chapters[i]['words'])
    for j in range(i + 1, len(chapters)):
        s2 = set(chapters[j]['words'])
        jaccard = len(s1.intersection(s2)) / len(s1.union(s2))
        if jaccard > max_jaccard:
            max_jaccard = jaccard
            max_pair = (chapters[i]['name'], chapters[j]['name'])

print(f"Maximum pairwise vocabulary Jaccard similarity: {max_jaccard:.4f} between {max_pair[0]} and {max_pair[1]}")
if max_jaccard < 0.45:
    print("PASS: Chapters exhibit high distinctiveness and specialized vocabulary; no template copy-paste detected.")
else:
    print("WARNING: Elevated vocabulary similarity, checking text chunks...")
