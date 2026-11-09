import glob
import re
from pathlib import Path

def test_all_python_blocks():
    files = sorted(glob.glob("ai-book-docs/module3-ai-robot-brain/*.mdx") + glob.glob("ai-book-docs/module4-vla/*.mdx"))
    
    results = {}
    for f in files:
        fname = Path(f).name
        txt = Path(f).read_text(encoding="utf-8")
        blocks = re.findall(r"```python\n(.*?)```", txt, re.DOTALL)
        for i, code in enumerate(blocks):
            key = f"{fname} [block {i+1}]"
            try:
                # Compile code
                compiled = compile(code, f"<{key}>", "exec")
                # Try to execute
                exec(compiled, {"__name__": "__main__"})
                results[key] = "PASS (executed cleanly)"
            except ModuleNotFoundError as e:
                results[key] = f"SKIP (missing dependency: {e})"
            except Exception as e:
                results[key] = f"ERROR ({type(e).__name__}: {e})"

    print("\n=== SUMMARY OF CODE EXECUTION RESULTS ===")
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_all_python_blocks()
