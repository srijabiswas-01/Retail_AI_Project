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


page_config("Executive Dashboard")

page_header(
    "Executive Dashboard",
    "High-level operating view across activity, sales, products, and customers.",
    "icon-dashboard",
)

summary = cached_csv("reports/summary.csv")
activity = cached_csv("reports/daily_activity.csv", ("date",))
sales_daily = cached_csv("data/processed/sales_daily.csv", ("date",))

if summary is not None and {"metric", "value"}.issubset(summary.columns):
    values = dict(zip(summary["metric"], summary["value"]))
    revenue = sales_daily["revenue"].sum() if sales_daily is not None and "revenue" in sales_daily.columns else 0
    profit = sales_daily["profit"].sum() if sales_daily is not None and "profit" in sales_daily.columns else 0

    metric_row(
        [
            ("Revenue", format_number(revenue), "Total processed sales"),
            ("Profit", format_number(profit), "Total processed margin"),
            ("Views", format_number(values.get("views", 0)), "Customer activity"),
            ("Purchases", format_number(values.get("purchases", 0)), "Completed purchases"),
        ]
    )
else:
    st.warning("Summary report is not available.")

if activity is not None and require_columns(activity, {"date", "events"}, "Daily activity"):
    section_title("Daily Activity", "icon-dashboard")
    fig = px.area(
        activity.sort_values("date"),
        x="date",
        y="events",
        title="Events Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)

if sales_daily is not None and require_columns(sales_daily, {"date", "revenue", "orders", "profit"}, "Sales daily"):
    section_title("Revenue, Orders, and Profit", "icon-sales")

    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.line(
            sales_daily.sort_values("date"),
            x="date",
            y=["revenue", "profit"],
            markers=True,
            title="Daily Revenue and Profit",
        )
        fig.update_layout(legend_title_text="Metric")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.dataframe(
            sales_daily[["date", "revenue", "orders", "profit"]]
            .sort_values("date", ascending=False)
            .head(12),
            use_container_width=True,
        )

section_title("Leaderboards", "icon-recommend")
col1, col2 = st.columns(2)

with col1:
    top_products = cached_csv("reports/top_products.csv")
    st.subheader("Top Products")
    if top_products is not None:
        st.dataframe(top_products.head(10), use_container_width=True)
    else:
        st.info("Top products report is not available.")

with col2:
    top_customers = cached_csv("reports/top_customers.csv")
    st.subheader("Top Customers")
    if top_customers is not None:
        st.dataframe(top_customers.head(10), use_container_width=True)
    else:
        st.info("Top customers report is not available.")
