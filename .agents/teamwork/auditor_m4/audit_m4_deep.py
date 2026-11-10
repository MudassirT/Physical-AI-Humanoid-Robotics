import os
import sys
import re
import json

MODULES = {
    'module10-hardware-architecture': [
        '10-1-humanoid-mechanical-design.mdx',
        '10-2-actuator-technologies.mdx',
        '10-3-power-electronics-and-motor-control.mdx',
        '10-4-communication-buses.mdx',
        '10-5-compute-platforms.mdx',
        '10-6-sensor-hardware.mdx',
        '10-7-real-time-embedded-software.mdx',
        '10-8-system-integration-and-testing.mdx',
    ],
    'module11-safety-ethics': [
        '11-1-robot-safety-standards.mdx',
        '11-2-functional-safety-architecture.mdx',
        '11-3-human-robot-interaction-safety.mdx',
        '11-4-ethics-of-autonomous-humanoids.mdx',
        '11-5-privacy-and-data-governance.mdx',
        '11-6-deployment-operations.mdx',
    ],
    'module12-capstone-frontiers': [
        '12-1-capstone-project-guide.mdx',
        '12-2-research-frontiers-locomotion.mdx',
        '12-3-research-frontiers-ai.mdx',
        '12-4-the-future-of-humanoid-robotics.mdx',
        '12-5-contributing-to-open-source.mdx',
        '12-6-reference-and-bibliography.mdx',
    ]
}

def analyze_chapter(mod, filename):
    filepath = os.path.join('ai-book-docs', mod, filename)
    if not os.path.exists(filepath):
        return {'error': f'File not found: {filepath}'}

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Total raw word count
    words = content.split()
    total_words = len(words)

    # Frontmatter extraction
    fm = {}
    fm_match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', content, re.DOTALL)
    body = content
    if fm_match:
        fm_raw = fm_match.group(1)
        body = content[fm_match.end():]
        for line in fm_raw.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip().strip('"\'')

    # Frontmatter requirements
    sidebar_pos = fm.get('sidebar_position')
    title = fm.get('title')
    description = fm.get('description')
    fm_valid = bool(sidebar_pos and title and description)

    # Component checks
    has_cp_import = bool(re.search(r'import\s+ChapterProgress\s+from', content))
    has_cp_tag = bool(re.search(r'<ChapterProgress\s*/>', content))
    has_qe_import = bool(re.search(r'import\s+QuizEngine\s+from', content))
    has_qe_tag = bool(re.search(r'<QuizEngine', content))

    # QuizEngine details
    # Match questions={[ ... ]}
    quiz_questions = []
    # Find all question blocks
    q_matches = re.findall(r'\{\s*id:\s*[\'\"]([^\'\"]+)[\'\"],\s*question:\s*[\'\"](.*?)[\'\"],\s*options:\s*(\[.*?\]),\s*correctAnswer:\s*(\d+),\s*explanation:\s*[\'\"](.*?)[\'\"]\s*\}', content, re.DOTALL)
    
    quiz_details = []
    for q in q_matches:
        q_id, q_text, opts_raw, correct_idx, expl = q
        try:
            # Parse options
            opts = re.findall(r'[\'\"](.*?)[\'\"]', opts_raw)
        except Exception:
            opts = []
        quiz_details.append({
            'id': q_id,
            'question': q_text,
            'options_count': len(opts),
            'correctAnswer': int(correct_idx),
            'explanation_len': len(expl),
            'explanation_words': len(expl.split())
        })

    # Code blocks
    # pattern for code blocks
    code_blocks_raw = re.findall(r'```([a-zA-Z0-9_\-\+]*)\r?\n(.*?)\r?\n```', content, re.DOTALL)
    code_blocks = []
    suspicious_code = []

    for lang, code in code_blocks_raw:
        code_words = len(code.split())
        lines = code.splitlines()
        
        # Check for facade / stub patterns:
        # e.g., only pass, only TODO, simulated print
        has_todo = bool(re.search(r'\b(TODO|FIXME|XXX|TBD)\b', code))
        has_bare_pass = bool(re.search(r'^\s*pass\s*$', code, re.MULTILINE))
        has_stub_func = bool(re.search(r'def\s+\w+\([^)]*\):\s*(?:pass|\.\.\.)', code))
        has_ellipsis = bool(re.search(r'^\s*\.\.\.\s*$', code, re.MULTILINE))
        has_not_implemented = bool(re.search(r'raise\s+NotImplementedError', code))
        
        flags = []
        if has_todo:
            flags.append('TODO')
        if has_bare_pass:
            flags.append('bare_pass')
        if has_stub_func:
            flags.append('stub_function')
        if has_ellipsis:
            flags.append('ellipsis')
        if has_not_implemented:
            flags.append('NotImplementedError')

        code_info = {
            'lang': lang,
            'lines': len(lines),
            'words': code_words,
            'flags': flags
        }
        code_blocks.append(code_info)
        if flags:
            suspicious_code.append({
                'lang': lang,
                'flags': flags,
                'snippet': code[:200]
            })

    # Math formulas
    inline_math = re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', content)
    block_math = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)

    # Citations
    citations = re.findall(r'\[(?:[A-Z][a-z]+(?:\s+et\s+al\.)?,\s*\d{4}|\d+)\]|\b(?:arXiv:\d+\.\d+|doi:\S+)', content)

    # Prose word count (excluding code blocks and frontmatter)
    content_no_code = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    content_no_jsx = re.sub(r'<[^>]+>', '', content_no_code)
    prose_words = len(content_no_jsx.split())

    return {
        'filename': filename,
        'module': mod,
        'total_words': total_words,
        'prose_words': prose_words,
        'frontmatter': fm,
        'frontmatter_valid': fm_valid,
        'sidebar_position': sidebar_pos,
        'title': title,
        'description': description,
        'components': {
            'chapter_progress': has_cp_import and has_cp_tag,
            'quiz_engine': has_qe_import and has_qe_tag,
            'quiz_questions_parsed': len(quiz_details),
            'quiz_questions': quiz_details
        },
        'code_blocks_count': len(code_blocks),
        'code_blocks': code_blocks,
        'suspicious_code': suspicious_code,
        'math': {
            'inline_count': len(inline_math),
            'block_count': len(block_math)
        },
        'citations_count': len(citations)
    }

