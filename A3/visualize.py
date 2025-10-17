import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("merged_with_bat_to_rat.csv")
df["season_label"] = df["season"].map({0: "Winter", 1: "Spring"})
df["rat_present_label"] = df["rat_present"].map({0: "Absent (0)", 1: "Present (1)"})
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







