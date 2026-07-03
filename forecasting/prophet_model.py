import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


project = Path(__file__).resolve().parent.parent

sales_daily = pd.read_csv(project / "data/processed/sales_daily.csv")
sales_daily["date"] = pd.to_datetime(sales_daily["date"])

df = (
    sales_daily[["date", "quantity"]]
    .rename(columns={"date": "ds", "quantity": "y"})
    .sort_values("ds")
)

split_index = max(int(len(df) * 0.8), len(df) - 30)
train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=True,
    daily_seasonality=False,
)

model.fit(train)

future = model.make_future_dataframe(periods=len(test) + 30)
forecast = model.predict(future)

evaluation = test.merge(
    forecast[["ds", "yhat"]],
    on="ds",
    how="left",
)

mae = mean_absolute_error(evaluation["y"], evaluation["yhat"])
rmse = np.sqrt(mean_squared_error(evaluation["y"], evaluation["yhat"]))
r2 = r2_score(evaluation["y"], evaluation["yhat"])

forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(
    project / "forecasting" / "prophet_forecast.csv",
    index=False,
)

joblib.dump(model, project / "models" / "prophet_model.pkl")

metrics = pd.DataFrame({
    "model": ["Prophet"],
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2],
    "train_rows": [len(train)],
    "test_rows": [len(test)],
})

metrics.to_csv(project / "reports" / "prophet_metrics.csv", index=False)

print("\nProphet metrics")
print(metrics)
print("\nForecast saved")
