# Step 2: Descriptive Statistics
# Goal: Explore the data, summarize key measures, and visualize bat vs rat activity

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the cleaned dataset
df = pd.read_csv("merged_clean.csv")

# Ensure datetime format for bin_start
df['bin_start'] = pd.to_datetime(df['bin_start'], errors='coerce')

# =========================================
# A) Quick Summary of the Data
# =========================================
print("=== Basic Info ===")
print(df.info())

print("\n=== First 5 rows ===")
print(df.head())

print("\n=== Descriptive Statistics for Rat and Bat Activity ===")
print(df[['rat_minutes', 'bat_landing_to_food']].describe())

# Count bins where rats were present vs absent
rat_present_count = df['rat_present'].sum()
rat_absent_count = len(df) - rat_present_count

print("\nBins with Rat Activity:", rat_present_count)
print("Bins with No Rat Activity:", rat_absent_count)

# =========================================
# B) Group data by 30-minute bins
# =========================================
# We aggregate per bin so we can compare bat and rat totals for each window
grouped = df.groupby('bin_start').agg({
    'rat_minutes': 'sum',
    'bat_landing_to_food': 'sum'
}).reset_index()

print("\n=== Aggregated Data (first 5 bins) ===")
print(grouped.head())

# =========================================
# C) Visualization 1: Line Plot over Time
# =========================================
plt.figure(figsize=(12,6))
plt.plot(grouped['bin_start'], grouped['rat_minutes'], label='Rat Activity (minutes)', color='red')
plt.plot(grouped['bin_start'], grouped['bat_landing_to_food'], label='Bat Activity (minutes)', color='blue')
plt.xlabel('Time')
plt.ylabel('Minutes on Platform')
plt.title('Rat vs Bat Activity Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# =========================================
# D) Visualization 2: Scatter Plot (Relationship)
# =========================================
plt.figure(figsize=(7,6))
plt.scatter(grouped['rat_minutes'], grouped['bat_landing_to_food'], color='purple', alpha=0.7)
plt.xlabel('Rat Minutes (per 30-min bin)')
plt.ylabel('Bat Minutes (per 30-min bin)')
plt.title('Relationship Between Rat and Bat Activity')
plt.grid(True)
plt.tight_layout()
plt.show()

# =========================================
# E) Visualization 3: Histogram (Distribution)
# =========================================
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.hist(grouped['rat_minutes'], bins=20, color='red', alpha=0.7)
plt.xlabel('Rat Minutes')
plt.ylabel('Frequency')
plt.title('Distribution of Rat Activity')

plt.subplot(1,2,2)
plt.hist(grouped['bat_landing_to_food'], bins=20, color='blue', alpha=0.7)
plt.xlabel('Bat Minutes')
plt.ylabel('Frequency')
plt.title('Distribution of Bat Activity')

plt.tight_layout()
plt.show()
