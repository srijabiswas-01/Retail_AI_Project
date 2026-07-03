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


page_config("Inventory Optimization")

page_header(
    "Inventory Optimization",
    "Stock health, reorder signals, and warehouse-level inventory risk.",
    "icon-inventory",
)

df = cached_csv("inventory/inventory_optimization.csv")
if df is None:
    st.error("Inventory optimization file is missing.")
    st.stop()

required = {"product_id", "warehouse_id", "current_stock", "reorder_point", "stockout", "inventory_status"}
if not require_columns(df, required, "Inventory optimization"):
    st.stop()

status_options = ["All"] + sorted(df["inventory_status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Inventory status", status_options)

filtered = df.copy()
if selected_status != "All":
    filtered = filtered[filtered["inventory_status"] == selected_status]

metric_row(
    [
        ("Products", format_number(filtered["product_id"].nunique()), "Selected rows"),
        ("Warehouses", format_number(filtered["warehouse_id"].nunique()), "Stock locations"),
        ("Current Stock", format_number(filtered["current_stock"].sum()), "Units on hand"),
        ("Stockout Rows", format_number(filtered["stockout"].sum()), "Risk flags"),
    ]
)

section_title("Inventory Status Mix", "icon-inventory")
status_counts = filtered["inventory_status"].value_counts().reset_index()
status_counts.columns = ["inventory_status", "rows"]
fig_status = px.bar(status_counts, x="inventory_status", y="rows", title="Rows by Inventory Status")
st.plotly_chart(fig_status, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    section_title("Warehouse Stock", "icon-dashboard")
    warehouse_stock = (
        filtered.groupby("warehouse_id", as_index=False)
        .agg(current_stock=("current_stock", "sum"), reorder_point=("reorder_point", "sum"))
        .sort_values("current_stock", ascending=False)
    )
    fig_warehouse = px.bar(
        warehouse_stock,
        x="warehouse_id",
        y=["current_stock", "reorder_point"],
        title="Stock vs Reorder Point by Warehouse",
    )
    fig_warehouse.update_layout(legend_title_text="Metric")
    st.plotly_chart(fig_warehouse, use_container_width=True)

with col2:
    section_title("Highest Reorder Pressure", "icon-alert")
    pressure = filtered.assign(
        reorder_gap=filtered["reorder_point"] - filtered["current_stock"]
    ).sort_values("reorder_gap", ascending=False)
    st.dataframe(
        pressure[
            [
                "product_id",
                "warehouse_id",
                "current_stock",
                "reorder_point",
                "reorder_gap",
                "inventory_status",
            ]
        ].head(20),
        use_container_width=True,
    )

section_title("Inventory Records", "icon-inventory")
st.dataframe(filtered.head(500), use_container_width=True)
