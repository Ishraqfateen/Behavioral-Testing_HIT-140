# merge_minimal.py
# Goal: Merge dataset2 (30-min bins) with dataset1 (bat events) correctly,
#       keeping *all* bins from dataset2 and attaching dataset1 rows that fall inside each bin.
#
# Output: merged.csv
# - One row per dataset1 event matched to its bin
# - Bins with no dataset1 events are still present (dataset1 columns = NaN)
# - No extra helper/aggregate columns are added

import pandas as pd

# ------------- CONFIG (edit if needed) -------------
IN1 = "dataset1.csv"   # bats/events
IN2 = "dataset2.csv"   # bins/rats
OUT = "merged.csv"
DAYFIRST = True        # True if your dates are DD/MM/YYYY; False for MM/DD/YYYY
BIN_MIN = 30           # bin length if dataset2 has no explicit bin_end
# ---------------------------------------------------

def pick_datetime(df, preferred):
    """Return a parsed datetime Series from the first matching column name."""
    for col in preferred:
        if col in df.columns:
            s = pd.to_datetime(df[col], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
            if s.notna().any():
                return s, col
    # try (date + time) combo
    date_cands = [c for c in ["date","Date","day","Day"] if c in df.columns]
    time_cands = [c for c in ["time","Time","timestamp","Timestamp","start_time","Start Time","datetime","DateTime"] if c in df.columns]
    if date_cands and time_cands:
        col_d, col_t = date_cands[0], time_cands[0]
        s = pd.to_datetime(df[col_d].astype(str) + " " + df[col_t].astype(str),
                           errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
        if s.notna().any():
            return s, f"{col_d}+{col_t}"
    # fallback: scan object columns
    for col in df.columns:
        if df[col].dtype == "object":
            s = pd.to_datetime(df[col], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
            if s.notna().any():
                return s, col
    raise ValueError("Could not find a datetime column.")

def main():
    # --------- Load ---------
    df1 = pd.read_csv(IN1)  # events
    df2 = pd.read_csv(IN2)  # bins

    # --------- Parse times ---------
    # dataset1: event time
    ev_time, ev_col = pick_datetime(df1, preferred=["start_time","Start Time","datetime","DateTime","timestamp","Timestamp"])
    df1 = df1.copy()
    df1["_event_dt"] = pd.to_datetime(ev_time, errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    df1 = df1[df1["_event_dt"].notna()].copy()

    # dataset2: bin start (and end if present or infer)
    bin_start, bin_col = pick_datetime(df2, preferred=["bin_start","Bin Start","timestamp","Timestamp","datetime","DateTime"])
    df2 = df2.copy()
    df2["_bin_start"] = pd.to_datetime(bin_start, errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    df2 = df2[df2["_bin_start"].notna()].copy()

    if "bin_end" in df2.columns:
        df2["_bin_end"] = pd.to_datetime(df2["bin_end"], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    else:
        df2["_bin_end"] = df2["_bin_start"] + pd.Timedelta(minutes=BIN_MIN)

    # --------- Match each event to its bin (asof + in-range check) ---------
    # 1) asof to get the most recent bin_start within BIN_MIN
    df2_for_match = df2[["_bin_start","_bin_end"]].sort_values("_bin_start")
    matched = pd.merge_asof(
        df1.sort_values("_event_dt"),
        df2_for_match,
        left_on="_event_dt",
        right_on="_bin_start",
        direction="backward",
        tolerance=pd.Timedelta(minutes=BIN_MIN),
    )

    # 2) keep only events that truly fall inside [bin_start, bin_end)
    inside = matched["_bin_start"].notna() & (matched["_event_dt"] < matched["_bin_end"])
    matched = matched[inside].copy()

    # Keep original df1 columns + the matched bin_start to merge on
    df1_for_join = matched[df1.columns.tolist() + ["_event_dt","_bin_start"]].copy()

    # --------- Final merge: KEEP ALL BINS ---------
    # Left-join dataset2 bins (all rows) with event rows that matched that bin
    out = df2.merge(df1_for_join, left_on="_bin_start", right_on="_bin_start", how="left")

    # --------- Tidy: drop helper columns, keep originals ---------
    drop_cols = ["_bin_start","_bin_end","_event_dt"]  # internal helpers
    out = out.drop(columns=[c for c in drop_cols if c in out.columns])

    # Optionally sort by time (bin then event within bin if you keep event datetime col)
    if "bin_start" in out.columns:
        out = out.sort_values("bin_start")
    elif "timestamp" in out.columns:
        out = out.sort_values("timestamp")

    out.to_csv(OUT, index=False)
    print(f"Done. Wrote {OUT} with {len(out)} rows.")
    # Small sanity prints
    zero_rat = out["rat_minutes"].eq(0).sum() if "rat_minutes" in out.columns else "n/a"
    print(f"Zero-rat bins preserved: {zero_rat}")

if __name__ == "__main__":
    main()


