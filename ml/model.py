import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

df = pd.read_csv("cleanedData.csv")

X = df[['score', 'sentiment_score']]
y = df['change']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = GradientBoostingRegressor(
    n_estimators=200,      
    learning_rate=0.05,    
    max_depth=4,           
    subsample=0.8,         
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

import joblib

joblib.dump(model, 'gbt_model.pkl')
