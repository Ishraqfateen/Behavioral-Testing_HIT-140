# rat_vs_bat_analysis.py
# Streamlined analysis focusing only on relevant graphs and statistics

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, pearsonr

# ===========================
# 1. LOAD THE DATA
# ===========================
FILE_PATH = "merged_grouped.csv"

print("Loading dataset...")
df = pd.read_csv(FILE_PATH)

print("\n=== Dataset Info ===")
print(df.info())

print("\n=== First 5 Rows ===")
print(df.head())

# Ensure required columns exist
required_columns = ["rat_present", "rat_minutes", "bat_landing_number"]
missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise KeyError(f"Missing required columns: {missing}")

# ===========================
# 2. SUMMARY STATS
# ===========================
print("\n=== Summary Statistics ===")
print(df.describe())

# Check proportion of bins with and without rats
rat_counts = df["rat_present"].value_counts(normalize=True)
print("\n=== Rat Presence Proportion ===")
print(rat_counts)

# ===========================
# 3. T-TEST: Bat Activity by Rat Presence
# ===========================
print("\n=== T-Test: Bat Activity by Rat Presence ===")
rat_present_group = df[df['rat_present'] == 1]['bat_landing_number']
rat_absent_group = df[df['rat_present'] == 0]['bat_landing_number']

# Welch's t-test (handles unequal variance)
t_stat, p_val = ttest_ind(rat_present_group, rat_absent_group, equal_var=False)

print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4f}")

# Group means
mean_present = rat_present_group.mean()
mean_absent = rat_absent_group.mean()
print(f"\nMean Bat Landings (Rats Present): {mean_present:.2f}")
print(f"Mean Bat Landings (Rats Absent): {mean_absent:.2f}")

if p_val < 0.05:
    if mean_present < mean_absent:
        print("Result: Significant decrease in bat activity when rats are present → Possible avoidance behavior (predator perception).")
    else:
        print("Result: Significant increase in bat activity when rats are present → Possible competition or aggressive foraging.")
else:
    print("Result: No significant difference → Rats may not strongly affect bat activity.")

# ===========================
# 4. CORRELATION: Rat Minutes vs Bat Landings
# ===========================
print("\n=== Correlation: Rat Minutes vs Bat Landings ===")
corr, p_corr = pearsonr(df['rat_minutes'], df['bat_landing_number'])
print(f"Correlation coefficient: {corr:.4f}")
print(f"P-value: {p_corr:.4f}")

if p_corr < 0.05:
    if corr < 0:
        print("Interpretation: Negative correlation → More rats are associated with fewer bats (avoidance behavior).")
    elif corr > 0:
        print("Interpretation: Positive correlation → More rats are associated with more bats (competition).")
else:
    print("Interpretation: No strong relationship between rat and bat activity.")

# ===========================
# 5. VISUALIZATIONS (Only Relevant Graphs)
# ===========================

# --- Boxplot: Bat Activity by Rat Presence ---
plt.figure(figsize=(8,6))
data = [rat_absent_group, rat_present_group]
plt.boxplot(
    data,
    tick_labels=['Rats Absent', 'Rats Present'],
    patch_artist=True,
    boxprops=dict(facecolor='lightblue', color='blue'),
    medianprops=dict(color='red'),
    whiskerprops=dict(color='blue'),
    capprops=dict(color='blue')
)
plt.title('Bat Activity by Rat Presence')
plt.xlabel('Rat Presence')
plt.ylabel('Bat Landing Number')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- Scatter Plot: Rat Minutes vs Bat Landings ---
plt.figure(figsize=(8,6))
plt.scatter(df['rat_minutes'], df['bat_landing_number'],
            alpha=0.6, color='purple', edgecolors='black')
plt.title('Rat Minutes vs Bat Landings')
plt.xlabel('Rat Minutes (per bin)')
plt.ylabel('Bat Landings (per bin)')
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# ===========================
# 6. FINAL SUMMARY
# ===========================
print("\n=== Final Summary ===")
print(f"Total Bins: {len(df)}")
print(f"Rat Absent Bins: {len(rat_absent_group)} ({rat_counts[0]*100:.2f}%)")
print(f"Rat Present Bins: {len(rat_present_group)} ({rat_counts[1]*100:.2f}%)")

print("\nAnalysis complete! Only relevant graphs and stats were generated.")


