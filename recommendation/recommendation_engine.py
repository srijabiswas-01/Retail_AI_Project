import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# =====================================================
# Project Path
# =====================================================

project = Path(__file__).resolve().parent.parent

# =====================================================
# Load Events
# =====================================================

print("\nLoading dataset...")

events = pd.read_csv(
    project /
    "data/raw/events.csv"
)

print("Original Shape:")
print(events.shape)

# =====================================================
# Interaction Score
# =====================================================

score_map = {
    "view": 1,
    "addtocart": 3,
    "transaction": 5
}

events["score"] = (
    events["event"]
    .map(score_map)
)

# =====================================================
# Rename Columns
# =====================================================

events.rename(
    columns={
        "visitorid": "customer_id",
        "itemid": "product_id"
    },
    inplace=True
)

# =====================================================
# Top Products
# =====================================================

print("\nSelecting top products...")

top_products = (
    events["product_id"]
    .value_counts()
    .head(3000)
    .index
)

events = events[
    events["product_id"]
    .isin(top_products)
]

print(
    "Products:",
    events["product_id"].nunique()
)

# =====================================================
# Active Customers
# =====================================================

print("\nSelecting active customers...")

top_customers = (
    events["customer_id"]
    .value_counts()
    .head(50000)
    .index
)

events = events[
    events["customer_id"]
    .isin(top_customers)
]

print(
    "Customers:",
    events["customer_id"].nunique()
)

# =====================================================
# Customer Product Matrix
# =====================================================

print("\nCreating interaction matrix...")

matrix = (
    events
    .pivot_table(
        index="customer_id",
        columns="product_id",
        values="score",
        aggfunc="sum",
        fill_value=0
    )
)

print(
    "\nMatrix Shape:"
)

print(
    matrix.shape
)

# =====================================================
# Cosine Similarity
# =====================================================

print(
    "\nCalculating similarity..."
)

similarity = cosine_similarity(
    matrix.T
)

similarity_df = pd.DataFrame(
    similarity,
    index=matrix.columns,
    columns=matrix.columns
)

print(
    similarity_df.shape
)

# =====================================================
# Save Model
# =====================================================

joblib.dump(
    similarity_df,
    project /
    "models" /
    "recommendation_model.pkl"
)

similarity_df.to_csv(
    project /
    "recommendation" /
    "item_similarity.csv"
)

# =====================================================
# Example Recommendation
# =====================================================

product = (
    similarity_df.index[0]
)

recommendations = (
    similarity_df[product]
    .sort_values(
        ascending=False
    )
    .head(10)
)

print("\nSample Product:")
print(product)

print(
    "\nTop Recommendations:"
)

print(
    recommendations
)

print(
    "\nRecommendation Engine Built Successfully"
)