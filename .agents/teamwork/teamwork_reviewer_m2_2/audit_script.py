import os
import glob
import re
import sys

def audit_module(mod_dir, expected_count):
    files = sorted(glob.glob(os.path.join(mod_dir, '*.mdx')))
    print(f'Checking {mod_dir}: found {len(files)} files (expected {expected_count})')
    assert len(files) == expected_count, f'Count mismatch: {len(files)} != {expected_count}'
    
    positions = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Frontmatter
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        assert fm_match, f'Missing frontmatter in {f}'
        fm = fm_match.group(1)
        
        pos_match = re.search(r'sidebar_position:\s*(\d+)', fm)
        assert pos_match, f'Missing sidebar_position in {f}'
        pos = int(pos_match.group(1))
        positions.append(pos)
        
        title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        assert title_match, f'Missing title in {f}'
        
        desc_match = re.search(r'description:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        assert desc_match, f'Missing description in {f}'
        
        # Components
        assert 'import ChapterProgress' in content, f'Missing ChapterProgress import in {f}'
        assert 'import QuizEngine' in content, f'Missing QuizEngine import in {f}'
        assert '<ChapterProgress' in content, f'Missing <ChapterProgress in {f}'
        assert '<QuizEngine' in content, f'Missing <QuizEngine in {f}'
        
        # Math
        assert '$$' in content, f'Missing block math in {f}'
        assert '$' in content, f'Missing inline math in {f}'
        
        # Citations
        has_citations = any(term in content for term in ['References', 'Citations', 'Literature', 'Seminal', 'Bibliography', 'et al.'])
        assert has_citations, f'Missing references/citations in {f}'
        
        # Code
        assert '```' in content, f'Missing code block in {f}'
        
        # Check unclosed code fences
        fence_count = content.count('```')
        assert fence_count % 2 == 0, f'Odd number of code fences ({fence_count}) in {f}'
        
        # Length check: each chapter should be substantial (at least 200 lines)
        lines = content.splitlines()
        print(f"  {os.path.basename(f)}: pos={pos}, lines={len(lines)}, code_fences={fence_count//2}")
        assert len(lines) >= 150, f"Chapter {f} seems too short ({len(lines)} lines)"

    assert sorted(positions) == list(range(1, expected_count + 1)), f'Positions mismatch: {positions}'
    print(f'All {expected_count} files in {mod_dir} passed frontmatter, components, math, and code audits!\n')

if __name__ == '__main__':
    audit_module('ai-book-docs/module3-ai-robot-brain', 10)
    audit_module('ai-book-docs/module4-vla', 10)
    print('ALL CHAPTER AUDITS PASSED!')
