

import math
import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib.pyplot as plt


FILE = "merged_grouped.csv"
COL_HESIT = "bat_landing_to_food"   
COL_GROUP = "rat_present"           
         
df = pd.read_csv(FILE)


hes = df.loc[(df[COL_GROUP] == 1), COL_HESIT].dropna().astype(float)

n = hes.size
if n == 0:
    raise ValueError(
        "No hesitation data found where rat_present == 1. "
        "Check your file or column names."
    )


mean = hes.mean()
std = hes.std(ddof=1)               
median = np.median(hes)
q25, q75 = np.percentile(hes, [25, 75])
iqr = q75 - q25
vmin, vmax = hes.min(), hes.max()


tcrit = t.ppf(0.975, df=n-1)        
se = std / math.sqrt(n)
ci_lo = mean - tcrit * se
ci_hi = mean + tcrit * se


print("=== Bat Hesitation (Rats Present Only) ===")
print(f"Sample size (n):         {n}")
print(f"Mean (sec):              {mean:.2f}")
print(f"Standard deviation:      {std:.2f}")
print(f"Median (sec):            {median:.2f}")
print(f"25th–75th pct (IQR):     {q25:.2f} – {q75:.2f}  (IQR = {iqr:.2f})")
print(f"Min / Max (sec):         {vmin:.2f} / {vmax:.2f}")
print(f"95% CI for mean (sec):   [{ci_lo:.2f}, {ci_hi:.2f}]")



plt.figure(figsize=(10, 6))


plt.hist(hes, bins=30, edgecolor="black", alpha=0.7)


max_value = int(hes.max())
plt.xticks(np.arange(0, max_value + 10, 10))
plt.xticks(rotation=90)
plt.title("Bat Hesitation Time (Rats Present)")
plt.xlabel("Hesitation time (sec)")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


report_line = (
    f"\nReport-ready: Bats hesitated {mean:.2f} s on average (95% CI {ci_lo:.2f}–{ci_hi:.2f}, "
    f"n={n}; median {median:.2f} s, IQR {q25:.2f}–{q75:.2f})."
)
print(report_line)


