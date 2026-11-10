import re
from pathlib import Path

BASE_DIR = Path(r"C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main")
DOCS_DIR = BASE_DIR / "ai-book-docs"

M4_DIRS = [
    "module10-hardware-architecture",
    "module11-safety-ethics",
    "module12-capstone-frontiers",
]

def check_mdx_tables_and_syntax():
    print("Checking markdown tables and MDX syntax...")
    issues = []
    
    for mdir in M4_DIRS:
        folder = DOCS_DIR / mdir
        for fpath in folder.glob("*.mdx"):
            content = fpath.read_text(encoding="utf-8")
            fname = fpath.name
            lines = content.splitlines()
            
            in_code_block = False
            in_table = False
            table_header_cols = 0
            
            for line_idx, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                
                # Check markdown table
                if stripped.startswith("|") and stripped.endswith("|"):
                    # Table row
                    # Split cells by unescaped pipe
                    # First remove backticked expressions
                    clean_line = re.sub(r"`[^`]+`", "CODE", stripped)
                    pipes = clean_line.count("|")
                    cols = pipes - 1
                    
                    # If this is table separator row: |---|---|
                    if re.match(r"^\|(\s*:?-+:?\s*\|)+$", stripped):
                        pass
                    elif not in_table:
                        in_table = True
                        table_header_cols = cols
                    else:
                        if cols != table_header_cols:
                            issues.append(f"{fname}:{line_idx}: Table column mismatch: expected {table_header_cols}, got {cols} cols: {stripped[:50]}")
                else:
                    in_table = False

                # Check unescaped JSX curlies in headings or plain paragraphs
                # Exclude <ChapterProgress ... />, <QuizEngine ... />, import statements, export
                if not in_code_block and not stripped.startswith("<") and not stripped.startswith("import") and not stripped.startswith("export"):
                    # Check if there is an unescaped { not part of an inline code backtick or math $
                    # Remove inline code
                    line_no_code = re.sub(r"`[^`]+`", "", stripped)
                    # Remove inline math $...$
                    line_no_math = re.sub(r"\$[^$]+\$", "", line_no_code)
                    # Check for { without closing or JSX expression
                    # Note: KaTeX in $$ block is already excluded if in_code_block, but if $$ spans multiple lines:
                    # Docusaurus remark-math handles $$ on separate lines.
            
    print(f"Table and syntax check complete. Issues found: {len(issues)}")
    for iss in issues:
        print(f"  ❌ {iss}")

if __name__ == "__main__":
    check_mdx_tables_and_syntax()
