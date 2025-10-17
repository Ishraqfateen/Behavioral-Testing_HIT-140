#Dropped any rows missing pm25,pm10
#Featured new variables
import pandas as pd


df = pd.read_csv("merged_with_air_quality.csv")
df.columns = df.columns.str.strip().str.lower()

pm25_col = [c for c in df.columns if 'pm25' in c or 'pm2.5' in c]
pm10_col = [c for c in df.columns if 'pm10' in c]

print(pm25_col, pm10_col)

if pm25_col and pm10_col:
    
    df[pm25_col[0]] = pd.to_numeric(df[pm25_col[0]], errors='coerce')
    df[pm10_col[0]] = pd.to_numeric(df[pm10_col[0]], errors='coerce')



    before_drop = len(df)
    df = df.dropna(subset=[pm25_col[0], pm10_col[0]]).copy()
    dropped_rows = before_drop - len(df)
    print(f"Dropped {dropped_rows} rows with missing pm25/pm10 values.")

    df['air_quality_index'] = (df[pm25_col[0]] + df[pm10_col[0]]) / 2
    df['visibility'] = 100 - df['air_quality_index']

    
    df.to_csv("merged_with_air_quality_features.csv", index=False)
    print("Saved as 'merged_with_air_quality_features.csv'.")

else:
    print("Could not find pm25, pm10 columns")



