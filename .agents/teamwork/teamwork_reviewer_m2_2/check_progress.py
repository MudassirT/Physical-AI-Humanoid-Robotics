import glob
import re
from pathlib import Path

def validate_progress():
    files = sorted(glob.glob("ai-book-docs/module3-ai-robot-brain/*.mdx") + glob.glob("ai-book-docs/module4-vla/*.mdx"))
    
    for f in files:
        txt = Path(f).read_text(encoding="utf-8")
        stem = Path(f).stem
        
        # Match <ChapterProgress ... />
        prog_match = re.search(r'<ChapterProgress\s+([^>]+)/>', txt)
        assert prog_match, f"Missing <ChapterProgress in {f}"
        props = prog_match.group(1)
        
        cid_match = re.search(r'chapterId="([^"]+)"', props)
        assert cid_match, f"Missing chapterId in {f}"
        cid = cid_match.group(1)
        assert cid == stem, f"chapterId mismatch in {f}: '{cid}' != '{stem}'"
        
        mod_match = re.search(r'moduleId="([^"]+)"', props)
        assert mod_match, f"Missing moduleId in {f}"
        mod = mod_match.group(1)
        expected_mod = "module3" if "module3" in f else "module4"
        assert mod == expected_mod, f"moduleId mismatch in {f}: '{mod}' != '{expected_mod}'"
        
        tot_match = re.search(r'totalChapters=\{?(\d+)\}?', props)
        assert tot_match, f"Missing totalChapters in {f}"
        tot = int(tot_match.group(1))
        assert tot == 10, f"totalChapters mismatch in {f}: {tot} != 10"
        
        print(f"[PASS] {stem}: ChapterProgress(chapterId='{cid}', moduleId='{mod}', totalChapters={tot})")

    print(f"\nAll 20 ChapterProgress components strictly conform to contract!")

if __name__ == "__main__":
    validate_progress()
