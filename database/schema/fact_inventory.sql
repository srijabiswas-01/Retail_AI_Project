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
