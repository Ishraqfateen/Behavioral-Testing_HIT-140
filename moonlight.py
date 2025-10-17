# Moon Illumination added with astral library

import pandas as pd
from astral import moon
import math

df = pd.read_csv("merged_engineered_simple.csv")
df['time'] = pd.to_datetime(df['time'], errors='coerce', dayfirst=True)

def illumination_from_phase(date):
    if pd.isna(date):
        return None
    phase = moon.phase(date)  # 0–29.53 (days in lunar cycle)
    illumination = (1 - math.cos(2 * math.pi * phase / 29.53)) / 2 * 100
    return round(illumination, 2)

df['moon_illumination'] = df['time'].apply(illumination_from_phase)


df.to_csv("merged_with_moonlight.csv", index=False)
print("New file saved as 'merged_with_moonlight.csv'")

