import numpy as np

A=100.0
B=80.0
alpha=0.30
beta=0.40
E=0.05
k=8.0
L_0=0.35

def compute_policy_loss(N, D):
    return A / (N ** alpha) + B / (D ** beta) + E

def compute_success_rate(loss):
    return 1.0 / (1.0 + np.exp(k * (loss - L_0)))

target_s = 0.90
fixed_n = 7e9

# Invert sigmoid:
target_loss = L_0 - (1.0 / k) * np.log((1.0 / target_s) - 1.0)
print(f"target_loss: {target_loss}")

param_loss = A / (fixed_n ** alpha)
print(f"param_loss: {param_loss}")

remaining_loss = target_loss - param_loss - E
print(f"remaining_loss: {remaining_loss}")

required_hours = (B / remaining_loss) ** (1.0 / beta)
print(f"required_hours: {required_hours}")

loss = compute_policy_loss(fixed_n, required_hours)
print(f"actual loss: {loss}")

s = compute_success_rate(loss)
print(f"actual success rate: {s}")
