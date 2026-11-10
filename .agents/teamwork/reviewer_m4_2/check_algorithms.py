import os
import re

chapters_to_check = [
    ("ai-book-docs/module10-hardware-architecture/10-3-power-electronics-and-motor-control.mdx", ["Clarke", "Park", "SVPWM", "FOC", "PI"]),
    ("ai-book-docs/module10-hardware-architecture/10-4-communication-buses.mdx", ["EtherCAT", "SOEM", "CST", "PDO", "DC", "jitter"]),
    ("ai-book-docs/module10-hardware-architecture/10-7-real-time-embedded-software.mdx", ["Rate Monotonic", "Liu", "Layland", "FreeRTOS", "priority inheritance"]),
    ("ai-book-docs/module11-safety-ethics/11-1-robot-safety-standards.mdx", ["ISO/TS 15066", "SSM", "separation distance", "T_r", "T_s"]),
    ("ai-book-docs/module11-safety-ethics/11-2-functional-safety-architecture.mdx", ["1oo2", "ISO 13849", "PL e", "STO", "cross-monitoring"]),
    ("ai-book-docs/module11-safety-ethics/11-3-human-robot-interaction-safety.mdx", ["Momentum Observer", "De Luca", "residual", "threshold"]),
    ("ai-book-docs/module11-safety-ethics/11-5-privacy-and-data-governance.mdx", ["Differential Privacy", "Laplace", "epsilon", "GDPR"]),
    ("ai-book-docs/module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx", ["Centroidal", "momentum", "friction cone", "landing"]),
    ("ai-book-docs/module12-capstone-frontiers/12-3-research-frontiers-ai.mdx", ["3D Gaussian", "Splat", "covariance", "ellipsoid"]),
    ("ai-book-docs/module12-capstone-frontiers/12-4-the-future-of-humanoid-robotics.mdx", ["scaling law", "power law", "Chinchilla", "success rate"])
]

print("=== CHECKING ALGORITHMIC RIGOR KEYWORDS & FORMULAS ===")
for path, keywords in chapters_to_check:
    print(f"\nChecking {os.path.basename(path)}:")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for kw in keywords:
        count = len(re.findall(re.escape(kw), text, re.IGNORECASE))
        print(f"  Keyword '{kw}': {count} occurrences")
