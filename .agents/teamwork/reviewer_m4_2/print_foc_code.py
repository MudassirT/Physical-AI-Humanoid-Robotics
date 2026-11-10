from verify_m4_deep import all_cpp_codes

for fname, idx, code in all_cpp_codes:
    if "10-3" in fname:
        print(code)