def main():
    all_results = {}
    summary = {
        'total_chapters': 0,
        'total_words': 0,
        'min_words': 999999,
        'max_words': 0,
        'chapters_under_1800': [],
        'chapters_missing_cp': [],
        'chapters_missing_qe': [],
        'chapters_invalid_fm': [],
        'suspicious_code_count': 0,
        'modules': {}
    }

    for mod, files in MODULES.items():
        all_results[mod] = []
        mod_words = 0
        for f in files:
            res = analyze_chapter(mod, f)
            all_results[mod].append(res)
            
            tw = res.get('total_words', 0)
            summary['total_chapters'] += 1
            summary['total_words'] += tw
            mod_words += tw
            if tw < summary['min_words']:
                summary['min_words'] = tw
            if tw > summary['max_words']:
                summary['max_words'] = tw
            if tw < 1800:
                summary['chapters_under_1800'].append({'file': f, 'words': tw})

            if not res.get('frontmatter_valid'):
                summary['chapters_invalid_fm'].append(f)
            if not res.get('components', {}).get('chapter_progress'):
                summary['chapters_missing_cp'].append(f)
            if not res.get('components', {}).get('quiz_engine'):
                summary['chapters_missing_qe'].append(f)
            if res.get('suspicious_code'):
                summary['suspicious_code_count'] += len(res['suspicious_code'])

        summary['modules'][mod] = {
            'chapters': len(files),
            'total_words': mod_words,
            'avg_words_per_chapter': round(mod_words / len(files), 1)
        }

    summary['avg_words_overall'] = round(summary['total_words'] / summary['total_chapters'], 1)

    output = {
        'summary': summary,
        'details': all_results
    }

    out_path = os.path.join('.agents', 'teamwork', 'auditor_m4', 'audit_metrics.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Audit completed. Total chapters: {summary['total_chapters']}")
    print(f"Total words: {summary['total_words']}, Avg: {summary['avg_words_overall']}")
    print(f"Min words: {summary['min_words']}, Max words: {summary['max_words']}")
    print(f"Chapters under 1800 words: {len(summary['chapters_under_1800'])}")
    print(f"Chapters missing ChapterProgress: {len(summary['chapters_missing_cp'])}")
    print(f"Chapters missing QuizEngine: {len(summary['chapters_missing_qe'])}")
    print(f"Chapters invalid frontmatter: {len(summary['chapters_invalid_fm'])}")
    print(f"Suspicious code occurrences: {summary['suspicious_code_count']}")
    print("Module stats:")
    for m, s in summary['modules'].items():
        print(f"  {m}: {s['chapters']} ch, {s['total_words']} words, avg {s['avg_words_per_chapter']}")

if __name__ == '__main__':
    main()
