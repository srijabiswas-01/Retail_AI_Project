import pandas as pd
import numpy as np
from pathlib import Path

project = Path(__file__).resolve().parent.parent

events = pd.read_csv(
    project/"data/raw/events.csv"
)

customers = pd.DataFrame()

customers["customer_id"] = (
    events["visitorid"]
    .unique()
)

gender = [
    "Male",
    "Female"
]

income = [
    "Low",
    "Middle",
    "High"
]

segment = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum"
]

np.random.seed(42)

customers["gender"] = (
    np.random.choice(
        gender,
        len(customers)
    )
)

customers["income_group"] = (
    np.random.choice(
        income,
        len(customers)
    )
)

customers["customer_segment"] = (
    np.random.choice(
        segment,
        len(customers)
    )
)

customers.to_csv(
    project/
    "data/staging/customer_master.csv",
    index=False
)

print(customers.head())
print(customers.shape)