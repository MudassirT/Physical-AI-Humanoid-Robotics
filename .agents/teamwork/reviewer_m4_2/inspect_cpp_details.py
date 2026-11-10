import os
from verify_m4_deep import all_cpp_codes

print("=== CHECKING C++ CODE BLOCKS ===")
for fname, idx, code in all_cpp_codes:
    print(f"\n==========================================")
    print(f"FILE: {fname} (Block {idx})")
    print(f"==========================================")
    lines = code.split("\n")
    print(f"Total lines: {len(lines)}")
    # Print sample
    for l in lines[:25]:
        print("  " + l)
