with open('ai-book-docs/sidebar.ts', 'r', encoding='utf-8') as f:
    sidebar_content = f.read()

m10_files = [
    '10-1-humanoid-mechanical-design',
    '10-2-actuator-technologies',
    '10-3-power-electronics-and-motor-control',
    '10-4-communication-buses',
    '10-5-compute-platforms',
    '10-6-sensor-hardware',
    '10-7-real-time-embedded-software',
    '10-8-system-integration-and-testing',
]

m11_files = [
    '11-1-robot-safety-standards',
    '11-2-functional-safety-architecture',
    '11-3-human-robot-interaction-safety',
    '11-4-ethics-of-autonomous-humanoids',
    '11-5-privacy-and-data-governance',
    '11-6-deployment-operations',
]

m12_files = [
    '12-1-capstone-project-guide',
    '12-2-research-frontiers-locomotion',
    '12-3-research-frontiers-ai',
    '12-4-the-future-of-humanoid-robotics',
    '12-5-contributing-to-open-source',
    '12-6-reference-and-bibliography',
]

print("=== SIDEBAR VERIFICATION ===")
missing_sidebar = []
for f in m10_files:
    if f"module10-hardware-architecture/{f}" not in sidebar_content and f"module10/{f}" not in sidebar_content:
        missing_sidebar.append(f)

for f in m11_files:
    if f"module11-safety-ethics/{f}" not in sidebar_content and f"module11/{f}" not in sidebar_content:
        missing_sidebar.append(f)

for f in m12_files:
    if f"module12-capstone-frontiers/{f}" not in sidebar_content and f"module12/{f}" not in sidebar_content:
        missing_sidebar.append(f)

if missing_sidebar:
    print(f"Missing from sidebar: {missing_sidebar}")
else:
    print("ALL 20 CHAPTERS ARE PROPERLY REGISTERED IN ai-book-docs/sidebar.ts!")
