with open('backend/tests/test_adversarial_safety_capstone_m4.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_range(s, e):
    for i in range(s-1, e):
        print(f"{i+1}: {lines[i]}", end='')

print("=== 1. test_adversarial_11_2 ===")
print_range(213, 275)

print("\n=== 2. test_empirical_12_2 & test_adversarial_12_2 ===")
print_range(640, 715)

print("\n=== 3. test_adversarial_12_4 ===")
print_range(779, 830)

print("\n=== 4. test_adversarial_12_6 ===")
print_range(834, 885)
