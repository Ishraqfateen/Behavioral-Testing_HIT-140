# merge_bins_keep_dataset1_rows.py
import pandas as pd
from pathlib import Path
from typing import Optional

# ================== CONFIG ==================
DAYFIRST = True      # True if your dates are DD/MM/YYYY; False if MM/DD/YYYY
IN1 = "dataset1.csv"
IN2 = "dataset2.csv"
OUT = "merged_long.csv"    # one row per dataset1 record with its matched dataset2 bin
# ============================================

def smart_parse_datetime(
    df: pd.DataFrame,
    preferred_cols=(),
    date_col_candidates=("date","Date","day","Day"),
    time_col_candidates=("time","Time","start_time","Start Time","timestamp","Timestamp","datetime","DateTime"),
    dayfirst=True
) -> Optional[pd.Series]:
    """Return a parsed datetime Series from df using common patterns."""
    # 1) Try explicit datetime-like columns
    try_cols = list(preferred_cols) + [
        "start_time","Start Time","timestamp","Timestamp","datetime","DateTime","time","Time"
    ]
    for c in try_cols:
        if c in df.columns:
            s = pd.to_datetime(df[c], errors="coerce", dayfirst=dayfirst, infer_datetime_format=True)
            if s.notna().any():
                return s

    # 2) Try combining a date col + a time col
    date_col = next((c for c in date_col_candidates if c in df.columns), None)
    time_col = next((c for c in time_col_candidates if c in df.columns), None)
    if date_col and time_col:
        combo = df[date_col].astype(str).str.strip() + " " + df[time_col].astype(str).str.strip()
        s = pd.to_datetime(combo, errors="coerce", dayfirst=dayfirst, infer_datetime_format=True)
        if s.notna().any():
            return s

    # 3) Fallback: scan any object-like col
    for c in df.columns:
        if pd.api.types.is_object_dtype(df[c]):
            s = pd.to_datetime(df[c], errors="coerce", dayfirst=dayfirst, infer_datetime_format=True)
            if s.notna().any():
                return s
    return None

def main():
    p1, p2 = Path(IN1), Path(IN2)
    if not p1.exists():
        raise FileNotFoundError(f"{IN1} not found in {Path.cwd()}")
    if not p2.exists():
        raise FileNotFoundError(f"{IN2} not found in {Path.cwd()}")

    # --- Load
    df1 = pd.read_csv(p1)
    df2 = pd.read_csv(p2)

    # --- Parse dataset1 start_time
    dt1 = smart_parse_datetime(df1, preferred_cols=("start_time","Start Time","datetime","DateTime"), dayfirst=DAYFIRST)
    if dt1 is None:
        raise ValueError("Could not detect/parse a datetime column in dataset1. "
                         "Add/rename a column to 'start_time' or 'datetime'.")
    df1 = df1.copy()
    df1["start_time_parsed"] = pd.to_datetime(dt1, errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    df1 = df1[df1["start_time_parsed"].notna()].copy()

    # --- Parse dataset2 bin start
    dt2_start = smart_parse_datetime(
        df2,
        preferred_cols=("timestamp","Timestamp","bin_start","Bin Start","datetime","DateTime","start_time","Start Time"),
        dayfirst=DAYFIRST
    )
    if dt2_start is None:
        raise ValueError("Could not detect/parse a bin-start datetime column in dataset2. "
                         "Add/rename a column to 'timestamp' or 'datetime' for bin starts.")
    df2 = df2.copy()
    df2["bin_start"] = pd.to_datetime(dt2_start, errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    df2 = df2[df2["bin_start"].notna()].copy()

    # --- Bin end: use explicit end column if present, else assume 30 minutes
    dt2_end = None
    for cand in ("bin_end","Bin End","end_time","End Time","end","End","stop","Stop","finish","Finish"):
        if cand in df2.columns:
            dt2_end = pd.to_datetime(df2[cand], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
            break
    if dt2_end is not None and dt2_end.notna().any():
        df2["bin_end"] = dt2_end
    else:
        df2["bin_end"] = df2["bin_start"] + pd.Timedelta(minutes=30)

    # --- Clean + sort (fixes “disarranged” dates)
    df1.sort_values("start_time_parsed", inplace=True)
    df2.sort_values("bin_start", inplace=True)

    # ================== MATCHING LOGIC ==================
    # Treat dataset2 timestamps as the START of the 30-min bin:
    #   bin = [bin_start, bin_end)
    # For each dataset1 start time, pick the most recent bin_start within 30 minutes,
    # then keep only if start_time < bin_end (i.e., truly inside the bin).
    merged = pd.merge_asof(
        df1,
        df2.sort_values("bin_start"),
        left_on="start_time_parsed",
        right_on="bin_start",
        direction="backward",
        tolerance=pd.Timedelta(minutes=30)
    )
    inside = merged["bin_start"].notna() & (merged["start_time_parsed"] < merged["bin_end"])
    merged = merged[inside].copy()
    # ====================================================

    # Optional: If your dataset2 timestamps are actually the **END** of each bin (e.g., 19:30 means (19:00,19:30]),
    # replace the block above with this alternative:
    #
    # df2_alt = df2.copy()
    # df2_alt["bin_end"] = df2_alt["bin_start"]       # treat given times as bin_end
    # df2_alt["bin_start"] = df2_alt["bin_end"] - pd.Timedelta(minutes=30)
    # merged = pd.merge_asof(
    #     df1.sort_values("start_time_parsed"),
    #     df2_alt.sort_values("bin_end"),
    #     left_on="start_time_parsed",
    #     right_on="bin_end",
    #     direction="forward",
    #     tolerance=pd.Timedelta(minutes=30)
    # )
    # inside = merged["bin_start"].notna() & (merged["start_time_parsed"] >= merged["bin_start"])
    # merged = merged[inside].copy()

    # Final tidy: order by bin then by event
    order_cols = ["bin_start","start_time_parsed"]
    merged.sort_values([c for c in order_cols if c in merged.columns], inplace=True)

    # Put key time columns first for readability
    front = [c for c in ["bin_start","bin_end","start_time_parsed"] if c in merged.columns]
    rest = [c for c in merged.columns if c not in front]
    merged = merged[front + rest]

    merged.to_csv(OUT, index=False)
    print(f"Done. Wrote {OUT} with {len(merged)} rows.")
    matched = len(merged)
    total1 = len(df1)
    print(f"Matched dataset1 rows into bins: {matched} / {total1}")
    if matched < total1:
        print("Note: Some dataset1 rows were outside the available dataset2 time range or >30min from any bin.")

if __name__ == "__main__":
    main()


