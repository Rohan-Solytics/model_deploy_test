import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

print("Running Model 1: Linear Regression")
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])
model = LinearRegression().fit(X, y)
print(f"Prediction for X=6: {model.predict([[6]])}")