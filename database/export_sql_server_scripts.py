import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql"
SCHEMA_DIR = PROJECT_ROOT / "database" / "schema"

TABLES = [
    {
        "name": "dim_customer",
        "csv": PROJECT_ROOT / "data" / "staging" / "customer_master.csv",
        "schema": SCHEMA_DIR / "dim_customer.sql",
        "load_order": 1,
        "columns": ["customer_id", "gender", "income_group", "customer_segment"],
        "stage_columns": [
            "customer_id BIGINT NOT NULL",
            "gender VARCHAR(20) NOT NULL",
            "income_group VARCHAR(20) NOT NULL",
            "customer_segment VARCHAR(20) NOT NULL",
        ],
    },
    {
        "name": "dim_product",
        "csv": PROJECT_ROOT / "data" / "staging" / "product_master.csv",
        "schema": SCHEMA_DIR / "dim_product.sql",
        "load_order": 2,
        "columns": ["product_id", "brand", "unit_price", "cost_price", "profit_margin"],
        "stage_columns": [
            "product_id BIGINT NOT NULL",
            "brand VARCHAR(100) NOT NULL",
            "unit_price DECIMAL(12, 2) NOT NULL",
            "cost_price DECIMAL(12, 2) NOT NULL",
            "profit_margin DECIMAL(6, 2) NOT NULL",
        ],
    },
    {
        "name": "fact_inventory",
        "csv": PROJECT_ROOT / "data" / "staging" / "inventory_fact.csv",
        "schema": SCHEMA_DIR / "fact_inventory.sql",
        "load_order": 3,
        "columns": [
            "product_id",
            "warehouse_id",
            "current_stock",
            "safety_stock",
            "reorder_point",
            "lead_time",
        ],
        "stage_columns": [
            "product_id BIGINT NOT NULL",
            "warehouse_id INT NOT NULL",
            "current_stock INT NOT NULL",
            "safety_stock INT NOT NULL",
            "reorder_point INT NOT NULL",
            "lead_time INT NOT NULL",
        ],
    },
    {
        "name": "fact_sales",
        "csv": PROJECT_ROOT / "data" / "staging" / "sales_fact.csv",
        "schema": SCHEMA_DIR / "fact_sales.sql",
        "load_order": 4,
        "columns": [
            "sales_id",
            "customer_id",
            "product_id",
            "warehouse_id",
            "date_key",
            "quantity",
            "unit_price",
            "sales_amount",
            "cost_amount",
            "profit",
        ],
        "stage_columns": [
            "sales_id BIGINT NOT NULL",
            "customer_id BIGINT NOT NULL",
            "product_id BIGINT NOT NULL",
            "warehouse_id INT NOT NULL",
            "date_key INT NOT NULL",
            "quantity INT NOT NULL",
            "unit_price DECIMAL(12, 2) NOT NULL",
            "sales_amount DECIMAL(14, 2) NOT NULL",
            "cost_amount DECIMAL(14, 2) NOT NULL",
            "profit DECIMAL(14, 2) NOT NULL",
        ],
    },
]


def sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def read_schema(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def write_create_schema() -> Path:
    output = SQL_DIR / "00_create_retail_ai_schema.sql"
    drop_sql = """
IF OBJECT_ID('dbo.fact_sales', 'U') IS NOT NULL DROP TABLE dbo.fact_sales;
IF OBJECT_ID('dbo.fact_inventory', 'U') IS NOT NULL DROP TABLE dbo.fact_inventory;
IF OBJECT_ID('dbo.dim_product', 'U') IS NOT NULL DROP TABLE dbo.dim_product;
IF OBJECT_ID('dbo.dim_customer', 'U') IS NOT NULL DROP TABLE dbo.dim_customer;
GO
""".strip()

    body = [
        "-- Auto-generated SQL Server schema script.",
        f"-- Generated at: {datetime.now(timezone.utc).isoformat()}",
        "SET NOCOUNT ON;",
        "GO",
        drop_sql,
    ]

    for table in sorted(TABLES, key=lambda item: item["load_order"]):
        body.append(f"\n-- {table['name']}")
        body.append(read_schema(table["schema"]))

    output.write_text("\n\n".join(body) + "\n", encoding="utf-8")
    return output


def bulk_insert_statement(table: dict) -> str:
    stage_name = f"stg_{table['name']}"
    stage_columns = ",\n    ".join(table["stage_columns"])
    column_list = ", ".join(f"[{column}]" for column in table["columns"])

    return f"""
DROP TABLE IF EXISTS dbo.{stage_name};

CREATE TABLE dbo.{stage_name} (
    {stage_columns}
);

PRINT 'Loading dbo.{table["name"]}';
BULK INSERT dbo.{stage_name}
FROM '{sql_path(table["csv"])}'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    CODEPAGE = '65001'
);

INSERT INTO dbo.{table["name"]} ({column_list})
SELECT {column_list}
FROM dbo.{stage_name};

PRINT CONCAT('Rows loaded into dbo.{table["name"]}: ', @@ROWCOUNT);

DROP TABLE dbo.{stage_name};
""".strip()


def write_load_data() -> Path:
    output = SQL_DIR / "01_load_retail_ai_data.sql"
    body = [
        "-- Auto-generated SQL Server bulk load script.",
        "-- Run this after 00_create_retail_ai_schema.sql.",
        "-- The CSV paths must be readable by the SQL Server service account.",
        f"-- Generated at: {datetime.now(timezone.utc).isoformat()}",
        "SET NOCOUNT ON;",
        "GO",
        "DELETE FROM dbo.fact_sales;",
        "DELETE FROM dbo.fact_inventory;",
        "DELETE FROM dbo.dim_product;",
        "DELETE FROM dbo.dim_customer;",
        "DROP TABLE IF EXISTS dbo.stg_fact_sales;",
        "DROP TABLE IF EXISTS dbo.stg_fact_inventory;",
        "DROP TABLE IF EXISTS dbo.stg_dim_product;",
        "DROP TABLE IF EXISTS dbo.stg_dim_customer;",
        "GO",
    ]

    for table in sorted(TABLES, key=lambda item: item["load_order"]):
        body.append(bulk_insert_statement(table))
        body.append("GO")

    output.write_text("\n\n".join(body) + "\n", encoding="utf-8")
    return output


def write_validation() -> Path:
    output = SQL_DIR / "02_validate_retail_ai_data.sql"
    body = [
        "-- Auto-generated SQL Server validation checks.",
        f"-- Generated at: {datetime.now(timezone.utc).isoformat()}",
        "SET NOCOUNT ON;",
        "GO",
        """
SELECT 'dim_customer' AS table_name, COUNT_BIG(*) AS row_count FROM dbo.dim_customer
UNION ALL
SELECT 'dim_product', COUNT_BIG(*) FROM dbo.dim_product
UNION ALL
SELECT 'fact_inventory', COUNT_BIG(*) FROM dbo.fact_inventory
UNION ALL
SELECT 'fact_sales', COUNT_BIG(*) FROM dbo.fact_sales;
GO
""".strip(),
        """
SELECT TOP (20)
    date_key,
    SUM(sales_amount) AS revenue,
    SUM(profit) AS profit,
    SUM(quantity) AS quantity
FROM dbo.fact_sales
GROUP BY date_key
ORDER BY date_key DESC;
GO
""".strip(),
        """
SELECT
    SUM(CASE WHEN s.customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_fk,
    SUM(CASE WHEN p.product_id IS NULL THEN 1 ELSE 0 END) AS missing_product_fk
FROM dbo.fact_sales fs
LEFT JOIN dbo.dim_customer s ON fs.customer_id = s.customer_id
LEFT JOIN dbo.dim_product p ON fs.product_id = p.product_id;
GO
""".strip(),
    ]

    output.write_text("\n\n".join(body) + "\n", encoding="utf-8")
    return output


def validate_csv_headers() -> None:
    for table in TABLES:
        if not table["csv"].exists():
            raise FileNotFoundError(table["csv"])

        actual_columns = pd.read_csv(table["csv"], nrows=0).columns.tolist()
        if actual_columns != table["columns"]:
            raise ValueError(
                f"{table['csv']} columns do not match dbo.{table['name']}. "
                f"Expected {table['columns']}, found {actual_columns}"
            )


def write_sample_inserts(rows_per_table: int) -> Path:
    output = SQL_DIR / "03_sample_insert_data.sql"
    chunks = [
        "-- Auto-generated sample INSERT script.",
        "-- Useful for quick SQL Server smoke tests. Use 01_load_retail_ai_data.sql for full data.",
        f"-- Generated at: {datetime.now(timezone.utc).isoformat()}",
        "SET NOCOUNT ON;",
        "GO",
    ]

    for table in sorted(TABLES, key=lambda item: item["load_order"]):
        df = pd.read_csv(table["csv"], nrows=rows_per_table)
        columns = ", ".join(f"[{col}]" for col in table["columns"])
        chunks.append(f"-- Sample rows for dbo.{table['name']}")

        for _, row in df.iterrows():
            values = []
            for col in table["columns"]:
                value = row[col]
                if pd.isna(value):
                    values.append("NULL")
                elif isinstance(value, str):
                    values.append("'" + value.replace("'", "''") + "'")
                else:
                    values.append(str(value))

            chunks.append(
                f"INSERT INTO dbo.{table['name']} ({columns}) VALUES ({', '.join(values)});"
            )
        chunks.append("GO")

    output.write_text("\n".join(chunks) + "\n", encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate SQL Server schema, data load, and validation scripts."
    )
    parser.add_argument(
        "--sample-inserts",
        type=int,
        default=5,
        help="Number of sample INSERT rows per table to export into sql/03_sample_insert_data.sql.",
    )
    args = parser.parse_args()

    SQL_DIR.mkdir(parents=True, exist_ok=True)
    validate_csv_headers()

    outputs = [
        write_create_schema(),
        write_load_data(),
        write_validation(),
    ]

    if args.sample_inserts > 0:
        outputs.append(write_sample_inserts(args.sample_inserts))

    print("Generated SQL Server scripts:")
    for output in outputs:
        print(f"- {output.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
