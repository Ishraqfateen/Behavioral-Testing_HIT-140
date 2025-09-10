import pandas as pd
import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt

df = pd.read_csv("merged_grouped.csv")
df = df.dropna(subset=['bat_landing_number', 'rat_present'])

grp_present = df[df['rat_present'] == 1]['bat_landing_number'].values
grp_absent  = df[df['rat_present'] == 0]['bat_landing_number'].values

n1, n0 = len(grp_present), len(grp_absent)
mean1, mean0 = np.mean(grp_present), np.mean(grp_absent)
var1, var0 = np.var(grp_present, ddof=1), np.var(grp_absent, ddof=1)

print(f"Group sizes → Rats Present: {n1}, Rats Absent: {n0}")
print(f"Mean (Rats Present): {mean1:.2f}")
print(f"Mean (Rats Absent): {mean0:.2f}")

t_stat, p_val = stats.ttest_ind(grp_present, grp_absent, equal_var=True)
df_ttest = n1 + n0 - 2
sp = math.sqrt(((n1 - 1)*var1 + (n0 - 1)*var0) / df_ttest)
se_diff = sp * math.sqrt((1/n1) + (1/n0))
mean_diff = mean1 - mean0
t_crit = stats.t.ppf(0.975, df_ttest)
ci_low = mean_diff - t_crit * se_diff
ci_high = mean_diff + t_crit * se_diff

print("\n=== Two-Sample T-Test Results ===")
print(f"T-statistic: {t_stat:.4f}")
print(f"Degrees of Freedom: {df_ttest}")
print(f"P-value: {p_val:.6f}")
print(f"Mean Difference (Present - Absent): {mean_diff:.3f}")
print(f"95% Confidence Interval: [{ci_low:.3f}, {ci_high:.3f}]")

if p_val < 0.05:
    print("Result: Significant difference between groups.")
else:
    print("Result: No significant difference between groups.")

if ci_low > 0:
    print("Bats are more active when rats are present.")
elif ci_high < 0:
    print("Bats are less active when rats are present.")
else:
    print("CI includes zero → No clear evidence of change in bat activity.")

means = [mean0, mean1]

se0 = math.sqrt(var0 / n0)
se1 = math.sqrt(var1 / n1)
tcrit0 = stats.t.ppf(0.975, n0 - 1)
tcrit1 = stats.t.ppf(0.975, n1 - 1)
ci0 = tcrit0 * se0
ci1 = tcrit1 * se1
ci_errs = [[0, 0], [0, 0]] 
yerr = np.array([[ci0, ci1], [ci0, ci1]])  

plt.figure(figsize=(7, 5))
plt.bar([0, 1], means, yerr=[ci0, ci1], capsize=6)
plt.xticks([0, 1], ['Rats Absent (0)', 'Rats Present (1)'])
plt.ylabel('Mean bat landings per 30-min bin')
plt.title('Bat Activity by Rat Presence (Mean ± 95% CI)')
annot = f"t({df_ttest}) = {t_stat:.2f}, p = {p_val:.4g}\nΔ = {mean_diff:.2f}  (95% CI [{ci_low:.2f}, {ci_high:.2f}])"
plt.gcf().text(0.5, -0.12, annot, ha='center', va='top')
plt.tight_layout()
plt.savefig("bat_vs_rat_bar_ci.png", dpi=200, bbox_inches="tight")
plt.show()


