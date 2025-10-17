# =====================================================
# Investigation B – Final Linear Regression (Simple + Coefficient Comparison)
# =====================================================

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# ---------- Load ----------
df = pd.read_csv("merged_with_bat_to_rat.csv")
df.columns = [c.strip().lower() for c in df.columns]

# ---------- Define variables ----------
Y_COL = "total_hesitation_delay"
SEASON_COL = "season"

X_COLS = [
    "rat_arrival_number",
    "food_risk_ratio",
    "hours_after_sunset_x",  # adjust if needed
    "moon_illumination",
    "visibility",
    "bat_to_rat_ratio",
    "food_change_rate"
]

# Drop NaNs
df = df.dropna(subset=[Y_COL, SEASON_COL] + X_COLS)

# ---------- Helper function ----------
def run_lr(df_season, season_name):
    X = df_season[X_COLS].astype(float)
    y = df_season[Y_COL].astype(float)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metrics
    r2_train = model.score(X_train, y_train)
    r2_test = model.score(X_test, y_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    nrmse = rmse / (y_test.max() - y_test.min())

    # Output
    print(f"\n===== {season_name.upper()} MODEL RESULTS =====")
    print("Coefficients (seconds per +1 unit):")
    for name, coef in zip(X_COLS, model.coef_):
        print(f"{name:25s} {coef:8.3f}")
    print(f"Intercept:  {model.intercept_:8.3f}")
    print()
    print(f"R² (train) = {r2_train:.3f}")
    print(f"R² (test)  = {r2_test:.3f}")
    print(f"MAE (test) = {mae:.2f}")
    print(f"RMSE (test)= {rmse:.2f}")
    print(f"NRMSE (test)= {nrmse:.3f}")

    return model

# ---------- Run per season ----------
winter_df = df[df[SEASON_COL] == 0]
spring_df = df[df[SEASON_COL] == 1]

LR_winter = run_lr(winter_df, "Winter")
LR_spring = run_lr(spring_df, "Spring")

# ---------- Coefficient Comparison ----------
coef_table = pd.DataFrame({
    "Variable": X_COLS,
    "Winter": LR_winter.coef_,
    "Spring": LR_spring.coef_
})

print("\n=== Coefficient Comparison (Winter vs Spring) ===")
print(coef_table.round(3).to_string(index=False))

# ---------- Visualise Coefficient Comparison ----------
coef_table.plot(
    x="Variable", kind="bar", figsize=(7,7),
    title="Comparison of Coefficients (Winter vs Spring)"
)
plt.ylabel("Coefficient Value (seconds per unit)")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()








