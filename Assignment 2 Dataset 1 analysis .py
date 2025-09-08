## Dataset 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("dataset1.csv")

# Part of differential analysis
print(df.head())
print(df.info())
print(df.shape) # number of rows and columns
print(df.columns) # column names

numbers = df.describe()
print(numbers)

mode1 = df.mode()
print("Mode of dataset 1: \n", mode1)

median1 = df.median(numeric_only = True)
print("Median of dataset 1: \n", median1)

variance = df.var(numeric_only = True)
print(variance)

std_deviation = df.std(numeric_only = True)
print(std_deviation)

# Mean, median and mode of the column bat_landing_to_food
bat_landing = df["bat_landing_to_food"]
bat_landing_mean = bat_landing.mean()
bat_landing_median = bat_landing.median()
bat_landing_mode = bat_landing.mode()
print("Mean of the column bat_landing_to_food:", bat_landing_mean)
print("Median of the column bat_landing_to_food:", bat_landing_median)
print("Mode of the column bat_landing_to_food:", bat_landing_mode)

# Mean, median and mode of the column seconds_after_rat_arrival
rat_arr = df["seconds_after_rat_arrival"]
rat_arr_mean = rat_arr.mean()
rat_arr_median = rat_arr.median()
rat_arr_mode = rat_arr.mode()
print("Mean of the column seconds_after_rat_arrival is: ", rat_arr_mean)
print("Median of the column seconds_after_rat_arrival is: ", rat_arr_median)
print("Mode of the column seconds_after_rat_arrival is: ", rat_arr_mode)

### Idea behind Inferential Analysis: If the bats perceive risk in the presence of rats, there would be an increase in vigilance, otherwise there won't be any change.
### We can use T-test to compare the results as for when rats are present ("risk perceived") and when they are absent ("No risk perceived")

# Spliting the  data into two groups: risk = 0 vs risk = 1
no_risk_perceived = df.loc[df['risk'] == 0, 'bat_landing_to_food'].dropna()
risk_perceived = df.loc[df['risk'] == 1, 'bat_landing_to_food'].dropna()

# Descriptive statistics
print("The Descriptive Statistics for bat_landing_to_food column are:")
print(f"Sample size (no risk perceived): {len(no_risk_perceived)}")
print(f"Mean (no risk perceived): {no_risk_perceived.mean():.2f}")
print(f"Median (no risk perceived): {no_risk_perceived.median():.2f}")
print(f"Standard Deviation (no risk perceived): {no_risk_perceived.std():.2f}\n")

print(f"Sample size (risk perceived): {len(risk_perceived)}")
print(f"Mean (risk perceived): {risk_perceived.mean():.2f}")
print(f"Median (risk perceived): {risk_perceived.median():.2f}")
print(f"Standard Deviation (risk perceived): {risk_perceived.std():.2f}\n")

# 4. Visualisation using box plot
plt.figure(figsize=(10,5))
plt.boxplot([no_risk_perceived, risk_perceived],
            labels=["No Risk Perceived", "Risk Perceived"])
plt.title("Bat landing to food time\n(0 = No Risk Perceived, 1 = Risk Perceived)")
#plt.suptitle("")
plt.ylabel("Seconds")
# plt.show()

# Drawing a Histogram
plt.figure(figsize=(10,5))
plt.hist(no_risk_perceived, bins=30, alpha=0.5, label="No Risk Perceived")
plt.hist(risk_perceived, bins=30, alpha=0.5, label="Risk Perceived")
plt.legend()
plt.xlabel("Bat landing to food (seconds)")
plt.ylabel("The Frequency of bat landing")
plt.title("Histogram of bat landing onto food times")
plt.show()

# 5. Inferential analysis by doing a t-test to compare the statistics
t_stat, p_val = stats.ttest_ind(no_risk_perceived, risk_perceived, equal_var=False)

print("t-test results are:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4f}")

# Interpretation of the end results found from Dataset 1
if p_val < 0.05:
    print("There is a significant difference in the values. So, when bats show increased vigilance when they perceive risk from rats.")
else:
    print("There is no significant difference in the values. Hence, risk perception does not clearly alter vigilance times for the bats.")
