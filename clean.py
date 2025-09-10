import pandas as pd

IN_PATH = "merged.csv"
OUT_PATH = "merged_clean.csv"
BIN_MIN = 30 

def coerce_numeric(df, cols):
    """Convert to numeric, keep NaN if conversion fails."""
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

def main():
    print("Loading merged dataset...")
    df = pd.read_csv(IN_PATH)

    for col in ["bin_start", "bin_end", "start_time_parsed"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "bin_start" in df.columns:
        if "bin_end" not in df.columns:
            df["bin_end"] = pd.NaT
        need_end = df["bin_end"].isna()
        df.loc[need_end, "bin_end"] = df.loc[need_end, "bin_start"] + pd.Timedelta(minutes=BIN_MIN)

    before = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {before - len(df)} duplicate rows.")

    required_cols = ["bin_start", "rat_minutes", "rat_arrival_number"]
    existing_cols = [c for c in required_cols if c in df.columns]

    before_drop = len(df)
    df = df.dropna(subset=existing_cols)
    print(f"Dropped {before_drop - len(df)} rows with NaNs in {existing_cols}.")

    numeric_candidates = [
        "rat_minutes", "rat_arrival_number", "rat_landing_number", 
        "rat_number", "rat_count", "bat_landing_to_food",
        "bat_landing_number", "seconds_after_rat_arrival",
        "risk", "reward"
    ]
    coerce_numeric(df, numeric_candidates)

    before_drop_numeric = len(df)
    df = df.dropna(subset=["rat_minutes", "rat_arrival_number"])
    print(f"Dropped {before_drop_numeric - len(df)} rows due to invalid numeric values.")

    sort_cols = [c for c in ["bin_start", "start_time_parsed"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    df.to_csv(OUT_PATH, index=False)
    print(f"Clean dataset saved as {OUT_PATH}")
    print(f"Final number of rows: {len(df)}")

if __name__ == "__main__":
    main()
