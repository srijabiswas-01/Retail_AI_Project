import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent.parent

events = pd.read_csv(
    project /
    "data/raw/events.csv"
)

# convert timestamp
events["timestamp"] = pd.to_datetime(
    events["timestamp"],
    unit="ms"
)

# remove duplicates
events = events.drop_duplicates()

# remove nulls
events = events.dropna()

# rename
events.rename(
    columns={
        "visitorid":"customer_id",
        "itemid":"product_id"
    },
    inplace=True
)

events.to_csv(
    project /
    "data/processed/cleaned_events.csv",
    index=False
)

print(events.head())
print(events.shape)