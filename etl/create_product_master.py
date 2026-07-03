import pandas as pd
import numpy as np
from pathlib import Path

project = Path(__file__).resolve().parent.parent

events = pd.read_csv(
    project/"data/raw/events.csv"
)

products = pd.DataFrame()

products["product_id"] = (
    events["itemid"]
    .unique()
)

np.random.seed(42)

brands = [
    "Samsung",
    "Apple",
    "Sony",
    "LG",
    "Dell",
    "HP",
    "Nike",
    "Adidas",
    "Puma",
    "Lenovo"
]

products["brand"] = np.random.choice(
    brands,
    len(products)
)

products["unit_price"] = (
    np.random.randint(
        10,
        5000,
        len(products)
    )
)

products["cost_price"] = (
    products["unit_price"]
    * 0.65
)

products["profit_margin"] = (
    (
        products["unit_price"]
        -
        products["cost_price"]
    )
    /
    products["unit_price"]
) * 100

products.to_csv(
    project/
    "data/staging/product_master.csv",
    index=False
)

print(products.head())
print(products.shape)