import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.append(str(APP_ROOT))

from utils.data_loader import (  # noqa: E402
    cached_csv,
    format_number,
    metric_row,
    page_config,
    page_header,
    section_title,
)


page_config("Retail AI Platform")

page_header(
    "Retail AI Intelligence Platform",
    "A working analytics and machine learning workspace for sales, demand, inventory, recommendations, and customer behavior.",
    "icon-logo",
)

summary = cached_csv("reports/summary.csv")
sales_daily = cached_csv("data/processed/sales_daily.csv", ("date",))

if summary is not None and {"metric", "value"}.issubset(summary.columns):
    values = dict(zip(summary["metric"], summary["value"]))
    total_revenue = sales_daily["revenue"].sum() if sales_daily is not None and "revenue" in sales_daily.columns else 0

    metric_row(
        [
            ("Customers", format_number(values.get("customers", 0)), "Unique shoppers observed"),
            ("Products", format_number(values.get("products", 0)), "Catalog items tracked"),
            ("Transactions", format_number(values.get("transactions", 0)), "Purchase events"),
            ("Revenue", format_number(total_revenue), "From processed daily sales"),
        ]
    )
else:
    st.warning("Summary report not found or has unexpected columns.")
    st.info("Run ETL scripts, then refresh this page.")

if sales_daily is not None and {"date", "revenue", "orders", "profit"}.issubset(sales_daily.columns):
    section_title("Sales Overview", "icon-sales")

    chart_df = sales_daily.sort_values("date")
    fig = px.line(
        chart_df,
        x="date",
        y=["revenue", "profit"],
        title="Daily Revenue and Profit",
        markers=True,
    )
    fig.update_layout(legend_title_text="Metric")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section_title("Top Products", "icon-recommend")
        top_products = cached_csv("reports/top_products.csv")
        if top_products is not None:
            st.dataframe(top_products.head(10), use_container_width=True)
        else:
            st.info("Top products report is not available.")

    with col2:
        section_title("Top Customers", "icon-customer")
        top_customers = cached_csv("reports/top_customers.csv")
        if top_customers is not None:
            st.dataframe(top_customers.head(10), use_container_width=True)
        else:
            st.info("Top customers report is not available.")
else:
    st.info("Processed sales data is not ready yet.")
