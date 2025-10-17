import pandas as pd
IN1 = "dataset1.csv"   
IN2 = "dataset2.csv"   
OUT = "merged.csv"
DAYFIRST = True        
BIN_MIN = 30           


def pick_datetime(df, preferred):
    """Return a parsed datetime Series from the first matching column name."""
    for col in preferred:
        if col in df.columns:
            s = pd.to_datetime(df[col], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
            if s.notna().any():
                return s, col
    
    date_cands = [c for c in ["date","Date","day","Day"] if c in df.columns]
    time_cands = [c for c in ["time","Time","timestamp","Timestamp","start_time","Start Time","datetime","DateTime"] if c in df.columns]
    if date_cands and time_cands:
        col_d, col_t = date_cands[0], time_cands[0]
        s = pd.to_datetime(df[col_d].astype(str) + " " + df[col_t].astype(str),
                           errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
        if s.notna().any():
            return s, f"{col_d}+{col_t}"
    
    for col in df.columns:
        if df[col].dtype == "object":
            s = pd.to_datetime(df[col], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
            if s.notna().any():
                return s, col
    raise ValueError("Could not find a datetime column.")

def main():
    df1 = pd.read_csv(IN1)  
    df2 = pd.read_csv(IN2)  

    
    
    ev_time, ev_col = pick_datetime(df1, preferred=["start_time","Start Time","datetime","DateTime","timestamp","Timestamp"])
    df1 = df1.copy()
    df1["_event_dt"] = pd.to_datetime(ev_time, errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    df1 = df1[df1["_event_dt"].notna()].copy()

    
    bin_start, bin_col = pick_datetime(df2, preferred=["bin_start","Bin Start","timestamp","Timestamp","datetime","DateTime"])
    df2 = df2.copy()
    df2["_bin_start"] = pd.to_datetime(bin_start, errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    df2 = df2[df2["_bin_start"].notna()].copy()

    if "bin_end" in df2.columns:
        df2["_bin_end"] = pd.to_datetime(df2["bin_end"], errors="coerce", dayfirst=DAYFIRST, infer_datetime_format=True)
    else:
        df2["_bin_end"] = df2["_bin_start"] + pd.Timedelta(minutes=BIN_MIN)

    
    
    df2_for_match = df2[["_bin_start","_bin_end"]].sort_values("_bin_start")
    matched = pd.merge_asof(
        df1.sort_values("_event_dt"),
        df2_for_match,
        left_on="_event_dt",
        right_on="_bin_start",
        direction="backward",
        tolerance=pd.Timedelta(minutes=BIN_MIN),
    )

    
    inside = matched["_bin_start"].notna() & (matched["_event_dt"] < matched["_bin_end"])
    matched = matched[inside].copy()

    
    df1_for_join = matched[df1.columns.tolist() + ["_event_dt","_bin_start"]].copy()

    
    out = df2.merge(df1_for_join, left_on="_bin_start", right_on="_bin_start", how="left")

    
    drop_cols = ["_bin_start","_bin_end","_event_dt"]  # internal helpers
    out = out.drop(columns=[c for c in drop_cols if c in out.columns])

    
    if "bin_start" in out.columns:
        out = out.sort_values("bin_start")
    elif "timestamp" in out.columns:
        out = out.sort_values("timestamp")

    out.to_csv(OUT, index=False)
    print(f"Done. Wrote {OUT} with {len(out)} rows.")
    
    zero_rat = out["rat_minutes"].eq(0).sum() if "rat_minutes" in out.columns else "n/a"
    print(f"Zero-rat bins preserved: {zero_rat}")

if __name__ == "__main__":
    main()


