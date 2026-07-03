import pandas as pd

from src.config.paths import PROCESSED_DATA_DIR, STAGING_DATA_DIR
from src.utils.io import read_csv, write_csv


sales = read_csv(STAGING_DATA_DIR / "sales_fact.csv")

sales["date"] = pd.to_datetime(
    sales["date_key"],
    format="%Y%m%d"
)

daily = (
    sales
    .groupby("date")
    .agg(
        revenue=("sales_amount","sum"),
        orders=("sales_id","count"),
        quantity=("quantity","sum"),
        profit=("profit","sum")
    )
    .reset_index()
)

write_csv(daily, PROCESSED_DATA_DIR / "sales_daily.csv")

print(daily.head())
