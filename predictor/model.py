import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('../input/stock-prices/train.csv')
test_df = pd.read_csv('../input/stock-prices/test.csv')

X = df.drop(["SalePrice"], axis = 1)
X = X.drop(["Id"], axis = 1)
X_test = test_df

y = df["SalePrice"]

label_encoder = preprocessing.LabelEncoder()
for (columnName, columnData) in X.iteritems():
    if(X[columnName].dtype == object):
        X[columnName]= label_encoder.fit_transform(X[columnName])

for (columnName, columnData) in X_test.iteritems():
    if(X_test[columnName].dtype == object):
        X_test[columnName]= label_encoder.fit_transform(X_test[columnName])

for (columnName, columnData) in X.iteritems():
    X[columnName].fillna(X[columnName].mean(), inplace=True)
    
for (columnName, columnData) in X_test.iteritems():
    X_test[columnName].fillna(X_test[columnName].mean(), inplace=True)
    
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.20, random_state=42)

model = GradientBoostingRegressor(learning_rate = 0.04, max_depth = 4, n_estimators = 1000, subsample = 0.5)
model.fit(X_train.values, y_train)

y_pred = model.predict(X_val)

print('RMSE:', mean_squared_error(y_val, y_pred,squared=False))
print('MAE:', mean_absolute_error(y_val, y_pred))
plt.scatter(y_val, y_pred)
a, b = np.polyfit(y_val, y_pred, 1)
plt.plot(y_val, a*y_val+b, color="black")