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
