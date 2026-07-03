# SQL Server Export Scripts

Run these scripts in SQL Server Management Studio or Azure Data Studio in this order:

1. `00_create_retail_ai_schema.sql`
2. `01_load_retail_ai_data.sql`
3. `02_validate_retail_ai_data.sql`

Optional:

- `03_sample_insert_data.sql` inserts a few sample rows per table for smoke testing.

## Important Notes

- `01_load_retail_ai_data.sql` uses `BULK INSERT`.
- The CSV paths in that script must be readable by the SQL Server service account.
- If SQL Server runs on another machine, copy the CSV files there or update the paths in the load script.
- The load script imports into staging tables first, then inserts into the final constrained tables.

## Regenerate Scripts

From the project root:

```powershell
.\.venv\Scripts\python.exe database\export_sql_server_scripts.py --sample-inserts 5
```
