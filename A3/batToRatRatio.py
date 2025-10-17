#adds bat_to_rats_ratio
import pandas as pd
import numpy as np

df = pd.read_csv("merged_with_air_quality_features.csv")

if "bat_to_rat_ratio" not in df.columns:
    if "bat_landing_number" in df.columns and "rat_arrival_number" in df.columns:
        df["bat_to_rat_ratio"] = (
            pd.to_numeric(df["bat_landing_number"], errors="coerce").fillna(0) /
            (pd.to_numeric(df["rat_arrival_number"], errors="coerce").fillna(0) + 1)
        )
        print("Added new variable: bat_to_rat_ratio")
    else:
        print(" Missing columns for bat_to_rat_ratio")

df.to_csv("merged_with_bat_to_rat.csv", index=False)
