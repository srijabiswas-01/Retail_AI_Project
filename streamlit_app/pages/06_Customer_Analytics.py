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


page_config("Customer Analytics")

page_header(
    "Customer Analytics",
    "RFM scoring, customer segmentation, and customer value distribution.",
    "icon-customer",
)

segments = cached_csv("customer_analytics/customer_segments.csv")
rfm = cached_csv("customer_analytics/rfm_analysis.csv")

if segments is None:
    st.error("Customer segments file is missing.")
    st.stop()

required = {"customer_id", "recency", "frequency", "monetary", "RFM_SCORE", "cluster", "segment"}
if not require_columns(segments, required, "Customer segments"):
    st.stop()

segment_options = ["All"] + sorted(segments["segment"].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("Customer segment", segment_options)

filtered = segments.copy()
if selected_segment != "All":
    filtered = filtered[filtered["segment"] == selected_segment]

metric_row(
    [
        ("Customers", format_number(filtered["customer_id"].nunique()), "Selected audience"),
        ("Avg Recency", format_number(filtered["recency"].mean(), 1), "Lower is better"),
        ("Avg Frequency", format_number(filtered["frequency"].mean(), 1), "Purchase activity"),
        ("Avg Monetary", format_number(filtered["monetary"].mean(), 1), "Customer value"),
    ]
)

section_title("Segment Distribution", "icon-customer")
segment_counts = segments["segment"].value_counts().reset_index()
segment_counts.columns = ["segment", "customers"]
fig_segment = px.bar(segment_counts, x="segment", y="customers", title="Customers by Segment")
st.plotly_chart(fig_segment, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    section_title("RFM Value Map", "icon-dashboard")
    fig_scatter = px.scatter(
        filtered.head(5000),
        x="frequency",
        y="monetary",
        color="segment",
        size="recency",
        hover_data=["customer_id", "RFM_SCORE"],
        title="Frequency vs Monetary Value",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    section_title("Cluster Mix", "icon-recommend")
    cluster_counts = filtered["cluster"].value_counts().reset_index()
    cluster_counts.columns = ["cluster", "customers"]
    fig_cluster = px.pie(cluster_counts, names="cluster", values="customers", title="Customers by Cluster")
    st.plotly_chart(fig_cluster, use_container_width=True)

section_title("Customer Segment Table", "icon-customer")
st.dataframe(
    filtered[
        [
            "customer_id",
            "recency",
            "frequency",
            "monetary",
            "RFM_SCORE",
            "cluster",
            "segment",
        ]
    ].head(500),
    use_container_width=True,
)

if rfm is not None:
    with st.expander("Raw RFM analysis"):
        st.dataframe(rfm.head(500), use_container_width=True)
