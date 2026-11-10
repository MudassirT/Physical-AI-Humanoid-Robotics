import re
from pathlib import Path

BASE_DIR = Path(r"C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main")
DOCS_DIR = BASE_DIR / "ai-book-docs"

M4_DIRS = [
    "module10-hardware-architecture",
    "module11-safety-ethics",
    "module12-capstone-frontiers",
]

def check_links():
    print("Checking markdown links in M4 chapters...")
    broken_links = []
    
    # Collect all existing docs in ai-book-docs
    all_docs = {}
    for p in DOCS_DIR.rglob("*.mdx"):
        rel = p.relative_to(DOCS_DIR).as_posix()
        all_docs[rel] = p
        all_docs[p.stem] = p
    for p in DOCS_DIR.rglob("*.md"):
        rel = p.relative_to(DOCS_DIR).as_posix()
        all_docs[rel] = p
        all_docs[p.stem] = p
        
    for mdir in M4_DIRS:
        folder = DOCS_DIR / mdir
        for fpath in folder.glob("*.mdx"):
            content = fpath.read_text(encoding="utf-8")
            fname = fpath.name
            
            # Remove code fences
            content_no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
            
            # Find markdown links: [text](target)
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content_no_code)
            for text, target in links:
                target = target.strip()
                # Skip external links
                if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:") or target.startswith("#"):
                    continue
                # Remove anchor
                target_base = target.split("#")[0]
                if not target_base:
                    continue
                
                # Check if file exists relative to fpath or ai-book-docs
                resolved = False
                target_rel = (fpath.parent / target_base).resolve()
                if target_rel.exists() or (target_rel.with_suffix(".mdx").exists()) or (target_rel.with_suffix(".md").exists()):
                    resolved = True
                if not resolved:
                    target_docs = (DOCS_DIR / target_base.lstrip("/")).resolve()
                    if target_docs.exists() or (target_docs.with_suffix(".mdx").exists()) or (target_docs.with_suffix(".md").exists()):
                        resolved = True
                if not resolved and target_base.startswith("/ai-book/"):
                    clean = target_base[len("/ai-book/"):]
                    target_docs = (DOCS_DIR / clean).resolve()
                    if target_docs.exists() or (target_docs.with_suffix(".mdx").exists()) or (target_docs.with_suffix(".md").exists()):
                        resolved = True
                    if clean.startswith("category/"):
                        resolved = True
                        
                if not resolved:
                    broken_links.append(f"{fname}: Broken link target '{target}' (text: '{text}')")
                    
    print(f"Link check complete. Broken links found: {len(broken_links)}")
    for bl in broken_links:
        print(f"  ❌ {bl}")

if __name__ == "__main__":
    check_links()
