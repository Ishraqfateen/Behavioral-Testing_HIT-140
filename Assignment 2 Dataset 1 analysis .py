
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


df = pd.read_csv("merged_clean.csv")
no_risk = df.loc[df["risk"] == 0, "bat_landing_to_food"].dropna()
risk    = df.loc[df["risk"] == 1, "bat_landing_to_food"].dropna()

if len(no_risk) == 0 or len(risk) == 0:
    raise ValueError("One of the groups (risk=0 or risk=1) has no data after cleaning.")

def quick_stats(x):
    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "median": float(np.median(x)),
        "sd": float(np.std(x, ddof=1))
    }

stats_no = quick_stats(no_risk)
stats_yes = quick_stats(risk)

t_stat, p_val = stats.ttest_ind(no_risk, risk, equal_var=False)


print("=== Bat landing to food vs Risk ===")
print(f"risk=0  → n={stats_no['n']}, mean={stats_no['mean']:.2f}, median={stats_no['median']:.2f}, sd={stats_no['sd']:.2f}")
print(f"risk=1  → n={stats_yes['n']}, mean={stats_yes['mean']:.2f}, median={stats_yes['median']:.2f}, sd={stats_yes['sd']:.2f}")
print("\n--- Welch Two-Sample t-test ---")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value    : {p_val:.6f}")
if p_val < 0.05:
    print("Result     : Significant difference between risk groups.")
else:
    print("Result     : No significant difference between risk groups.")
plt.figure(figsize=(9,5))
plt.boxplot([no_risk, risk], labels=["No Risk (0)", "Risk (1)"])
plt.title("Bat landing to food time by risk")
plt.ylabel("Seconds")

plt.figure(figsize=(9,5))
plt.hist(no_risk, bins=30, alpha=0.55, label="No Risk (0)", edgecolor="black")
plt.hist(risk,    bins=30, alpha=0.55, label="Risk (1)",    edgecolor="black")
plt.xlabel("Bat landing to food (seconds)")
plt.ylabel("Frequency")
plt.title("Distribution of bat landing to food time")
plt.legend()
plt.tight_layout()
plt.show()

