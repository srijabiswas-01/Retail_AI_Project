import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from lightgbm import LGBMRegressor

# =====================================
# Project Path
# =====================================

project = Path(__file__).resolve().parent.parent

# =====================================
# Load Data
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

model = LGBMRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    random_state=42
)

print("\nTraining LightGBM...")

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
# Save Model
# =====================================

joblib.dump(
    model,
    project /
    "models" /
    "lightgbm_model.pkl"
)

# =====================================
# Save Importance
# =====================================

importance.to_csv(
    project /
    "reports" /
    "lightgbm_feature_importance.csv",
    index=False
)

# =====================================
# Save Metrics
# =====================================

metrics = pd.DataFrame({
    "model":["LightGBM"],
    "MAE":[mae],
    "RMSE":[rmse],
    "R2":[r2],
    "train_rows":[len(train)],
    "test_rows":[len(test)]
})

metrics.to_csv(
    project /
    "reports" /
    "lightgbm_metrics.csv",
    index=False
)

print("\nLightGBM Model Saved")
