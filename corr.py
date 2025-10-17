import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("merged_with_bat_to_rat.csv")
df.columns = [c.strip().lower() for c in df.columns]

# Focus only on continuous variables you used in the regression
cols = [
    "total_hesitation_delay",
    "rat_arrival_number",
    "food_risk_ratio",
    "bat_landing_number",
    "hours_after_sunset_x",
    "moon_illumination",
    "visibility",
    "bat_to_rat_ratio",
    "food_change_rate"
]

# Separate winter & spring data
winter = df[df["season"] == 0][cols]
spring = df[df["season"] == 1][cols]

# Compute correlation with response variable only
corr_winter = winter.corr()["total_hesitation_delay"].drop("total_hesitation_delay")
corr_spring = spring.corr()["total_hesitation_delay"].drop("total_hesitation_delay")

# Combine into one DataFrame for easy plotting
corr_df = pd.DataFrame({"Winter": corr_winter, "Spring": corr_spring})

# Plot
plt.figure(figsize=(8,5))
corr_df.plot(kind="bar", figsize=(10,6))
plt.title("Correlation with Total Hesitation Delay (Winter vs Spring)")
plt.ylabel("Pearson r")
plt.xlabel("Explanatory Variable")
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='black', lw=1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
