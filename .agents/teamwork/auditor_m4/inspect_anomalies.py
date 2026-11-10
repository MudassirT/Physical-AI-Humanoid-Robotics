import json
import os
import re

with open('.agents/teamwork/auditor_m4/audit_metrics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== INSPECTING CHAPTER PROGRESS DETECTION ===')
for mod, chs in data['details'].items():
    for ch in chs:
        filename = ch['filename']
        filepath = os.path.join('ai-book-docs', mod, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check any occurrences of ChapterProgress
        cp_lines = [line for line in content.splitlines() if 'ChapterProgress' in line]
        print(f"{mod}/{filename}: {len(cp_lines)} lines mentioning ChapterProgress")
        for line in cp_lines[:4]:
            print(f"    {line.strip()}")

print('\n=== SUSPICIOUS CODE DETAILS ===')
for mod, chs in data['details'].items():
    for ch in chs:
        if ch['suspicious_code']:
            print(f"{mod}/{ch['filename']}:")
            for sc in ch['suspicious_code']:
                print(f"  Flags: {sc['flags']}")
                print(f"  Snippet:\n{sc['snippet']}")
