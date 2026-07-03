# =====================================================
# Retail AI Platform
# Phase 1: Data Understanding & Exploratory Analysis
# File: notebooks/01_data_understanding.py
# =====================================================

import pandas as pd
from pathlib import Path


# =====================================================
# Helper Function
# =====================================================
def section(title):
    print("\n")
    print("=" * 60)
    print(title)
    print("=" * 60)


# =====================================================
# Main Function
# =====================================================
def main():

    # -----------------------------------------------
    # Project Paths
    # -----------------------------------------------
    project_root = Path(__file__).resolve().parent.parent

    raw_path = project_root / "data" / "raw"
    report_path = project_root / "reports"

    report_path.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------
    # Load Dataset
    # -----------------------------------------------
    section("Loading Datasets")

    events = pd.read_csv(
        raw_path / "events.csv"
    )

    category = pd.read_csv(
        raw_path / "category_tree.csv"
    )

    print(f"Events Shape      : {events.shape}")
    print(f"Category Shape    : {category.shape}")

    # -----------------------------------------------
    # Dataset Information
    # -----------------------------------------------
    section("Dataset Information")

    print("\nColumns:")
    print(events.columns.tolist())

    print("\nFirst 5 Rows:")
    print(events.head())

    # -----------------------------------------------
    # Memory Usage
    # -----------------------------------------------
    section("Memory Usage")

    memory = (
        events.memory_usage(deep=True)
        .sum() / 1024**2
    )

    print(f"Events Memory: {memory:.2f} MB")

    # -----------------------------------------------
    # Missing Values
    # -----------------------------------------------
    section("Missing Values")

    print(events.isnull().sum())

    # -----------------------------------------------
    # Convert Timestamp
    # -----------------------------------------------
    section("Timestamp Conversion")

    events["timestamp"] = pd.to_datetime(
        events["timestamp"],
        unit="ms"
    )

    print(
        f"Start Date: {events['timestamp'].min()}"
    )

    print(
        f"End Date: {events['timestamp'].max()}"
    )

    # -----------------------------------------------
    # Event Analysis
    # -----------------------------------------------
    section("Event Distribution")

    event_counts = (
        events["event"]
        .value_counts()
    )

    print(event_counts)

    # -----------------------------------------------
    # Business KPIs
    # -----------------------------------------------
    section("Business KPIs")

    total_customers = (
        events["visitorid"]
        .nunique()
    )

    total_products = (
        events["itemid"]
        .nunique()
    )

    total_transactions = (
        events["transactionid"]
        .notnull()
        .sum()
    )

    print(
        f"Total Customers     : {total_customers:,}"
    )

    print(
        f"Total Products      : {total_products:,}"
    )

    print(
        f"Total Transactions  : {total_transactions:,}"
    )

    # -----------------------------------------------
    # Customer Funnel
    # -----------------------------------------------
    section("Customer Funnel")

    views = (
        events["event"] == "view"
    ).sum()

    cart = (
        events["event"] == "addtocart"
    ).sum()

    purchases = (
        events["event"] == "transaction"
    ).sum()

    print(f"Views       : {views:,}")
    print(f"Add To Cart : {cart:,}")
    print(f"Purchases   : {purchases:,}")

    if views > 0:

        cart_rate = (
            cart / views
        ) * 100

        purchase_rate = (
            purchases / views
        ) * 100

        print(
            f"\nView → Cart Conversion      : {cart_rate:.2f}%"
        )

        print(
            f"View → Purchase Conversion : {purchase_rate:.2f}%"
        )

    # -----------------------------------------------
    # Daily Demand
    # -----------------------------------------------
    section("Daily Demand Analysis")

    daily_activity = (
        events
        .groupby(
            events["timestamp"].dt.date
        )
        .size()
        .reset_index()
    )

    daily_activity.columns = [
        "date",
        "events"
    ]

    print(
        daily_activity.head()
    )

    # -----------------------------------------------
    # Top Products
    # -----------------------------------------------
    section("Top Products")

    top_products = (
        events["itemid"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    top_products.columns = [
        "product_id",
        "events"
    ]

    print(top_products)

    # -----------------------------------------------
    # Top Customers
    # -----------------------------------------------
    section("Top Customers")

    top_customers = (
        events["visitorid"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    top_customers.columns = [
        "customer_id",
        "events"
    ]

    print(top_customers)

    # -----------------------------------------------
    # Save Reports
    # -----------------------------------------------
    section("Saving Reports")

    daily_activity.to_csv(
        report_path /
        "daily_activity.csv",
        index=False
    )

    top_products.to_csv(
        report_path /
        "top_products.csv",
        index=False
    )

    top_customers.to_csv(
        report_path /
        "top_customers.csv",
        index=False
    )

    # -----------------------------------------------
    # Summary Statistics
    # -----------------------------------------------
    summary = pd.DataFrame({
        "metric": [
            "customers",
            "products",
            "transactions",
            "views",
            "cart",
            "purchases"
        ],
        "value": [
            total_customers,
            total_products,
            total_transactions,
            views,
            cart,
            purchases
        ]
    })

    summary.to_csv(
        report_path /
        "summary.csv",
        index=False
    )

    section("Analysis Completed")

    print(
        f"Reports saved to:\n{report_path}"
    )


# =====================================================
# Execute
# =====================================================
if __name__ == "__main__":
    main()