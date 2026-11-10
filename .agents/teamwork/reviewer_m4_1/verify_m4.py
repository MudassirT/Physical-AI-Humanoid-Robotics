import os
import re
import json
import yaml
from pathlib import Path

BASE_DIR = Path(r"C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main")
DOCS_DIR = BASE_DIR / "ai-book-docs"

M4_MODULES = [
    ("module10-hardware-architecture", 8, "10-", 10),
    ("module11-safety-ethics", 6, "11-", 11),
    ("module12-capstone-frontiers", 6, "12-", 12),
]

def check_m4():
    print("=" * 70)
    print("AUDITING MILESTONE M4 CHAPTERS AND CATEGORIES")
    print("=" * 70)
    
    total_files = 0
    errors = []
    warnings = []
    
    # 1. Check _category_.json files
    for mod_dir, expected_chaps, prefix, mod_pos in M4_MODULES:
        cat_file = DOCS_DIR / mod_dir / "_category_.json"
        if not cat_file.exists():
            errors.append(f"Missing _category_.json in {mod_dir}")
        else:
            try:
                data = json.loads(cat_file.read_text(encoding="utf-8"))
                if "label" not in data or "position" not in data:
                    errors.append(f"Invalid _category_.json schema in {mod_dir}: missing label or position")
                elif data["position"] != mod_pos:
                    errors.append(f"Incorrect position in {mod_dir}/_category_.json: expected {mod_pos}, got {data['position']}")
                else:
                    print(f"[OK] Category file: {mod_dir}/_category_.json (label: '{data['label']}', pos: {data['position']})")
            except Exception as e:
                errors.append(f"Error parsing {cat_file}: {e}")

    # 2. Check all chapters
    for mod_dir, expected_count, prefix, mod_pos in M4_MODULES:
        folder = DOCS_DIR / mod_dir
        mdx_files = sorted([f for f in folder.glob("*.mdx") if f.name.startswith(prefix)])
        print(f"\nChecking {mod_dir}: found {len(mdx_files)} chapters (expected {expected_count})")
        if len(mdx_files) != expected_count:
            errors.append(f"{mod_dir}: Expected {expected_count} chapters, found {len(mdx_files)}")
            
        for f in mdx_files:
            total_files += 1
            content = f.read_text(encoding="utf-8")
            fname = f.name
            
            # --- Frontmatter Check ---
            fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
            if not fm_match:
                errors.append(f"{fname}: Missing or malformed YAML frontmatter")
            else:
                fm_raw = fm_match.group(1)
                try:
                    fm = yaml.safe_load(fm_raw)
                    if "sidebar_position" not in fm:
                        errors.append(f"{fname}: Frontmatter missing 'sidebar_position'")
                    if "title" not in fm or not str(fm["title"]).strip():
                        errors.append(f"{fname}: Frontmatter missing or empty 'title'")
                    if "description" not in fm or not str(fm["description"]).strip():
                        errors.append(f"{fname}: Frontmatter missing or empty 'description'")
                except Exception as e:
                    errors.append(f"{fname}: YAML parse error: {e}")

            # --- Integrity / Quality / Length Check ---
            lines = content.splitlines()
            word_count = len(re.findall(r"\w+", content))
            if word_count < 800:
                errors.append(f"{fname}: Word count too low ({word_count} words). Possible facade/stub.")
            
            # Check for dummy placeholders in non-code prose
            content_prose = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
            dummy_patterns = [r"\bTODO\b", r"\bTBD\b", r"Lorem ipsum", r"fill this in", r"\bplaceholder\b"]
            for pat in dummy_patterns:
                matches = re.findall(pat, content_prose, re.IGNORECASE)
                if matches:
                    warnings.append(f"{fname}: Found placeholder pattern '{pat}' {len(matches)} times in prose")

            # --- Interactive Components Check ---
            has_cp_import = bool(re.search(r"import\s+.*ChapterProgress.*from\s+['\"][^'\"]*ChapterProgress['\"]", content))
            has_cp_render = bool(re.search(r"<ChapterProgress\b[^>]*\/>", content))
            has_qe_import = bool(re.search(r"import\s+.*QuizEngine.*from\s+['\"][^'\"]*QuizEngine['\"]", content))
            has_qe_render = bool(re.search(r"<QuizEngine\b", content))
            
            if not has_cp_import:
                errors.append(f"{fname}: Missing ChapterProgress import")
            if not has_cp_render:
                errors.append(f"{fname}: Missing <ChapterProgress /> render")
            if not has_qe_import:
                errors.append(f"{fname}: Missing QuizEngine import")
            if not has_qe_render:
                errors.append(f"{fname}: Missing <QuizEngine /> render")

            # Detailed QuizEngine structure check
            qe_match = re.search(r"<QuizEngine\b(.*?)/>", content, re.DOTALL)
            question_count = 0
            if not qe_match:
                errors.append(f"{fname}: Could not locate <QuizEngine ... /> block")
            else:
                qe_body = qe_match.group(1)
                # Count questions by "id:" or "question:"
                id_count = len(re.findall(r"id:\s*['\"]", qe_body))
                question_count = len(re.findall(r"question:\s*['\"]", qe_body))
                options_count = len(re.findall(r"options:\s*\[", qe_body))
                ans_count = len(re.findall(r"(?:correctIndex|correctAnswer):\s*\d+", qe_body))
                exp_count = len(re.findall(r"explanation:\s*['\"]", qe_body))
                
                if question_count < 2:
                    errors.append(f"{fname}: QuizEngine has only {question_count} question(s) (expected >= 2)")
                if not (id_count == question_count == options_count == ans_count == exp_count):
                    warnings.append(f"{fname}: QuizEngine property count mismatch: id={id_count}, q={question_count}, opt={options_count}, ans={ans_count}, exp={exp_count}")

            # --- KaTeX and Math Check ---
            code_fence_count = len(re.findall(r"^```", content, re.MULTILINE))
            if code_fence_count % 2 != 0:
                errors.append(f"{fname}: Odd number of code fence markers (```) ({code_fence_count})")

            # Remove code fences and inline backticks to inspect math
            content_no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
            content_no_code = re.sub(r"`[^`\n]+`", "", content_no_code)

            # Block math $$
            double_dollar_count = len(re.findall(r"\$\$", content_no_code))
            if double_dollar_count % 2 != 0:
                errors.append(f"{fname}: Odd number of $$ block math delimiters ({double_dollar_count})")

            # Check single dollar inline math $
            content_no_double_dollar = re.sub(r"\$\$.*?\$\$", "", content_no_code, flags=re.DOTALL)
            single_dollar_count = len(re.findall(r"(?<!\\)\$", content_no_double_dollar))
            if single_dollar_count % 2 != 0:
                warnings.append(f"{fname}: Odd number of single $ math delimiters ({single_dollar_count})")

            # --- Citations / References Check ---
            has_refs = bool(re.search(r"##.*(?:References|Literature|Bibliography|Further\s*Reading|Citations)", content, re.IGNORECASE))
            if not has_refs:
                errors.append(f"{fname}: Missing References / Bibliography section")

            print(f"  [OK] {fname}: {word_count} words | {code_fence_count // 2} code blocks | $$ math: {double_dollar_count} | Quiz Qs: {question_count}")

    print("\n" + "=" * 70)
    print(f"AUDIT SUMMARY: Checked {total_files} chapters across 3 modules.")
    print(f"Errors found: {len(errors)}")
    print(f"Warnings found: {len(warnings)}")
    print("=" * 70)
    
    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  ❌ {e}")
            
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠️ {w}")

if __name__ == "__main__":
    check_m4()
