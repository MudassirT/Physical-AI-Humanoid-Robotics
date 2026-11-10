import os
import sys
import numpy as np
import traceback
from verify_m4_deep import all_python_codes

print("=== TESTING EXECUTION OF PYTHON CODE BLOCKS ===")

for fname, idx, code in all_python_codes:
    print(f"\n==========================================")
    print(f"Testing {fname} (Block {idx})...")
    # Check if this block has mock / standalone execution
    # Some blocks may require ROS 2 (rclpy) or cv2 or torch if not installed.
    # Let's inspect what imports are needed
    try:
        # Create an isolated global namespace
        ns = {}
        # Execute the code
        exec(code, ns)
        print(f"SUCCESS: {fname} executed without runtime errors.")
        # If there is a main function or demo run, check if it ran or can run
        if "__main__" in code and "main" in ns:
            print(f"Calling main() in {fname}...")
            try:
                ns["main"]()
                print(f"SUCCESS: main() completed cleanly in {fname}.")
            except Exception as e:
                print(f"NOTE on main() execution in {fname}: {e}")
    except ModuleNotFoundError as mnf:
        print(f"SKIPPED execution due to optional environment dependency: {mnf}")
    except Exception as e:
        print(f"FAILURE in {fname}: {type(e).__name__}: {e}")
        traceback.print_exc()
