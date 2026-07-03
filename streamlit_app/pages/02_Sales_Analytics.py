import sys
from pathlib import Path

import plotly.express as px
import streamlit as st


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.append(str(APP_ROOT))

from utils.data_loader import (  # noqa: E402
    cached_csv,
    format_number,
    metric_row,
    page_config,
    page_header,
    require_columns,
    section_title,
)


page_config("Sales Analytics")

page_header(
    "Sales Analytics",
    "Revenue, orders, quantity, and profitability trends from the processed sales dataset.",
    "icon-sales",
)

df = cached_csv("data/processed/sales_daily.csv", ("date",))
if df is None:
    st.error("Sales daily dataset is missing.")
    st.stop()

if not require_columns(df, {"date", "revenue", "orders", "quantity", "profit"}, "Sales daily"):
    st.stop()

df = df.sort_values("date")

date_range = st.sidebar.date_input("Date range", [df["date"].min(), df["date"].max()])
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]

metric_row(
    [
        ("Revenue", format_number(df["revenue"].sum()), "Filtered total"),
        ("Orders", format_number(df["orders"].sum()), "Filtered total"),
        ("Quantity", format_number(df["quantity"].sum()), "Units sold"),
        ("Profit", format_number(df["profit"].sum()), "Filtered total"),
    ]
)

section_title("Revenue Trend", "icon-sales")
fig = px.line(df, x="date", y="revenue", markers=True, title="Daily Revenue")
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    section_title("Orders and Quantity", "icon-dashboard")
    fig_orders = px.bar(df, x="date", y=["orders", "quantity"], title="Daily Orders and Quantity")
    fig_orders.update_layout(legend_title_text="Metric")
    st.plotly_chart(fig_orders, use_container_width=True)

with col2:
    section_title("Profit Trend", "icon-forecast")
    fig_profit = px.line(df, x="date", y="profit", markers=True, title="Daily Profit")
    st.plotly_chart(fig_profit, use_container_width=True)

section_title("Recent Sales Rows", "icon-inventory")
st.dataframe(
    df[["date", "revenue", "orders", "quantity", "profit"]]
    .sort_values("date", ascending=False)
    .head(25),
    use_container_width=True,
)
