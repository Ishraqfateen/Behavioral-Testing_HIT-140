import pandas as pd
import numpy as np
from scipy import stats
import math

# Load dataset
df = pd.read_csv("merged_grouped.csv")

# Drop NaNs in required columns
df = df.dropna(subset=['bat_landing_number', 'rat_present'])

# Split into groups
grp_present = df[df['rat_present'] == 1]['bat_landing_number'].values
grp_absent = df[df['rat_present'] == 0]['bat_landing_number'].values

n1, n0 = len(grp_present), len(grp_absent)
mean1, mean0 = np.mean(grp_present), np.mean(grp_absent)
var1, var0 = np.var(grp_present, ddof=1), np.var(grp_absent, ddof=1)

print(f"Group sizes → Rats Present: {n1}, Rats Absent: {n0}")
print(f"Mean (Rats Present): {mean1:.2f}")
print(f"Mean (Rats Absent): {mean0:.2f}")

# Run standard 2-sample t-test assuming equal variance
t_stat, p_val = stats.ttest_ind(grp_present, grp_absent, equal_var=True)

# Degrees of freedom
df_ttest = n1 + n0 - 2

# Calculate pooled standard deviation
sp = math.sqrt(((n1 - 1)*var1 + (n0 - 1)*var0) / df_ttest)

# Standard error of the difference
se_diff = sp * math.sqrt((1/n1) + (1/n0))

# 95% CI for difference
mean_diff = mean1 - mean0
t_crit = stats.t.ppf(0.975, df_ttest)  # two-tailed, alpha = 0.05
ci_low = mean_diff - t_crit * se_diff
ci_high = mean_diff + t_crit * se_diff

print("\n=== Two-Sample T-Test Results ===")
print(f"T-statistic: {t_stat:.4f}")
print(f"Degrees of Freedom: {df_ttest}")
print(f"P-value: {p_val:.6f}")
print(f"Mean Difference (Present - Absent): {mean_diff:.3f}")

print(f"95% Confidence Interval: [{ci_low:.3f}, {ci_high:.3f}]")

# Interpretation
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


