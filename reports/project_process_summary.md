# Retail AI Project Process Summary

## Pipeline Order

1. Raw data
   - `data/raw/events.csv`
   - `data/raw/item_properties_part1.csv`
   - `data/raw/item_properties_part2.csv`
   - `data/raw/category_tree.csv`

2. ETL staging
   - `etl/create_customer_master.py`
   - `etl/create_product_master.py`
   - `etl/create_date_dimension.py`
   - `etl/create_warehouse_dimension.py`
   - `etl/create_inventory_fact.py`
   - `etl/create_sales_fact.py`

3. Processed features
   - `src/features/create_cleaned_events.py`
   - `src/features/create_customer_features.py`
   - `src/features/create_product_features.py`
   - `src/features/create_sales_daily.py`

4. Analytics and models
   - Forecasting: `forecasting/create_forecasting_dataset.py`, then model scripts.
   - Inventory: `inventory/inventory_optimization.py`
   - Recommendations: `recommendation/recommendation_engine.py`, then `recommendation/collaborative_filtering.py`
   - Customer analytics: `customer_analytics/rfm_analysis.py`, then `customer_analytics/customer_segmentation.py`

5. Dashboard
   - Run with: `streamlit run streamlit_app/Home.py`

## Model Outputs

- XGBoost: `models/xgboost_model.pkl`, `reports/xgboost_metrics.csv`, `reports/xgboost_feature_importance.csv`
- LightGBM: `models/lightgbm_model.pkl`, `reports/lightgbm_metrics.csv`, `reports/lightgbm_feature_importance.csv`
- Prophet: `models/prophet_model.pkl`, `forecasting/prophet_forecast.csv`, `reports/prophet_metrics.csv`
- LSTM: `models/lstm_model.keras`, `models/lstm_scaler.pkl`, `reports/lstm_metrics.csv`
- Recommendation: `models/recommendation_model.pkl`, `recommendation/top_recommendations.csv`

## Optimizations Applied

- Forecast dataset expanded from sparse product rows to a continuous daily panel for the top 250 products.
- Lag and rolling features now use prior values only, reducing target leakage.
- XGBoost and LightGBM now use chronological train/test splits instead of random splits.
- XGBoost now saves metrics for dashboard comparison.
- Prophet now forecasts total daily demand and saves holdout metrics.
- LSTM now trains on chronological daily demand instead of mixed product rows.
- Inventory demand now uses daily product demand instead of transaction-level averages.
- Customer segmentation was fixed so the VIP segment no longer captures nearly every customer.
- Streamlit CSV cache now refreshes automatically when files change.

## Current Validation Snapshot

- Forecast dataset: 27,250 rows, 250 products.
- Inventory output: 235,061 rows.
- Recommendation output: 29,970 rows.
- Customer segments: 11,719 customers across six segments.

## Notes

- The forecasting target is sparse because most products have zero demand on many days.
- LightGBM currently performs best among the tree models on the latest chronological holdout.
- Prophet and LSTM are trained on total daily demand, so their metrics are not directly comparable to product-level tree model metrics.
