import pandas as pd
from pathlib import Path

# =====================================
# Project Path
# =====================================

project = Path(__file__).resolve().parent.parent

# =====================================
# Load Similarity Matrix
# =====================================

print("\nLoading similarity matrix...")

similarity = pd.read_csv(
    project /
    "recommendation" /
    "item_similarity.csv",
    index_col=0
)
similarity.index = similarity.index.astype(int)
similarity.columns = similarity.columns.astype(int)

print(similarity.shape)

# =====================================
# Generate Recommendations
# =====================================

recommendations = []

products = similarity.index.tolist()

for product in products:

    recs = (
        similarity.loc[product]
        .sort_values(ascending=False)
        .iloc[1:11]
    )

    for rank, (rec, score) in enumerate(
        recs.items(),
        start=1
    ):

        recommendations.append([
            product,
            rec,
            rank,
            score
        ])

recommendations = pd.DataFrame(
    recommendations,
    columns=[
        "product_id",
        "recommended_product",
        "rank",
        "similarity_score"
    ]
)
recommendations = recommendations.sort_values(
    ["product_id", "rank"]
)

# =====================================
# Save
# =====================================

recommendations.to_csv(
    project /
    "recommendation" /
    "top_recommendations.csv",
    index=False
)

print("\nGenerated")
print(recommendations.head())

print("\nShape")
print(recommendations.shape)
