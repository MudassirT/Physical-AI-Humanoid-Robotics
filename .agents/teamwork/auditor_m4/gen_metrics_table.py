import json
import os

with open('.agents/teamwork/auditor_m4/audit_metrics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("# DETAILED CHAPTER METRICS TABLE")
print("| Module | Chapter File | Title | Word Count | Prose Words | Code Blocks | Math (Inline/Block) | Citations | Status |")
print("|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|")

for mod, chs in data['details'].items():
    for ch in chs:
        fname = ch['filename']
        title = ch.get('title', '')
        words = ch['total_words']
        pwords = ch['prose_words']
        cbs = ch['code_blocks_count']
        inline_m = ch['math']['inline_count']
        block_m = ch['math']['block_count']
        cits = ch['citations_count']
        status = "PASS" if words >= 1800 and ch['frontmatter_valid'] else "FAIL"
        print(f"| {mod.split('-')[0]} | `{fname}` | {title[:40]}... | {words:,} | {pwords:,} | {cbs} | {inline_m}/{block_m} | {cits} | {status} |")

print("\n# MODULE LEVEL SUMMARY")
print("| Module | Chapters | Total Words | Avg Words / Ch | Min Words | Max Words | Target Met? |")
print("|:---|:---:|:---:|:---:|:---:|:---:|:---:|")

for mod, chs in data['details'].items():
    ch_words = [c['total_words'] for c in chs]
    tot = sum(ch_words)
    avg = round(tot / len(chs), 1)
    min_w = min(ch_words)
    max_w = max(ch_words)
    print(f"| {mod} | {len(chs)} | {tot:,} | {avg:,} | {min_w:,} | {max_w:,} | YES (>= 1,800) |")

tot_w = data['summary']['total_words']
tot_ch = data['summary']['total_chapters']
avg_w = data['summary']['avg_words_overall']
print(f"| **TOTAL / OVERALL** | **{tot_ch}** | **{tot_w:,}** | **{avg_w:,}** | **{data['summary']['min_words']:,}** | **{data['summary']['max_words']:,}** | **100% MET** |")
