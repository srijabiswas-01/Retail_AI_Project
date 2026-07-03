import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent

events = pd.read_csv(
    project / "data/raw/events.csv"
)

events["timestamp"] = pd.to_datetime(
    events["timestamp"],
    unit="ms"
)

start = events["timestamp"].min()
end = events["timestamp"].max()

dates = pd.date_range(
    start=start,
    end=end,
    freq="D"
)

date_dim = pd.DataFrame()

date_dim["date"] = dates

date_dim["date_key"] = (
    date_dim["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

date_dim["year"] = (
    date_dim["date"]
    .dt.year
)

date_dim["quarter"] = (
    date_dim["date"]
    .dt.quarter
)

date_dim["month"] = (
    date_dim["date"]
    .dt.month
)

date_dim["month_name"] = (
    date_dim["date"]
    .dt.month_name()
)

date_dim["week"] = (
    date_dim["date"]
    .dt.isocalendar()
    .week
)

date_dim["day"] = (
    date_dim["date"]
    .dt.day
)

date_dim["weekday"] = (
    date_dim["date"]
    .dt.day_name()
)

date_dim["is_weekend"] = (
    date_dim["date"]
    .dt.weekday >= 5
)

def season(month):
    if month in [12,1,2]:
        return "Winter"
    elif month in [3,4,5]:
        return "Spring"
    elif month in [6,7,8]:
        return "Summer"
    else:
        return "Autumn"

date_dim["season"] = (
    date_dim["month"]
    .apply(season)
)

date_dim.to_csv(
    project/
    "data/staging/date_dimension.csv",
    index=False
)

print(date_dim.head())
print(date_dim.shape)