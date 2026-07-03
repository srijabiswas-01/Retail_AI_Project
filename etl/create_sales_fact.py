import pandas as pd
import numpy as np
from pathlib import Path

# =====================================================
# Project Path
# =====================================================

project = Path(__file__).resolve().parent.parent

# =====================================================
# Load Data
# =====================================================

events = pd.read_csv(
    project /
    "data/raw/events.csv"
)

products = pd.read_csv(
    project /
    "data/staging/product_master.csv"
)

inventory = pd.read_csv(
    project /
    "data/staging/inventory_fact.csv"
)

# =====================================================
# Keep only transactions
# =====================================================

sales = events[
    events["event"] == "transaction"
].copy()

# =====================================================
# Timestamp
# =====================================================

sales["timestamp"] = pd.to_datetime(
    sales["timestamp"],
    unit="ms"
)

sales["date_key"] = (
    sales["timestamp"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# =====================================================
# Rename columns
# =====================================================

sales.rename(
    columns={
        "visitorid":"customer_id",
        "itemid":"product_id"
    },
    inplace=True
)

# =====================================================
# Quantity
# =====================================================

np.random.seed(42)

sales["quantity"] = (
    np.random.randint(
        1,
        5,
        len(sales)
    )
)

# =====================================================
# Merge Product Data
# =====================================================

sales = sales.merge(
    products,
    on="product_id",
    how="left"
)

# =====================================================
# Merge Warehouse
# =====================================================

sales = sales.merge(
    inventory[
        [
            "product_id",
            "warehouse_id"
        ]
    ],
    on="product_id",
    how="left"
)

# =====================================================
# Revenue
# =====================================================

sales["sales_amount"] = (
    sales["quantity"]
    *
    sales["unit_price"]
)

sales["cost_amount"] = (
    sales["quantity"]
    *
    sales["cost_price"]
)

sales["profit"] = (
    sales["sales_amount"]
    -
    sales["cost_amount"]
)

# =====================================================
# Sales ID
# =====================================================

sales["sales_id"] = range(
    1,
    len(sales)+1
)

# =====================================================
# Final Columns
# =====================================================

sales = sales[
    [
        "sales_id",
        "customer_id",
        "product_id",
        "warehouse_id",
        "date_key",
        "quantity",
        "unit_price",
        "sales_amount",
        "cost_amount",
        "profit"
    ]
]

# =====================================================
# Save
# =====================================================

sales.to_csv(
    project /
    "data/staging/sales_fact.csv",
    index=False
)

print(sales.head())
print("\nShape:")
print(sales.shape)

print("\nTotal Revenue:")
print(
    sales["sales_amount"]
    .sum()
)

print("\nTotal Profit:")
print(
    sales["profit"]
    .sum()
)