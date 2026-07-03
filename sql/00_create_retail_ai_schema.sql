-- Auto-generated SQL Server schema script.

-- Generated at: 2026-07-03T10:31:15.095114+00:00

SET NOCOUNT ON;

GO

IF OBJECT_ID('dbo.fact_sales', 'U') IS NOT NULL DROP TABLE dbo.fact_sales;
IF OBJECT_ID('dbo.fact_inventory', 'U') IS NOT NULL DROP TABLE dbo.fact_inventory;
IF OBJECT_ID('dbo.dim_product', 'U') IS NOT NULL DROP TABLE dbo.dim_product;
IF OBJECT_ID('dbo.dim_customer', 'U') IS NOT NULL DROP TABLE dbo.dim_customer;
GO


-- dim_customer

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE TABLE dbo.dim_customer (
    customer_id BIGINT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    income_group VARCHAR(20) NOT NULL,
    customer_segment VARCHAR(20) NOT NULL,
    created_at DATETIME2(0) NOT NULL CONSTRAINT df_dim_customer_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT pk_dim_customer PRIMARY KEY CLUSTERED (customer_id),
    CONSTRAINT ck_dim_customer_gender CHECK (gender IN ('Male', 'Female')),
    CONSTRAINT ck_dim_customer_income_group CHECK (income_group IN ('Low', 'Middle', 'High')),
    CONSTRAINT ck_dim_customer_segment CHECK (customer_segment IN ('Bronze', 'Silver', 'Gold', 'Platinum'))
);
GO


-- dim_product

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE TABLE dbo.dim_product (
    product_id BIGINT NOT NULL,
    brand VARCHAR(100) NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    cost_price DECIMAL(12, 2) NOT NULL,
    profit_margin DECIMAL(6, 2) NOT NULL,
    created_at DATETIME2(0) NOT NULL CONSTRAINT df_dim_product_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT pk_dim_product PRIMARY KEY CLUSTERED (product_id),
    CONSTRAINT ck_dim_product_unit_price CHECK (unit_price >= 0),
    CONSTRAINT ck_dim_product_cost_price CHECK (cost_price >= 0),
    CONSTRAINT ck_dim_product_profit_margin CHECK (profit_margin BETWEEN -100 AND 100)
);
GO

CREATE NONCLUSTERED INDEX ix_dim_product_brand
ON dbo.dim_product (brand);
GO


-- fact_inventory

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE TABLE dbo.fact_inventory (
    product_id BIGINT NOT NULL,
    warehouse_id INT NOT NULL,
    current_stock INT NOT NULL,
    safety_stock INT NOT NULL,
    reorder_point INT NOT NULL,
    lead_time INT NOT NULL,
    loaded_at DATETIME2(0) NOT NULL CONSTRAINT df_fact_inventory_loaded_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT pk_fact_inventory PRIMARY KEY CLUSTERED (product_id, warehouse_id),
    CONSTRAINT fk_fact_inventory_product FOREIGN KEY (product_id) REFERENCES dbo.dim_product(product_id),
    CONSTRAINT ck_fact_inventory_warehouse CHECK (warehouse_id BETWEEN 1 AND 9999),
    CONSTRAINT ck_fact_inventory_current_stock CHECK (current_stock >= 0),
    CONSTRAINT ck_fact_inventory_safety_stock CHECK (safety_stock >= 0),
    CONSTRAINT ck_fact_inventory_reorder_point CHECK (reorder_point >= 0),
    CONSTRAINT ck_fact_inventory_lead_time CHECK (lead_time > 0)
);
GO

CREATE NONCLUSTERED INDEX ix_fact_inventory_warehouse_id
ON dbo.fact_inventory (warehouse_id)
INCLUDE (current_stock, reorder_point, safety_stock);
GO


-- fact_sales

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE TABLE dbo.fact_sales (
    sales_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    warehouse_id INT NOT NULL,
    date_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    sales_amount DECIMAL(14, 2) NOT NULL,
    cost_amount DECIMAL(14, 2) NOT NULL,
    profit DECIMAL(14, 2) NOT NULL,
    loaded_at DATETIME2(0) NOT NULL CONSTRAINT df_fact_sales_loaded_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT pk_fact_sales PRIMARY KEY CLUSTERED (sales_id),
    CONSTRAINT fk_fact_sales_customer FOREIGN KEY (customer_id) REFERENCES dbo.dim_customer(customer_id),
    CONSTRAINT fk_fact_sales_product FOREIGN KEY (product_id) REFERENCES dbo.dim_product(product_id),
    CONSTRAINT ck_fact_sales_date_key CHECK (date_key BETWEEN 19000101 AND 20991231),
    CONSTRAINT ck_fact_sales_warehouse CHECK (warehouse_id BETWEEN 1 AND 9999),
    CONSTRAINT ck_fact_sales_quantity CHECK (quantity > 0),
    CONSTRAINT ck_fact_sales_unit_price CHECK (unit_price >= 0),
    CONSTRAINT ck_fact_sales_sales_amount CHECK (sales_amount >= 0),
    CONSTRAINT ck_fact_sales_cost_amount CHECK (cost_amount >= 0)
);
GO

CREATE NONCLUSTERED INDEX ix_fact_sales_customer_id
ON dbo.fact_sales (customer_id)
INCLUDE (date_key, sales_amount, profit);
GO

CREATE NONCLUSTERED INDEX ix_fact_sales_product_id
ON dbo.fact_sales (product_id)
INCLUDE (date_key, quantity, sales_amount);
GO

CREATE NONCLUSTERED INDEX ix_fact_sales_date_key
ON dbo.fact_sales (date_key)
INCLUDE (sales_amount, profit, quantity);
GO
