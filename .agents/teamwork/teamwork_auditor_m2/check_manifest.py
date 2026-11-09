import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path("backend").resolve()))

from tests.e2e.curriculum_manifest import CHAPTERS, MODULES

m1_m4_chapters = [ch for ch in CHAPTERS if ch.module_id in {"module1", "module2", "module3", "module4"}]

print(f"Total expected M1-M4 chapters in manifest: {len(m1_m4_chapters)}")
missing = []
present = []

for ch in m1_m4_chapters:
    p = Path(ch.relative_path)
    if not p.exists():
        missing.append(ch)
    else:
        present.append((ch, p.stat().st_size))

print(f"Present on disk: {len(present)}")
print(f"Missing from disk: {len(missing)}")

if missing:
    print("MISSING CHAPTERS:")
    for ch in missing:
        print(f"  - {ch.module_id}: {ch.filename}")
else:
    print("ALL 44 CHAPTERS IN MODULES 1-4 EXIST ON DISK!")
    for ch, sz in present:
        print(f"  OK: {ch.module_id:10} | {ch.filename:42} | Size: {sz:6} B | Milestone: {ch.milestone}")
