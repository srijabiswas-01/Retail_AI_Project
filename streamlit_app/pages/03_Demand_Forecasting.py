import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


page_config("Demand Forecasting")

page_header(
    "Demand Forecasting",
    "Historical demand trends, model output, and feature signals for forecasting workflows.",
    "icon-forecast",
)

forecast_df = cached_csv("forecasting/data/forecast_dataset.csv", ("date",))
if forecast_df is None:
    st.error("Forecast dataset is missing. Run forecasting/create_forecasting_dataset.py.")
    st.stop()

if not require_columns(forecast_df, {"date", "product_id", "quantity", "sales_amount"}, "Forecast dataset"):
    st.stop()

products = sorted(forecast_df["product_id"].dropna().unique().tolist())
selected_product = st.sidebar.selectbox("Product filter", ["All products"] + products)

filtered = forecast_df.copy()
if selected_product != "All products":
    filtered = filtered[filtered["product_id"] == selected_product]

daily_sales = (
    filtered.groupby("date", as_index=False)
    .agg(sales_amount=("sales_amount", "sum"), quantity=("quantity", "sum"))
    .sort_values("date")
)

metric_row(
    [
        ("Rows", format_number(len(filtered)), "Forecast training rows"),
        ("Products", format_number(filtered["product_id"].nunique()), "Selected scope"),
        ("Sales Amount", format_number(filtered["sales_amount"].sum()), "Historical total"),
        ("Quantity", format_number(filtered["quantity"].sum()), "Historical demand"),
    ]
)

section_title("Historical Demand", "icon-sales")
fig = px.line(
    daily_sales,
    x="date",
    y=["sales_amount", "quantity"],
    markers=True,
    title="Daily Sales Amount and Quantity",
)
fig.update_layout(legend_title_text="Metric")
st.plotly_chart(fig, use_container_width=True)

section_title("Prophet Forecast", "icon-forecast")
prophet = cached_csv("forecasting/prophet_forecast.csv", ("ds",))

if prophet is not None and {"ds", "yhat", "yhat_lower", "yhat_upper"}.issubset(prophet.columns):
    fig_forecast = go.Figure()
    fig_forecast.add_trace(
        go.Scatter(x=prophet["ds"], y=prophet["yhat"], mode="lines", name="Forecast")
    )
    fig_forecast.add_trace(
        go.Scatter(
            x=pd.concat([prophet["ds"], prophet["ds"].iloc[::-1]]),
            y=pd.concat([prophet["yhat_upper"], prophet["yhat_lower"].iloc[::-1]]),
            fill="toself",
            fillcolor="rgba(115, 167, 255, 0.18)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Forecast range",
        )
    )
    fig_forecast.update_layout(title="Prophet Prediction Interval", xaxis_title="Date", yaxis_title="Forecast")
    st.plotly_chart(fig_forecast, use_container_width=True)
else:
    st.info("Prophet forecast file is not available.")

section_title("Model Performance", "icon-dashboard")
metrics = []
for model, path in {
    "LightGBM": "reports/lightgbm_metrics.csv",
    "LSTM": "reports/lstm_metrics.csv",
    "XGBoost": "reports/xgboost_metrics.csv",
    "Prophet": "reports/prophet_metrics.csv",
}.items():
    temp = cached_csv(path)
    if temp is not None:
        temp["model"] = model
        metrics.append(temp)

if metrics:
    st.dataframe(pd.concat(metrics, ignore_index=True), use_container_width=True)
else:
    st.info("No model metrics files were found.")

section_title("Feature Importance", "icon-inventory")
importance = cached_csv("reports/xgboost_feature_importance.csv")

if importance is not None and {"feature", "importance"}.issubset(importance.columns):
    fig_importance = px.bar(
        importance.sort_values("importance", ascending=True).tail(12),
        x="importance",
        y="feature",
        orientation="h",
        title="Top Forecasting Features",
    )
    st.plotly_chart(fig_importance, use_container_width=True)
else:
    st.info("Feature importance file is not available.")
