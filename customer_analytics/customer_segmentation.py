import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ====================================
# Project Path
# ====================================

project = Path(__file__).resolve().parent.parent

# ====================================
# Load RFM Data
# ====================================

rfm = pd.read_csv(
    project / "customer_analytics" / "rfm_analysis.csv"
)

print("\nLoaded RFM shape:", rfm.shape)

# ====================================
# Features for Clustering
# ====================================

X = rfm[["recency", "frequency", "monetary"]]

# ====================================
# Scaling (VERY IMPORTANT)
# ====================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ====================================
# KMeans Model
# ====================================

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

rfm["cluster"] = kmeans.fit_predict(X_scaled)

# ====================================
# Cluster Interpretation (Business Mapping)
# ====================================

cluster_summary = rfm.groupby("cluster").agg({
    "recency": "mean",
    "frequency": "mean",
    "monetary": "mean"
}).reset_index()

print("\nCluster Summary:")
print(cluster_summary)

# ====================================
# Segment Labeling (Business Logic)
# ====================================

rfm["recency_percentile"] = 1 - rfm["recency"].rank(pct=True)
rfm["frequency_percentile"] = rfm["frequency"].rank(pct=True)
rfm["monetary_percentile"] = rfm["monetary"].rank(pct=True)


def label_customer(row):
    if row["frequency_percentile"] >= 0.95 and row["monetary_percentile"] >= 0.80:
        return "VIP Customer"
    if row["frequency_percentile"] >= 0.90:
        return "Loyal Customer"
    if row["monetary_percentile"] >= 0.90:
        return "High Value Customer"
    if row["recency_percentile"] >= 0.75:
        return "Recent Customer"
    if row["recency_percentile"] <= 0.25:
        return "At Risk Customer"
    return "Regular Customer"


rfm["segment"] = rfm.apply(label_customer, axis=1)

rfm = rfm.drop(
    columns=[
        "recency_percentile",
        "frequency_percentile",
        "monetary_percentile",
    ]
)

# ====================================
# Save Output
# ====================================

output_path = project / "customer_analytics" / "customer_segments.csv"

rfm.to_csv(output_path, index=False)

print("\nSaved to:", output_path)

print("\nSegment Distribution:")
print(rfm["segment"].value_counts())
