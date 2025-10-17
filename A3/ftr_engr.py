#Created new variables
import pandas as pd
import numpy as np

IN_FILE  = "merged_with_season.csv"          
OUT_FILE = "merged_engineered_simple.csv"    

df = pd.read_csv(IN_FILE)
df.columns = [c.strip().lower() for c in df.columns]

required = [
    "food_availability",
    "rat_minutes",
    "rat_arrival_number",
    "bat_landing_to_food",
    "seconds_after_rat_arrival",
]
missing = [c for c in required if c not in df.columns]
if missing:
    raise KeyError(f"Missing required column(s): {missing}")

for c in required:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["rat_minutes"] = df["rat_minutes"].fillna(0)
df["rat_arrival_number"] = df["rat_arrival_number"].fillna(0)
df["food_availability"] = df["food_availability"].fillna(df["food_availability"].mean())
df["bat_landing_to_food"] = df["bat_landing_to_food"].fillna(0)
df["seconds_after_rat_arrival"] = df["seconds_after_rat_arrival"].fillna(0)

df["total_hesitation_delay"] = df["bat_landing_to_food"] + df["seconds_after_rat_arrival"]

df["food_risk_ratio"] = df["food_availability"] / (df["rat_minutes"] + 1)


df["food_change_rate"] = df["food_availability"].diff().fillna(0)


rat_nan_mask = df["rat_minutes"].isna() & df["rat_arrival_number"].isna()
df["rat_present"] = np.where(
    (df["rat_minutes"] > 0) | (df["rat_arrival_number"] > 0),
    1,
    0
)

df.to_csv(OUT_FILE, index=False)
print(f"✅ Saved: {OUT_FILE}")







