import pandas as pd
from pathlib import Path

# ====================================
# Project Path
# ====================================

project = Path(__file__).resolve().parent.parent

# ====================================
# Load Sales
# ====================================

sales = pd.read_csv(
    project /
    "data/staging/sales_fact.csv"
)

sales["date"] = pd.to_datetime(
    sales["date_key"],
    format="%Y%m%d"
)

# ====================================
# Reference Date (Snapshot)
# ====================================

snapshot = sales["date"].max()

# ====================================
# RFM Calculation
# ====================================

rfm = (
    sales
    .groupby("customer_id")
    .agg({
        "date": lambda x: (snapshot - x.max()).days,
        "sales_id": "count",
        "sales_amount": "sum"
    })
)

rfm.columns = [
    "recency",
    "frequency",
    "monetary"
]

rfm = rfm.reset_index()

# ====================================
# SAFE RFM SCORING (FIXED)
# Avoid qcut crash when data has duplicates / low variance
# ====================================

def safe_qcut(series, q=5, reverse=False):
    """
    Safe quantile binning function
    Works even if unique values < bins
    """
    try:
        bins = pd.qcut(series, q=q, duplicates="drop", labels=False)
    except Exception:
        bins = pd.cut(series.rank(method="first"), q, labels=False)

    if reverse:
        bins = bins.max() - bins

    return bins + 1


# Recency (lower is better → reverse scoring)
rfm["R"] = safe_qcut(rfm["recency"], q=5, reverse=True)

# Frequency (higher is better)
rfm["F"] = safe_qcut(rfm["frequency"], q=5)

# Monetary (higher is better)
rfm["M"] = safe_qcut(rfm["monetary"], q=5)

# ====================================
# Combine Score
# ====================================

rfm["RFM_SCORE"] = (
    rfm["R"].astype(str) +
    rfm["F"].astype(str) +
    rfm["M"].astype(str)
)

# ====================================
# Save Output
# ====================================

output_path = project / "customer_analytics" / "rfm_analysis.csv"

rfm.to_csv(output_path, index=False)

# ====================================
# Debug Output
# ====================================

print("\nRFM Sample:")
print(rfm.head())

print("\nShape:")
print(rfm.shape)

print("\nSaved to:")
print(output_path)
