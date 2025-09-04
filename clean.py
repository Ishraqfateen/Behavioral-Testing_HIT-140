# clean_merged_simple.py
# Cleans merged_long.csv and writes merged_clean.csv
# No pathlib, just plain strings for file paths.

import pandas as pd

# ===================== CONFIG =====================
IN_PATH  = "merged_long.csv"
OUT_PATH = "merged_clean.csv"
ASSUME_BIN_MINUTES = 30     # bin length in minutes if bin_end missing
FILL_HABIT_WITH = "Unknown" # placeholder for missing 'habit'
# ==================================================

def coerce_numeric_cols(df: pd.DataFrame) -> list:
    """Heuristically coerce likely numeric columns to numeric dtype."""
    likely = [c for c in df.columns if any(k in c.lower() for k in [
        "minute", "second", "count", "number", "risk", "reward",
        "hours_after", "landing", "arrival", "duration", "rate", "score",
        "sunset_time", "food_availability"
    ])]

    # ensure key columns are included
    for c in ["rat_minutes", "bat_landing_to_food", "seconds_after_rat_arrival",
              "bat_landing_number", "rat_arrival_number"]:
        if c in df.columns and c not in likely:
            likely.append(c)

    for c in likely:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return sorted(likely)

def main():
    # --- 1) Load data ---
    try:
        df = pd.read_csv(IN_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {IN_PATH}")

    # --- 2) Parse/standardize datetimes ---
    for col in ["start_time_parsed", "bin_start", "bin_end"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # If bin_end missing or NaT, assume fixed 30-min bins
    if "bin_end" not in df.columns:
        df["bin_end"] = pd.NaT
    missing_end = df["bin_end"].isna()
    if "bin_start" in df.columns:
        df.loc[missing_end, "bin_end"] = df.loc[missing_end, "bin_start"] + pd.Timedelta(minutes=ASSUME_BIN_MINUTES)

    # --- 3) Drop exact duplicate rows ---
    before = len(df)
    df = df.drop_duplicates()
    dropped_dupes = before - len(df)

    # --- 4) Keep only rows where start_time is inside its bin ---
    out_of_range = 0
    if {"start_time_parsed", "bin_start", "bin_end"}.issubset(df.columns):
        mask = (df["start_time_parsed"] >= df["bin_start"]) & (df["start_time_parsed"] < df["bin_end"])
        out_of_range = int((~mask).sum())
        df = df[mask].copy()

    # --- 5) Coerce numeric columns ---
    numeric_cols = coerce_numeric_cols(df)

    # Fill core NaNs for rat and bat data
    if "rat_minutes" in df.columns:
        df["rat_minutes"] = df["rat_minutes"].fillna(0)
    if "bat_landing_to_food" in df.columns:
        df["bat_landing_to_food"] = df["bat_landing_to_food"].fillna(0)

    # Clip negatives to 0
    for c in numeric_cols:
        df[c] = df[c].clip(lower=0)

    # --- 6) Fill categorical missing values ---
    if "habit" in df.columns:
        df["habit"] = df["habit"].fillna(FILL_HABIT_WITH)

    # --- 7) Add helper flags ---
    if "rat_minutes" in df.columns:
        df["rat_present"] = (df["rat_minutes"] > 0).astype(int)
    if "bat_landing_to_food" in df.columns:
        df["bat_present"] = (df["bat_landing_to_food"] > 0).astype(int)

    # --- 8) Sort chronologically ---
    sort_cols = [c for c in ["bin_start", "start_time_parsed"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    # --- 9) Save cleaned dataset ---
    df.to_csv(OUT_PATH, index=False)

    # --- 10) Console summary ---
    print("=== Cleaning Summary ===")
    print(f"Input rows: {before}")
    print(f"Dropped duplicates: {dropped_dupes}")
    print(f"Dropped out-of-range rows: {out_of_range}")
    print(f"Output rows: {len(df)}")
    print(f"Numeric columns coerced: {numeric_cols}")
    print(f"Flags added: rat_present={'rat_present' in df.columns}, bat_present={'bat_present' in df.columns}")
    print(f"Cleaned file saved as: {OUT_PATH}")

if __name__ == "__main__":
    main()