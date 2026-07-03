# Retail AI Intelligence Platform

An end-to-end retail analytics and machine learning project for sales intelligence, demand forecasting, inventory optimization, product recommendations, and customer segmentation.

The project includes a complete data pipeline, trained model artifacts, SQL Server schema/load scripts, generated reports, and a Streamlit dashboard.

## Project Goals

- Build a structured retail data warehouse from raw event and product data.
- Generate analytics-ready datasets for sales, customers, products, inventory, and forecasting.
- Train and compare forecasting models for retail demand planning.
- Identify inventory risk using reorder point and safety stock logic.
- Generate item-to-item recommendations from implicit user behavior.
- Segment customers using RFM analysis and clustering.
- Present insights through a multi-page Streamlit dashboard.

## Architecture

```text
Raw Data
   |
   v
ETL Staging Tables
   |
   v
Processed Feature Layer
   |
   +--> Forecasting Models
   +--> Inventory Optimization
   +--> Recommendation Engine
   +--> Customer Analytics
   |
   v
Reports + Model Artifacts
   |
   v
Streamlit Dashboard
```

Architecture diagram:

```text
architecture.png
```

## Project Structure

```text
Retail_AI_Project/
├── README.md
├── LICENSE
├── architecture.png
├── requirements.txt
├── customer_analytics/
│   ├── rfm_analysis.py
│   ├── customer_segmentation.py
│   ├── rfm_analysis.csv
│   └── customer_segments.csv
├── data/
│   ├── raw/
│   ├── staging/
│   └── processed/
├── database/
│   ├── export_sql_server_scripts.py
│   └── schema/
│       ├── dim_customer.sql
│       ├── dim_product.sql
│       ├── fact_sales.sql
│       └── fact_inventory.sql
├── etl/
├── forecasting/
│   ├── create_forecasting_dataset.py
│   ├── xgboost_model.py
│   ├── lightgbm_model.py
│   ├── prophet_model.py
│   ├── lstm_model.py
│   └── data/
├── inventory/
├── models/
│   └── model_metadata.json
├── recommendation/
├── reports/
├── sql/
├── src/
│   └── features/
└── streamlit_app/
    ├── Home.py
    ├── assets/
    ├── pages/
    └── utils/
```

## Main Features

### Executive Dashboard

- Business overview KPIs.
- Revenue, profit, activity, and purchase trends.
- Product and customer leaderboards.

### Sales Analytics

- Daily revenue trend.
- Orders and quantity trend.
- Profit analysis.
- Recent sales records.

### Demand Forecasting

- Product-level demand dataset.
- XGBoost and LightGBM forecasting models.
- Prophet and LSTM daily demand models.
- Model performance comparison.
- Feature importance visualization.

### Inventory Optimization

- Safety stock calculation.
- Reorder point calculation.
- Stockout flagging.
- Inventory status categories: `Safe`, `Low Stock`, `Critical`.

### Product Recommendations

- Item-to-item recommendation engine.
- Implicit interaction scoring from views, add-to-cart events, and transactions.
- Top recommendations by similarity score.

### Customer Analytics

- RFM scoring.
- KMeans clustering.
- Customer segment labels:
  - `VIP Customer`
  - `Loyal Customer`
  - `High Value Customer`
  - `Recent Customer`
  - `At Risk Customer`
  - `Regular Customer`

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Streamlit App

```powershell
.\.venv\Scripts\streamlit.exe run streamlit_app\Home.py
```

Open:

```text
http://localhost:8501
```

If Streamlit shows stale data after regenerating CSV files, hard refresh the browser with `Ctrl + F5`.

## Data Pipeline

Recommended integrated runner:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --skip-heavy
```

Run the full pipeline, including heavier model builds:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py
```

Available stages are defined in `pipeline_config.py`. Additional details are in `docs_pipeline.md`.

### 1. Raw Data

Raw data is stored in:

```text
data/raw/
```

Expected files:

```text
events.csv
item_properties_part1.csv
item_properties_part2.csv
category_tree.csv
```

### 2. ETL Staging

Run these scripts to create staging tables:

```powershell
.\.venv\Scripts\python.exe etl\create_customer_master.py
.\.venv\Scripts\python.exe etl\create_product_master.py
.\.venv\Scripts\python.exe etl\create_date_dimension.py
.\.venv\Scripts\python.exe etl\create_warehouse_dimension.py
.\.venv\Scripts\python.exe etl\create_inventory_fact.py
.\.venv\Scripts\python.exe etl\create_sales_fact.py
```

Outputs:

```text
data/staging/customer_master.csv
data/staging/product_master.csv
data/staging/date_dimension.csv
data/staging/warehouse_dimension.csv
data/staging/inventory_fact.csv
data/staging/sales_fact.csv
```

### 3. Feature Engineering

Run:

```powershell
.\.venv\Scripts\python.exe src\features\create_cleaned_events.py
.\.venv\Scripts\python.exe src\features\create_customer_features.py
.\.venv\Scripts\python.exe src\features\create_product_features.py
.\.venv\Scripts\python.exe src\features\create_sales_daily.py
```

Outputs:

```text
data/processed/cleaned_events.csv
data/processed/customer_features.csv
data/processed/product_features.csv
data/processed/sales_daily.csv
```

### 4. Forecasting

Create the forecasting dataset:

```powershell
.\.venv\Scripts\python.exe forecasting\create_forecasting_dataset.py
```

Train models:

```powershell
.\.venv\Scripts\python.exe forecasting\xgboost_model.py
.\.venv\Scripts\python.exe forecasting\lightgbm_model.py
.\.venv\Scripts\python.exe forecasting\prophet_model.py
.\.venv\Scripts\python.exe forecasting\lstm_model.py
```

Outputs:

```text
forecasting/data/forecast_dataset.csv
forecasting/prophet_forecast.csv
models/xgboost_model.pkl
models/lightgbm_model.pkl
models/prophet_model.pkl
models/lstm_model.keras
models/lstm_scaler.pkl
reports/xgboost_metrics.csv
reports/lightgbm_metrics.csv
reports/prophet_metrics.csv
reports/lstm_metrics.csv
```

### 5. Inventory Optimization

```powershell
.\.venv\Scripts\python.exe inventory\inventory_optimization.py
```

Output:

```text
inventory/inventory_optimization.csv
```

### 6. Recommendation Engine

Build item similarity:

```powershell
.\.venv\Scripts\python.exe recommendation\recommendation_engine.py
```

Generate recommendation table:

```powershell
.\.venv\Scripts\python.exe recommendation\collaborative_filtering.py
```

Outputs:

```text
models/recommendation_model.pkl
recommendation/item_similarity.csv
recommendation/top_recommendations.csv
```

### 7. Customer Analytics

```powershell
.\.venv\Scripts\python.exe customer_analytics\rfm_analysis.py
.\.venv\Scripts\python.exe customer_analytics\customer_segmentation.py
```

Outputs:

```text
customer_analytics/rfm_analysis.csv
customer_analytics/customer_segments.csv
```

## SQL Server Database Layer

Professional SQL Server schema files are stored in:

```text
database/schema/
```

Tables:

```text
dbo.dim_customer
dbo.dim_product
dbo.fact_sales
dbo.fact_inventory
```

The schema includes:

- Primary keys.
- Foreign keys.
- Check constraints.
- Default audit columns.
- Nonclustered indexes.

Generate SQL Server scripts:

```powershell
.\.venv\Scripts\python.exe database\export_sql_server_scripts.py --sample-inserts 5
```

Generated scripts:

```text
sql/00_create_retail_ai_schema.sql
sql/01_load_retail_ai_data.sql
sql/02_validate_retail_ai_data.sql
sql/03_sample_insert_data.sql
```

Run order in SQL Server:

```text
1. 00_create_retail_ai_schema.sql
2. 01_load_retail_ai_data.sql
3. 02_validate_retail_ai_data.sql
```

Important: `01_load_retail_ai_data.sql` uses `BULK INSERT`. The CSV paths must be readable by the SQL Server service account.

## Model Metadata

Model metadata is stored in:

```text
models/model_metadata.json
```

It documents:

- Model purpose.
- Model artifact path.
- Training dataset.
- Target variable.
- Metric file path.
- Current metric values where available.

## Current Validation Snapshot

Latest generated outputs:

```text
forecast_dataset.csv        27,250 rows
inventory_optimization.csv  235,061 rows
top_recommendations.csv     29,970 rows
customer_segments.csv       11,719 rows
```

Current model metrics:

```text
XGBoost   MAE 0.410   RMSE 0.905   R2 -0.148
LightGBM  MAE 0.340   RMSE 0.828   R2  0.038
Prophet   MAE 106.4   RMSE 146.4   R2 -0.435
LSTM      MAE 98.4    RMSE 129.3   R2 -0.085
```

Note: XGBoost and LightGBM predict product-level quantity. Prophet and LSTM predict total daily demand, so their metrics should not be compared directly with the tree models.

## Reports

Important report outputs:

```text
reports/summary.csv
reports/daily_activity.csv
reports/top_products.csv
reports/top_customers.csv
reports/xgboost_feature_importance.csv
reports/lightgbm_feature_importance.csv
reports/project_process_summary.md
```

## Troubleshooting

### Streamlit shows old data

Restart Streamlit and hard refresh the browser:

```powershell
.\.venv\Scripts\streamlit.exe run streamlit_app\Home.py
```

Then press `Ctrl + F5`.

### SQL Server cannot load CSV files

Check that:

- The CSV path in `sql/01_load_retail_ai_data.sql` exists.
- SQL Server service account has permission to read the folder.
- If SQL Server is remote, the CSV files are copied to that server.

### Customer Analytics shows only VIP customers

Regenerate customer analytics:

```powershell
.\.venv\Scripts\python.exe customer_analytics\rfm_analysis.py
.\.venv\Scripts\python.exe customer_analytics\customer_segmentation.py
```

Then refresh Streamlit.

### Forecasting charts look messy

Use the generated daily aggregation in the Streamlit page. Product-level forecast data contains multiple products per date, so charting raw rows directly can create crossed lines.

## License

This project is released under the MIT License. See `LICENSE`.
