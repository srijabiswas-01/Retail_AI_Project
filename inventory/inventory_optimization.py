import numpy as np
import pandas as pd

from src.config.paths import INVENTORY_DIR, STAGING_DATA_DIR
from src.utils.io import read_csv, write_csv, validate_columns


sales = read_csv(STAGING_DATA_DIR / "sales_fact.csv")
inventory = read_csv(STAGING_DATA_DIR / "inventory_fact.csv")

validate_columns(
    sales,
    {"product_id", "quantity", "date_key"},
    "sales_fact",
)
validate_columns(
    inventory,
    {"product_id", "warehouse_id", "current_stock", "safety_stock", "reorder_point", "lead_time"},
    "inventory_fact",
)

sales["date"] = pd.to_datetime(sales["date_key"], format="%Y%m%d")

daily_demand = (
    sales.groupby(["product_id", "date"], as_index=False)
    .agg(quantity=("quantity", "sum"))
)

demand = (
    daily_demand.groupby("product_id")
    .agg(avg_demand=("quantity", "mean"), std_demand=("quantity", "std"))
    .reset_index()
)

inventory = inventory.merge(demand, on="product_id", how="left")
inventory[["avg_demand", "std_demand"]] = inventory[["avg_demand", "std_demand"]].fillna(0)

service_level = 1.65
inventory["safety_stock_calc"] = (
    service_level * inventory["std_demand"] * np.sqrt(inventory["lead_time"])
)
inventory["reorder_point_calc"] = (
    inventory["avg_demand"] * inventory["lead_time"] + inventory["safety_stock_calc"]
)

inventory["stockout"] = (
    inventory["current_stock"] < inventory["reorder_point_calc"]
).astype(int)

inventory["stock_ratio"] = np.where(
    inventory["reorder_point_calc"] > 0,
    inventory["current_stock"] / inventory["reorder_point_calc"],
    np.inf,
)


def status(row):
    if row["stockout"] == 0:
        return "Safe"
    if row["stock_ratio"] < 0.5:
        return "Critical"
    return "Low Stock"


inventory["inventory_status"] = inventory.apply(status, axis=1)
inventory = inventory.drop(columns=["stock_ratio"])

output = INVENTORY_DIR / "inventory_optimization.csv"
write_csv(inventory, output)

summary = inventory["inventory_status"].value_counts()
print("\nInventory status")
print(summary)
print("\nSaved to")
print(output)
