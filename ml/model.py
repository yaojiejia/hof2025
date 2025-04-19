import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1. Load data
df = pd.read_csv('your_data.csv')

# 2. Define features and target
features = ['sentiment_score', 'vote_count', 'sector', 'ticker']
target = 'price_change'

# 3. Identify categorical features
cat_features = ['sector', 'ticker']

# 4. Split into train/validation (no shuffle for time series)
X = df[features]
y = df[target]
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

# 5. Initialize CatBoostRegressor
model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    loss_function='RMSE',
    cat_features=cat_features,
    early_stopping_rounds=50,
    verbose=100
)

# 6. Train with early stopping
model.fit(
    X_train, y_train,
    eval_set=(X_val, y_val),
    use_best_model=True
)

# 7. Predict & evaluate
y_pred = model.predict(X_val)
rmse = mean_squared_error(y_val, y_pred, squared=False)
print(f'Validation RMSE: {rmse:.4f}')

# 8. Inspect feature importance
fi = model.get_feature_importance(prettified=True)
print(fi)
