# Linear Regression model for Assessment 2

import pandas as pd
import math 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

df = pd.read_csv("A3 merged_grouped dataset.csv")

print(df.head())
print(df.shape)

df['hesitation'] = df['bat_landing_to_food'].fillna(0) + df['seconds_after_rat_arrival'].fillna(0)
# print(df.columns.get_loc('hesitation'))
# print(df['hesitation'].head())

# Using the Correlation coefficient to check correlation between response and explanatory variables

x_variables = ['food_availability', 'rat_minutes', 'rat_arrival_number']
y_variable = 'hesitation'

corr_df = df[x_variables + [y_variable]]

corr = corr_df.corr()
print(corr)

plt.figure(figsize=(8,6))
ax = sns.heatmap(corr,
                 vmin=-1,
                 vmax=1,
                 center=0,
                 cmap=sns.diverging_palette(20, 220, n=200),
                 square=False,
                 annot=True 
)

ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)


## Splitting the data

x = df[['food_availability','rat_minutes','rat_arrival_number']].values
y = df['hesitation'].values

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    test_size = 0.2,
                                                    random_state = 0)

LR_model = LinearRegression()

LR_model.fit(x_train, y_train)

# Printing the y-intercept and the coefficient of the model

print("The y-intercept is: (b0)", LR_model.intercept_)
print("The coefficient is: (b1)", LR_model.coef_)

print(f"The equation of the regression model is: y = {LR_model.intercept_} + {LR_model.coef_}x")

### Model Evaluation using metrics:
 
y_predict = LR_model.predict(x_test)

# Mean Absolute Error
mae = metrics.mean_absolute_error(y_test, y_predict)
# Mean Squared Error
mse = metrics.mean_squared_error(y_test, y_predict)
# Root Mean Squared Error
rmse = math.sqrt(mse)
# Normalised Root Mean Squared Error
y_min = y_test.min()
y_max = y_test.max()
nrmse = rmse / (y_max -y_min)

print("The Mean Absolute Error is:", mae)
print("The Mean Squared Error is:", mse)
print("The Root Mean Squared Error is:", rmse)
print("The Normalised Root Mean Squared Error is:", nrmse)


## Building a baseline model to compare the LR model

y_base = np.mean(y_train)
y_predict_base = np.full_like(y_test, y_base)

# print(y_predict_base)

df_predict = pd.DataFrame({"Actual values": y_test,
                           "Predicted values": y_predict_base})

print(df_predict.head())

# Evaluating the baseline model
mae_base = metrics.mean_absolute_error(y_test, y_predict_base)
mse_base = metrics.mean_squared_error(y_test, y_predict_base)
rmse_base = math.sqrt(mse_base)
# NRMSE
y_max = y_test.max()
y_min = y_test.min()
nrmse_base = rmse_base / (y_max - y_min)

print("The mean absolute error for the baseline model is:", mae_base)
print("The mean squared error for the baseline model is:", mse_base)
print("The root mean squared error for the baseline model is:", rmse_base)
print("The normalised root mean squared error for the baseline model is:", nrmse_base)


plt.show()