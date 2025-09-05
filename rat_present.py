# make_rat_groups_single.py
# Input : merged_clean.csv
# Output: merged_grouped.csv
#
# Rule (strict):
#   rat_present = 0  iff (rat_minutes == 0) AND (rat_arrival_number == 0)
#   rat_present = 1  otherwise
#
# Notes:
# - Drops rows with NaNs in rat_minutes or rat_arrival_number (keeps data strict).
# - Does not add any other columns.

import pandas as pd

IN_PATH = "merged_clean.csv"
OUT_PATH = "merged_grouped.csv"

def main():
    df = pd.read_csv(IN_PATH)

    # Ensure required columns exist
    required = ["rat_minutes", "rat_arrival_number"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required column(s): {missing}. They must be present in {IN_PATH}.")

    # Coerce to numeric and drop rows with NaNs in required fields
    for c in required:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    before = len(df)
    df = df.dropna(subset=required)
    print(f"Dropped {before - len(df)} rows with NaNs in {required}.")

    # Strict rat-present flag
    rat_absent = (df["rat_minutes"] == 0) & (df["rat_arrival_number"] == 0)
    df["rat_present"] = (~rat_absent).astype(int)

    # Save single grouped file
    df.to_csv(OUT_PATH, index=False)

    # Console summary
    print("=== Rat Present Summary ===")
    print(df["rat_present"].value_counts(dropna=False).to_string())
    print(f"Saved -> {OUT_PATH}")

if __name__ == "__main__":
    main()
