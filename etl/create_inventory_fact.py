import pandas as pd
import numpy as np
from pathlib import Path

project = Path(__file__).resolve().parent.parent

products = pd.read_csv(
    project/
    "data/staging/product_master.csv"
)

inventory = pd.DataFrame()

inventory["product_id"] = (
    products["product_id"]
)

inventory["warehouse_id"] = (
    np.random.randint(
        1,
        6,
        len(products)
    )
)

inventory["current_stock"] = (
    np.random.randint(
        10,
        1000,
        len(products)
    )
)

inventory["safety_stock"] = (
    np.random.randint(
        5,
        50,
        len(products)
    )
)

inventory["reorder_point"] = (
    np.random.randint(
        20,
        200,
        len(products)
    )
)

inventory["lead_time"] = (
    np.random.randint(
        1,
        15,
        len(products)
    )
)

inventory.to_csv(
    project/
    "data/staging/inventory_fact.csv",
    index=False
)

print(inventory.head())
print(inventory.shape)