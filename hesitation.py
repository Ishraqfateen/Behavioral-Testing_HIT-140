# hesitation_descriptives_ci.py
# Describe bat hesitation time (seconds) when rats are present
# Outputs: n, mean, SD, median, IQR, min/max, and 95% CI for the mean
# (No seaborn; matplotlib optional and disabled by default)

import math
import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib.pyplot as plt

# ------------- Config -------------
FILE = "merged_grouped.csv"
COL_HESIT = "bat_landing_to_food"   # seconds
COL_GROUP = "rat_present"           # 0/1
         # set True to see a quick histogram (matplotlib required)

# ------------- Load & filter -------------
df = pd.read_csv(FILE)

# Keep ONLY rows with rats present (1) and non-null hesitation
hes = df.loc[(df[COL_GROUP] == 1), COL_HESIT].dropna().astype(float)

n = hes.size
if n == 0:
    raise ValueError(
        "No hesitation data found where rat_present == 1. "
        "Check your file or column names."
    )

# ------------- Descriptive statistics -------------
mean = hes.mean()
std = hes.std(ddof=1)               # sample SD
median = np.median(hes)
q25, q75 = np.percentile(hes, [25, 75])
iqr = q75 - q25
vmin, vmax = hes.min(), hes.max()

# ------------- 95% Confidence Interval for the mean -------------
# CI = mean ± t*(SD/sqrt(n)), using t critical with df = n-1
tcrit = t.ppf(0.975, df=n-1)        # two-sided 95%
se = std / math.sqrt(n)
ci_lo = mean - tcrit * se
ci_hi = mean + tcrit * se

# ------------- Print results -------------
print("=== Bat Hesitation (Rats Present Only) ===")
print(f"Sample size (n):         {n}")
print(f"Mean (sec):              {mean:.2f}")
print(f"Standard deviation:      {std:.2f}")
print(f"Median (sec):            {median:.2f}")
print(f"25th–75th pct (IQR):     {q25:.2f} – {q75:.2f}  (IQR = {iqr:.2f})")
print(f"Min / Max (sec):         {vmin:.2f} / {vmax:.2f}")
print(f"95% CI for mean (sec):   [{ci_lo:.2f}, {ci_hi:.2f}]")

# ------------- Optional: quick histogram -------------
# Assuming hesitation data is already filtered as `hes`

plt.figure(figsize=(10, 6))

# Histogram with a reasonable number of bins
plt.hist(hes, bins=30, edgecolor="black", alpha=0.7)

# Set custom ticks at intervals of 10
max_value = int(hes.max())
plt.xticks(np.arange(0, max_value + 10, 10))

# Rotate labels to prevent overlapping
plt.xticks(rotation=90)

# Titles and labels
plt.title("Bat Hesitation Time (Rats Present)")
plt.xlabel("Hesitation time (sec)")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()



# ------------- Helpful reporting snippet -------------
# Example sentence you can paste into your report (prints to console):
report_line = (
    f"\nReport-ready: Bats hesitated {mean:.2f} s on average (95% CI {ci_lo:.2f}–{ci_hi:.2f}, "
    f"n={n}; median {median:.2f} s, IQR {q25:.2f}–{q75:.2f})."
)
print(report_line)


