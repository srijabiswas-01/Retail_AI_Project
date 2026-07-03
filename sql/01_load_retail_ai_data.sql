-- Auto-generated SQL Server bulk load script.

-- Run this after 00_create_retail_ai_schema.sql.

-- The CSV paths must be readable by the SQL Server service account.

-- Generated at: 2026-07-03T10:31:15.102356+00:00

SET NOCOUNT ON;

GO

DELETE FROM dbo.fact_sales;

DELETE FROM dbo.fact_inventory;

DELETE FROM dbo.dim_product;

DELETE FROM dbo.dim_customer;

DROP TABLE IF EXISTS dbo.stg_fact_sales;

DROP TABLE IF EXISTS dbo.stg_fact_inventory;

DROP TABLE IF EXISTS dbo.stg_dim_product;

DROP TABLE IF EXISTS dbo.stg_dim_customer;

GO

DROP TABLE IF EXISTS dbo.stg_dim_customer;

CREATE TABLE dbo.stg_dim_customer (
    customer_id BIGINT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    income_group VARCHAR(20) NOT NULL,
    customer_segment VARCHAR(20) NOT NULL
);

PRINT 'Loading dbo.dim_customer';
BULK INSERT dbo.stg_dim_customer
FROM 'D:\SB\SB\Retail_AI_Project\data\staging\customer_master.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    CODEPAGE = '65001'
);

INSERT INTO dbo.dim_customer ([customer_id], [gender], [income_group], [customer_segment])
SELECT [customer_id], [gender], [income_group], [customer_segment]
FROM dbo.stg_dim_customer;

PRINT CONCAT('Rows loaded into dbo.dim_customer: ', @@ROWCOUNT);

DROP TABLE dbo.stg_dim_customer;

GO

DROP TABLE IF EXISTS dbo.stg_dim_product;

CREATE TABLE dbo.stg_dim_product (
    product_id BIGINT NOT NULL,
    brand VARCHAR(100) NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    cost_price DECIMAL(12, 2) NOT NULL,
    profit_margin DECIMAL(6, 2) NOT NULL
);

PRINT 'Loading dbo.dim_product';
BULK INSERT dbo.stg_dim_product
FROM 'D:\SB\SB\Retail_AI_Project\data\staging\product_master.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    CODEPAGE = '65001'
);

INSERT INTO dbo.dim_product ([product_id], [brand], [unit_price], [cost_price], [profit_margin])
SELECT [product_id], [brand], [unit_price], [cost_price], [profit_margin]
FROM dbo.stg_dim_product;

PRINT CONCAT('Rows loaded into dbo.dim_product: ', @@ROWCOUNT);

DROP TABLE dbo.stg_dim_product;

GO

DROP TABLE IF EXISTS dbo.stg_fact_inventory;

CREATE TABLE dbo.stg_fact_inventory (
    product_id BIGINT NOT NULL,
    warehouse_id INT NOT NULL,
    current_stock INT NOT NULL,
    safety_stock INT NOT NULL,
    reorder_point INT NOT NULL,
    lead_time INT NOT NULL
);

PRINT 'Loading dbo.fact_inventory';
BULK INSERT dbo.stg_fact_inventory
FROM 'D:\SB\SB\Retail_AI_Project\data\staging\inventory_fact.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    CODEPAGE = '65001'
);

INSERT INTO dbo.fact_inventory ([product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time])
SELECT [product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time]
FROM dbo.stg_fact_inventory;

PRINT CONCAT('Rows loaded into dbo.fact_inventory: ', @@ROWCOUNT);

DROP TABLE dbo.stg_fact_inventory;

GO

DROP TABLE IF EXISTS dbo.stg_fact_sales;

CREATE TABLE dbo.stg_fact_sales (
    sales_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    warehouse_id INT NOT NULL,
    date_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    sales_amount DECIMAL(14, 2) NOT NULL,
    cost_amount DECIMAL(14, 2) NOT NULL,
    profit DECIMAL(14, 2) NOT NULL
);

PRINT 'Loading dbo.fact_sales';
BULK INSERT dbo.stg_fact_sales
FROM 'D:\SB\SB\Retail_AI_Project\data\staging\sales_fact.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    CODEPAGE = '65001'
);

INSERT INTO dbo.fact_sales ([sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit])
SELECT [sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit]
FROM dbo.stg_fact_sales;

PRINT CONCAT('Rows loaded into dbo.fact_sales: ', @@ROWCOUNT);

DROP TABLE dbo.stg_fact_sales;

GO
