# Adds a season label and drops month =6
import pandas as pd
from pathlib import Path


INPUT_PATH  = "merged_clean.csv"        
OUTPUT_PATH = "merged_with_season.csv"  


if not Path(INPUT_PATH).exists():
    raise FileNotFoundError(f"Could not find {INPUT_PATH}")

df = pd.read_csv(INPUT_PATH)
df = df[df["month_x"] != 6].copy()

# Assign seasons
def assign_season(m):
    if m in [0, 1, 2]:   # Dec, Jan, Feb
        return 0  # Winter
    elif m in [3, 4, 5]: # Mar, Apr, May
        return 1  # Spring
    else:
        return None

df["season"] = df["month_x"].apply(assign_season)
df["season_name"] = df["season"].map({0: "Winter", 1: "Spring"})


df.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved cleaned dataset with seasons → {OUTPUT_PATH}")


