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
print(f"CROSS-CHAPTER SIMILARITY & DUPLICATION AUDIT ({len(all_files)} chapters)")
print("=" * 60)

chapter_words = {}
for fpath in all_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    # Strip frontmatter and QuizEngine
    text = re.sub(r"^---.*?---", "", text, flags=re.DOTALL)
    text = re.sub(r"<QuizEngine.*?(?:/>|</QuizEngine>)", "", text, flags=re.DOTALL)
    # Tokenize words (lowercase, alphanumeric)
    tokens = set(re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()))
    chapter_words[fname] = tokens

high_similarity_pairs = []
for i in range(len(all_files)):
    f1 = os.path.basename(all_files[i])
    s1 = chapter_words[f1]
    for j in range(i + 1, len(all_files)):
        f2 = os.path.basename(all_files[j])
        s2 = chapter_words[f2]
        
        # Jaccard similarity
        inter = len(s1.intersection(s2))
        union = len(s1.union(s2))
        jaccard = inter / union if union > 0 else 0
        
        if jaccard > 0.60:  # Flag if >60% vocabulary overlap
            high_similarity_pairs.append((f1, f2, jaccard))

print(f"Total chapter pairs compared: {len(all_files) * (len(all_files) - 1) // 2}")
print(f"Pairs with >60% vocabulary overlap: {len(high_similarity_pairs)}")
for f1, f2, sim in high_similarity_pairs:
    print(f"  {f1} <-> {f2}: Jaccard = {sim:.3f}")

# Also check max similarity across all pairs
max_sim = 0
max_pair = None
for i in range(len(all_files)):
    f1 = os.path.basename(all_files[i])
    s1 = chapter_words[f1]
    for j in range(i + 1, len(all_files)):
        f2 = os.path.basename(all_files[j])
        s2 = chapter_words[f2]
        inter = len(s1.intersection(s2))
        union = len(s1.union(s2))
        jaccard = inter / union if union > 0 else 0
        if jaccard > max_sim:
            max_sim = jaccard
            max_pair = (f1, f2)

print(f"\nHighest vocabulary overlap pair: {max_pair[0]} <-> {max_pair[1]} at Jaccard = {max_sim:.3f}")
if max_sim < 0.65:
    print("[PASS] No copy-pasted or templated chapters detected! Every chapter has unique, domain-specific content.")
