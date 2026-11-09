import os
import glob
import re
import yaml

modules = [
    "ai-book-docs/module1-ros2",
    "ai-book-docs/module2-digital-twin",
    "ai-book-docs/module3-ai-robot-brain",
    "ai-book-docs/module4-vla",
]

total_files = 0
results = []
suspicious = []

for mod in modules:
    files = sorted(glob.glob(os.path.join(mod, "*.mdx")))
    for f in files:
        total_files += 1
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            
        # Frontmatter
        fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
        fm_ok = False
        title = ""
        sidebar_pos = None
        if fm_match:
            try:
                fm_data = yaml.safe_load(fm_match.group(1))
                if isinstance(fm_data, dict) and "title" in fm_data and "sidebar_position" in fm_data:
                    fm_ok = True
                    title = fm_data.get("title", "")
                    sidebar_pos = fm_data.get("sidebar_position")
            except Exception as e:
                fm_ok = False
        
        # Math checks
        block_math = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
        no_blocks = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        no_blocks = re.sub(r"\$\$.*?\$\$", "", no_blocks, flags=re.DOTALL)
        inline_math = re.findall(r"\$([^\$\n]+?)\$", no_blocks)
        
        # Delimiter balance check
        clean_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        clean_content = re.sub(r"`.*?`", "", clean_content)
        dollar_count = clean_content.count("$")
        
        # Code blocks
        code_blocks = re.findall(r"```([a-zA-Z0-9_\-+]*)\r?\n(.*?)```", content, re.DOTALL)
        
        # Citations pattern: [1], [2], (Author et al., Year), etc.
        citations = re.findall(r"(\[[0-9]+\]|\([A-Z][a-zA-Z\s]+et al\.,?\s+[12][0-9]{3}\)|\[@[a-zA-Z0-9_]+\])", content)
        
        # Hardware keywords
        hw_keywords = ["EtherCAT", "CAN-FD", "CAN", "RS-485", "Jetson", "Orin", "GPU", "FPGA", "MCU", "IMU", "LiDAR", "Micro-ROS", "STM32", "NVIDIA", "ARM", "Cortex", "Sensor", "Actuator", "FOC", "BLDC"]
        hw_found = [kw for kw in hw_keywords if re.search(r"\b" + re.escape(kw) + r"\b", content, re.I)]
        
        # Suspicious patterns
        flags = []
        for pat in [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"Lorem ipsum", r"\bPlaceholder\b", r"\bComing soon\b"]:
            m = re.findall(pat, content, re.I)
            if m:
                flags.append(f"{pat} ({len(m)})")
                
        r = {
            "file": os.path.basename(f),
            "dir": os.path.basename(mod),
            "length": len(content),
            "lines": len(content.splitlines()),
            "fm_ok": fm_ok,
            "title": title,
            "sidebar_pos": sidebar_pos,
            "block_math_count": len(block_math),
            "inline_math_count": len(inline_math),
            "dollar_count": dollar_count,
            "dollar_even": (dollar_count % 2 == 0),
            "code_block_count": len(code_blocks),
            "citations_count": len(citations),
            "hw_count": len(hw_found),
            "flags": flags
        }
        results.append(r)
        if flags or not fm_ok or not (dollar_count % 2 == 0) or len(content) < 3000:
            suspicious.append((f, r))

print(f"Total MDX chapters audited in M1-M4: {total_files}")
print(f"Suspicious files count: {len(suspicious)}")
for r in results:
    flag_str = f" FLAGS: {r['flags']}" if r["flags"] else ""
    even_str = "OK" if r["dollar_even"] else f"UNEVEN({r['dollar_count']})"
    print(f"[{r['dir']}] {r['file']}: {r['length']} B, {r['lines']} lines | FM: {r['fm_ok']} pos={r['sidebar_pos']} | Math: {r['block_math_count']} block, {r['inline_math_count']} inline (${even_str}) | Code: {r['code_block_count']} | Refs: {r['citations_count']} | HW: {r['hw_count']}{flag_str}")

if suspicious:
    print("\n--- SUSPICIOUS DETAILS ---")
    for path, r in suspicious:
        print(f"SUSPICIOUS: {path} -> {r}")
