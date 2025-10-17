import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("merged_with_bat_to_rat.csv")
df["season_label"] = df["season"].map({0: "Winter", 1: "Spring"})
df["rat_present_label"] = df["rat_present"].map({0: "Absent (0)", 1: "Present (1)"})

# Use consistent custom colors (e.g., blue for absent, orange for present)
palette = {"Absent (0)": "#66c2a5", "Present (1)": "#fc8d62"}

plt.figure(figsize=(8,6))
sns.boxplot(
    x="season_label", 
    y="total_hesitation_delay",
    hue="rat_present_label",
    data=df, 
    palette=palette,
    width=0.6
)
plt.title("Effect of Rat Presence on Bat Hesitation Delay (by Season)")
plt.xlabel("Season")
plt.ylabel("Total Hesitation Delay (seconds)")
plt.legend(title="Rat Present", loc="upper right")
plt.tight_layout()
plt.show()


plt.figure(figsize=(12,5))
sns.scatterplot(x="rat_minutes", y="total_hesitation_delay",
                hue="season_label", data=df, alpha=0.6)
plt.title("Relationship between Rat Activity and Hesitation Delay")
plt.xlabel("Rat Minutes (duration of rat presence)")
plt.ylabel("Total Hesitation Delay (seconds)")
plt.legend(title="Season")
plt.tight_layout()
plt.show()


plt.figure(figsize=(12,5))
sns.scatterplot(x="food_risk_ratio", y="total_hesitation_delay",
                hue="season_label", data=df, alpha=0.6)
plt.title("Reward–Risk Balance vs Hesitation Delay")
plt.xlabel("Food Risk Ratio (food_availability / (rat_minutes + 1))")
plt.ylabel("Total Hesitation Delay (seconds)")
plt.legend(title="Season")
plt.tight_layout()
plt.show()



