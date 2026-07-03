-- Auto-generated SQL Server validation checks.

-- Generated at: 2026-07-03T10:31:15.102356+00:00

SET NOCOUNT ON;

GO

SELECT 'dim_customer' AS table_name, COUNT_BIG(*) AS row_count FROM dbo.dim_customer
UNION ALL
SELECT 'dim_product', COUNT_BIG(*) FROM dbo.dim_product
UNION ALL
SELECT 'fact_inventory', COUNT_BIG(*) FROM dbo.fact_inventory
UNION ALL
SELECT 'fact_sales', COUNT_BIG(*) FROM dbo.fact_sales;
GO

SELECT TOP (20)
    date_key,
    SUM(sales_amount) AS revenue,
    SUM(profit) AS profit,
    SUM(quantity) AS quantity
FROM dbo.fact_sales
GROUP BY date_key
ORDER BY date_key DESC;
GO

SELECT
    SUM(CASE WHEN s.customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_fk,
    SUM(CASE WHEN p.product_id IS NULL THEN 1 ELSE 0 END) AS missing_product_fk
FROM dbo.fact_sales fs
LEFT JOIN dbo.dim_customer s ON fs.customer_id = s.customer_id
LEFT JOIN dbo.dim_product p ON fs.product_id = p.product_id;
GO
