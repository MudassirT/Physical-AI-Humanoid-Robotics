import os
import ast
from verify_m4_deep import all_python_codes, all_cpp_codes

print("=== INSPECTING PYTHON CODE BLOCKS ===")
for fname, idx, code in all_python_codes:
    print(f"\n--- {fname} (Block {idx}) ---")
    lines = code.strip().split('\n')
    print(f"Lines of code: {len(lines)}")
    print(f"First 3 lines:\n  " + "\n  ".join(lines[:3]))
    # parse AST
    tree = ast.parse(code)
    # Check imported modules
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    print(f"Imports: {set(imports)}")

print("\n=== INSPECTING C++ CODE BLOCKS ===")
for fname, idx, code in all_cpp_codes:
    print(f"\n--- {fname} (C++ Block {idx}) ---")
    lines = code.strip().split('\n')
    print(f"Lines of code: {len(lines)}")
    print(f"First 5 lines:\n  " + "\n  ".join(lines[:5]))
