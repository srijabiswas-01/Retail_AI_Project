import pandas as pd

from src.config.paths import FORECASTING_DATA_DIR, STAGING_DATA_DIR
from src.utils.io import read_csv, write_csv, validate_columns


sales = read_csv(STAGING_DATA_DIR / "sales_fact.csv")
validate_columns(
    sales,
    {"product_id", "quantity", "sales_amount", "date_key"},
    "sales_fact",
)
sales["date"] = pd.to_datetime(sales["date_key"], format="%Y%m%d")

top_n = 250
top_products = (
    sales.groupby("product_id")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .index
)

sales = sales[sales["product_id"].isin(top_products)].copy()

daily = (
    sales.groupby(["date", "product_id"], as_index=False)
    .agg(quantity=("quantity", "sum"), sales_amount=("sales_amount", "sum"))
)

date_index = pd.date_range(daily["date"].min(), daily["date"].max(), freq="D")
panel_index = pd.MultiIndex.from_product(
    [date_index, top_products],
    names=["date", "product_id"],
)

daily = (
    daily.set_index(["date", "product_id"])
    .reindex(panel_index, fill_value=0)
    .reset_index()
    .sort_values(["product_id", "date"])
)

daily["year"] = daily["date"].dt.year
daily["month"] = daily["date"].dt.month
daily["week"] = daily["date"].dt.isocalendar().week.astype(int)
daily["day"] = daily["date"].dt.day
daily["weekday"] = daily["date"].dt.weekday
daily["quarter"] = daily["date"].dt.quarter
daily["weekend"] = (daily["weekday"] >= 5).astype(int)

grouped_quantity = daily.groupby("product_id")["quantity"]

daily["lag_1"] = grouped_quantity.shift(1)
daily["lag_7"] = grouped_quantity.shift(7)
daily["lag_30"] = grouped_quantity.shift(30)

daily["rolling_7"] = grouped_quantity.transform(
    lambda values: values.shift(1).rolling(7, min_periods=1).mean()
)
daily["rolling_30"] = grouped_quantity.transform(
    lambda values: values.shift(1).rolling(30, min_periods=1).mean()
)

daily = daily.dropna(subset=["lag_1", "lag_7", "lag_30"]).copy()

output = FORECASTING_DATA_DIR / "forecast_dataset.csv"
write_csv(daily, output)

print(daily.head())
print("\nShape")
print(daily.shape)
print("\nProducts")
print(daily["product_id"].nunique())
