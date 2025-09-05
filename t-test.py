import pandas as pd

df = pd.read_csv("merged_grouped.csv")
print(df.info())
print(df["rat_present"].value_counts())
print("======new_Stuff=====")
print(df.describe())
print(df['rat_present'].value_counts(normalize=True))

