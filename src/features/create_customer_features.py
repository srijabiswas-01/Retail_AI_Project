import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent.parent

events = pd.read_csv(
    project /
    "data/processed/cleaned_events.csv"
)

customer = (
    events
    .groupby("customer_id")
    .agg(
        total_events=("event","count"),
        unique_products=("product_id","nunique"),
        first_visit=("timestamp","min"),
        last_visit=("timestamp","max")
    )
    .reset_index()
)

customer["days_active"] = (
    pd.to_datetime(customer["last_visit"])
    -
    pd.to_datetime(customer["first_visit"])
).dt.days

customer.to_csv(
    project /
    "data/processed/customer_features.csv",
    index=False
)

print(customer.head())