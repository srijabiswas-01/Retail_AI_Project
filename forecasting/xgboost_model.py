import pandas as pd
from pathlib import Path
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from xgboost import XGBRegressor
import joblib
import numpy as np

# =====================================
# Project Path
# =====================================

project = Path(__file__).resolve().parent.parent

# =====================================
# Load Dataset
# =====================================

df = pd.read_csv(
    project /
    "forecasting" /
    "data" /
    "forecast_dataset.csv"
)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

print("\nDataset Shape")
print(df.shape)

# =====================================
# Features
# =====================================

features = [
    "product_id",
    "year",
    "month",
    "week",
    "day",
    "weekday",
    "quarter",
    "weekend",
    "lag_1",
    "lag_7",
    "lag_30",
    "rolling_7",
    "rolling_30"
]

target = "quantity"

split_date = df["date"].quantile(0.8)
train = df[df["date"] <= split_date]
test = df[df["date"] > split_date]

if test.empty:
    split_index = int(len(df) * 0.8)
    train = df.iloc[:split_index]
    test = df.iloc[split_index:]

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

# =====================================
# Model
# =====================================

model = XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# =====================================
# Train
# =====================================

print("\nTraining Model...")

model.fit(
    X_train,
    y_train
)

# =====================================
# Prediction
# =====================================

pred = model.predict(
    X_test
)

# =====================================
# Metrics
# =====================================

mae = mean_absolute_error(
    y_test,
    pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        pred
    )
)

r2 = r2_score(
    y_test,
    pred
)

print("\nResults")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")

# =====================================
# Feature Importance
# =====================================

importance = pd.DataFrame({
    "feature": features,
    "importance":
        model.feature_importances_
})

importance = (
    importance
    .sort_values(
        "importance",
        ascending=False
    )
)

print("\nFeature Importance")
print(importance)

# =====================================
# Save
# =====================================

importance.to_csv(
    project /
    "reports" /
    "xgboost_feature_importance.csv",
    index=False
)

metrics = pd.DataFrame({
    "model": ["XGBoost"],
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2],
    "train_rows": [len(train)],
    "test_rows": [len(test)]
})

metrics.to_csv(
    project / "reports" / "xgboost_metrics.csv",
    index=False
)

joblib.dump(
    model,
    project /
    "models" /
    "xgboost_model.pkl"
)

print("\nModel Saved")
