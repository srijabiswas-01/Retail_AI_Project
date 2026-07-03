import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Input, LSTM
from tensorflow.keras.models import Sequential


project = Path(__file__).resolve().parent.parent

sales_daily = pd.read_csv(project / "data/processed/sales_daily.csv")
sales_daily["date"] = pd.to_datetime(sales_daily["date"])
sales_daily = sales_daily.sort_values("date")

series = sales_daily["quantity"].values.reshape(-1, 1)

scaler = MinMaxScaler()
scaled = scaler.fit_transform(series)

window = 14
X = []
y = []

for index in range(window, len(scaled)):
    X.append(scaled[index - window:index, 0])
    y.append(scaled[index, 0])

X = np.array(X)
y = np.array(y)
X = X.reshape(X.shape[0], X.shape[1], 1)

split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = Sequential(
    [
        Input(shape=(window, 1)),
        LSTM(32, activation="tanh"),
        Dense(1),
    ]
)

model.compile(optimizer="adam", loss="mse")

model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=16,
    verbose=1,
)

pred = model.predict(X_test)
pred = scaler.inverse_transform(pred)
actual = scaler.inverse_transform(y_test.reshape(-1, 1))

mae = mean_absolute_error(actual, pred)
rmse = np.sqrt(mean_squared_error(actual, pred))
r2 = r2_score(actual, pred)

model.save(project / "models" / "lstm_model.keras")
joblib.dump(scaler, project / "models" / "lstm_scaler.pkl")

metrics = pd.DataFrame({
    "model": ["LSTM"],
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2],
    "train_rows": [len(X_train)],
    "test_rows": [len(X_test)],
})

metrics.to_csv(project / "reports" / "lstm_metrics.csv", index=False)

print("\nLSTM metrics")
print(metrics)
