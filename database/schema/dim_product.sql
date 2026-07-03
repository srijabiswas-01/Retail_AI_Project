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
