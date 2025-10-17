#Merges the air quality data to our dataset
import pandas as pd

moonlight_df = pd.read_csv("merged_with_moonlight.csv")
air_quality_df = pd.read_csv("tel-aviv-air-quality.csv")

moonlight_df['time'] = pd.to_datetime(moonlight_df['time'], errors='coerce')
air_quality_df['date'] = pd.to_datetime(air_quality_df['date'], errors='coerce')
moonlight_df['date'] = moonlight_df['time'].dt.date
air_quality_df['date'] = air_quality_df['date'].dt.date

merged_df = pd.merge(moonlight_df, air_quality_df, on='date', how='left')


merged_df.to_csv("merged_with_air_quality.csv", index=False)
print("File saved as 'merged_with_air_quality.csv'")




