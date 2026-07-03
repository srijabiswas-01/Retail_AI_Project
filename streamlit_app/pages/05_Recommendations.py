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


page_config("Recommendations")

page_header(
    "Recommendations",
    "Product-to-product recommendations generated from collaborative behavior signals.",
    "icon-recommend",
)

df = cached_csv("recommendation/top_recommendations.csv")
if df is None:
    st.error("Recommendation output file is missing.")
    st.stop()

required = {"product_id", "recommended_product", "rank", "similarity_score"}
if not require_columns(df, required, "Top recommendations"):
    st.stop()

products = sorted(df["product_id"].dropna().unique().tolist())
selected_product = st.sidebar.selectbox("Product", ["All products"] + products)

filtered = df.copy()
if selected_product != "All products":
    filtered = filtered[filtered["product_id"] == selected_product]

metric_row(
    [
        ("Source Products", format_number(filtered["product_id"].nunique()), "Recommendation anchors"),
        ("Recommendations", format_number(len(filtered)), "Visible rows"),
        ("Avg Similarity", format_number(filtered["similarity_score"].mean(), 3), "Mean match score"),
        ("Max Rank", format_number(filtered["rank"].max()), "Recommendation depth"),
    ]
)

section_title("Recommendation Strength", "icon-recommend")
chart_df = filtered.sort_values("similarity_score", ascending=False).head(25)
fig = px.bar(
    chart_df,
    x="similarity_score",
    y="recommended_product",
    color="rank",
    orientation="h",
    title="Top Recommended Products by Similarity",
)
fig.update_yaxes(type="category")
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    section_title("Recommendations Table", "icon-dashboard")
    st.dataframe(
        filtered.sort_values(["product_id", "rank"]).head(500),
        use_container_width=True,
    )

with col2:
    section_title("Most Recommended Items", "icon-sales")
    popular = (
        df.groupby("recommended_product", as_index=False)
        .agg(times_recommended=("product_id", "count"), avg_similarity=("similarity_score", "mean"))
        .sort_values("times_recommended", ascending=False)
        .head(20)
    )
    st.dataframe(popular, use_container_width=True)
