from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
STAGING_DATA_DIR = DATA_DIR / "staging"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"
SQL_DIR = PROJECT_ROOT / "sql"
DATABASE_DIR = PROJECT_ROOT / "database"

FORECASTING_DIR = PROJECT_ROOT / "forecasting"
FORECASTING_DATA_DIR = FORECASTING_DIR / "data"
INVENTORY_DIR = PROJECT_ROOT / "inventory"
RECOMMENDATION_DIR = PROJECT_ROOT / "recommendation"
CUSTOMER_ANALYTICS_DIR = PROJECT_ROOT / "customer_analytics"
STREAMLIT_APP_DIR = PROJECT_ROOT / "streamlit_app"


def ensure_project_directories() -> None:
    for path in [
        RAW_DATA_DIR,
        STAGING_DATA_DIR,
        PROCESSED_DATA_DIR,
        REPORTS_DIR,
        MODELS_DIR,
        SQL_DIR,
        FORECASTING_DATA_DIR,
        INVENTORY_DIR,
        RECOMMENDATION_DIR,
        CUSTOMER_ANALYTICS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
