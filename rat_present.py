import pandas as pd

IN_PATH = "merged_clean.csv"
OUT_PATH = "merged_grouped.csv"

def main():
    df = pd.read_csv(IN_PATH)

    
    required = ["rat_minutes", "rat_arrival_number"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required column(s): {missing}. They must be present in {IN_PATH}.")

    
    for c in required:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    before = len(df)
    df = df.dropna(subset=required)
    print(f"Dropped {before - len(df)} rows with NaNs in {required}.")

   
    rat_absent = (df["rat_minutes"] == 0) & (df["rat_arrival_number"] == 0)
    df["rat_present"] = (~rat_absent).astype(int)

    
    df.to_csv(OUT_PATH, index=False)

    
    print("=== Rat Present Summary ===")
    print(df["rat_present"].value_counts(dropna=False).to_string())
    print(f"Saved -> {OUT_PATH}")

if __name__ == "__main__":
    main()
