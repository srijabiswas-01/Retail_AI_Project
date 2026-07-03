import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent.parent

events = pd.read_csv(
    project /
    "data/processed/cleaned_events.csv"
)

product = (
    events
    .groupby("product_id")
    .agg(
        views=("event","count"),
        customers=("customer_id","nunique")
    )
    .reset_index()
)

product.to_csv(
    project /
    "data/processed/product_features.csv",
    index=False
)

print(product.head())