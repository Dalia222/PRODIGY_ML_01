# -*- coding: utf-8 -*-
"""Prodigy_Infotech_01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15CbTXJZ0CjIpRHtxED_fpHwtoTcb63os
"""

!kaggle competitions download -c house-prices-advanced-regression-techniques

dataset_path = '/content/Prodigy_01'
!mkdir -p ~/.kaggle
!cp "/content/drive/MyDrive/kaggle.json" ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle competitions download -c house-prices-advanced-regression-techniques -p "{dataset_path}"
!unzip -q "{dataset_path}/house-prices-advanced-regression-techniques.zip" -d "{dataset_path}"

# @title imports
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.impute import SimpleImputer

# @title acquiring data files
train_data = pd.read_csv('/content/Prodigy_01/train.csv')
test_data = pd.read_csv('/content/Prodigy_01/test.csv')

# @title data analysis
print(train_data)
# Check for missing values
print(train_data.isnull().sum())
train_data.describe()

#@title Extract features (X) and target variable (y) from the training set
X_train = train_data[['PoolArea', 'WoodDeckSF', 'LotArea', 'MasVnrArea', 'GarageArea', 'TotalBsmtSF', 'FullBath','BedroomAbvGr']]
y_train = train_data['SalePrice']

# Extract features (X) from the test set
X_test = test_data[['PoolArea', 'WoodDeckSF', 'LotArea', 'MasVnrArea', 'GarageArea', 'TotalBsmtSF', 'BedroomAbvGr', 'FullBath']]

#@title handling missing values
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

# Separate numeric and non-numeric columns
numeric_cols = X_train.select_dtypes(include=['number']).columns
non_numeric_cols = X_train.select_dtypes(exclude=['number']).columns

# Create transformers for numeric and non-numeric columns
numeric_transformer = SimpleImputer(strategy='mean')
non_numeric_transformer = SimpleImputer(strategy='most_frequent')

# Create a column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('non_num', non_numeric_transformer, non_numeric_cols)
    ])

# Create a pipeline with the preprocessor and the model
model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', LinearRegression())])
# Drop rows with missing values
train_data = train_data.dropna()
missing_values = train_data.isnull().sum()
total_rows = train_data.shape[0]
missing_info = pd.DataFrame({
    'Column': missing_values.index,
    'Missing Values': missing_values.values,
    'Percentage': (missing_values / total_rows) * 100
})
missing_info
columns_with_missing_values = missing_info[missing_info['Missing Values'] > 0]
print("\nColumns with Missing Values Train_set:")
columns_with_missing_values

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

#@title training the model & evaluation matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Train the linear regression model
model.fit(X_train, y_train)

# Make predictions on the validation set
y_val_pred = model.predict(X_val)

# Evaluate the model
mse = mean_squared_error(y_val, y_val_pred)
mae = mean_absolute_error(y_val, y_val_pred)
r2 = r2_score(y_val, y_val_pred)

print(f'Mean Squared Error on Validation Set: {mse}')
print(f'Mean Absolute Error on Validation Set: {mae}')
print(f'R-squared Score on Validation Set: {r2}')

#@title Plotting
plt.figure(figsize=(10, 6))
plt.scatter(y_val, y_val_pred)
plt.plot([min(y_val), max(y_val)], [min(y_val_pred), max(y_val_pred)], color='gray', linestyle=':', linewidth=2)
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual Prices vs Predicted Prices with Regression Line")
plt.show()