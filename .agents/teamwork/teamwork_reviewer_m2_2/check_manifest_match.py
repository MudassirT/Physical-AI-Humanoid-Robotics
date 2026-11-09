import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path("backend").resolve()))

from tests.e2e.curriculum_manifest import CHAPTERS

m3_specs = [c for c in CHAPTERS if c.module_id == "module3"]
m4_specs = [c for c in CHAPTERS if c.module_id == "module4"]

print(f"M3 specs in manifest: {len(m3_specs)}")
print(f"M4 specs in manifest: {len(m4_specs)}")

root = Path(".")

for spec in m3_specs + m4_specs:
    p = root / spec.relative_path
    assert p.exists(), f"File does not exist: {p}"
    content = p.read_text(encoding="utf-8")
    assert spec.expected_title_fragment.lower() in content.lower(), f"Expected title fragment '{spec.expected_title_fragment}' not in {p}"
    print(f"Matched {spec.relative_path}: title fragment '{spec.expected_title_fragment}' verified.")

print("All manifest specs for M3 and M4 verified successfully!")
