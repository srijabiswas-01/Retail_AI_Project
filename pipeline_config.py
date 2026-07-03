PIPELINE_STAGES = {
    "etl": [
        "etl/create_customer_master.py",
        "etl/create_product_master.py",
        "etl/create_date_dimension.py",
        "etl/create_warehouse_dimension.py",
        "etl/create_inventory_fact.py",
        "etl/create_sales_fact.py",
    ],
    "features": [
        "src/features/create_cleaned_events.py",
        "src/features/create_customer_features.py",
        "src/features/create_product_features.py",
        "src/features/create_sales_daily.py",
    ],
    "forecasting": [
        "forecasting/create_forecasting_dataset.py",
        "forecasting/xgboost_model.py",
        "forecasting/lightgbm_model.py",
        "forecasting/prophet_model.py",
        "forecasting/lstm_model.py",
    ],
    "inventory": [
        "inventory/inventory_optimization.py",
    ],
    "recommendation": [
        "recommendation/recommendation_engine.py",
        "recommendation/collaborative_filtering.py",
    ],
    "customer": [
        "customer_analytics/rfm_analysis.py",
        "customer_analytics/customer_segmentation.py",
    ],
    "database": [
        "database/export_sql_server_scripts.py",
    ],
}


DEFAULT_STAGE_ORDER = [
    "etl",
    "features",
    "forecasting",
    "inventory",
    "recommendation",
    "customer",
    "database",
]
