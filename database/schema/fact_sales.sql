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
