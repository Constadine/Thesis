import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm

final_bird_data = pd.read_csv('data_for_correlation.csv')



# Replace -1 with NaN
filtered_data = final_bird_data.replace(-1, np.nan)

# Impute missing values with the mean of each column
filtered_data['air_pressure_values'].fillna(filtered_data['air_pressure_values'].mean(), inplace=True)
filtered_data['air_temperature_values'].fillna(filtered_data['air_temperature_values'].mean(), inplace=True)
filtered_data['wind_values'].fillna(filtered_data['wind_values'].mean(), inplace=True)
filtered_data['sea_temp_values'].fillna(filtered_data['sea_temp_values'].mean(), inplace=True)
filtered_data['seawater_level_values'].fillna(filtered_data['seawater_level_values'].mean(), inplace=True)
filtered_data['wave_height_values'].fillna(filtered_data['wave_height_values'].mean(), inplace=True)

# Now, select relevant columns for regression
X = filtered_data[['air_pressure_values', 'air_temperature_values', 
                   'wind_values', 'sea_temp_values', 'seawater_level_values', 
                   'wave_height_values']]
y = filtered_data['total_population']

# Check the resulting data shape
print(X.shape)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the linear regression model
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Print the coefficients
coefficients = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
print(coefficients)

# Add a constant to the model (for the intercept)
X_train_sm = sm.add_constant(X_train)

# Fit the model using statsmodels
model_sm = sm.OLS(y_train, X_train_sm).fit()

# Print the model summary
print(model_sm.summary())
