-- Auto-generated sample INSERT script.
-- Useful for quick SQL Server smoke tests. Use 01_load_retail_ai_data.sql for full data.
-- Generated at: 2026-07-03T10:31:15.102356+00:00
SET NOCOUNT ON;
GO
-- Sample rows for dbo.dim_customer
INSERT INTO dbo.dim_customer ([customer_id], [gender], [income_group], [customer_segment]) VALUES (257597, 'Male', 'Middle', 'Gold');
INSERT INTO dbo.dim_customer ([customer_id], [gender], [income_group], [customer_segment]) VALUES (992329, 'Female', 'Low', 'Bronze');
INSERT INTO dbo.dim_customer ([customer_id], [gender], [income_group], [customer_segment]) VALUES (111016, 'Male', 'Low', 'Gold');
INSERT INTO dbo.dim_customer ([customer_id], [gender], [income_group], [customer_segment]) VALUES (483717, 'Male', 'Middle', 'Silver');
INSERT INTO dbo.dim_customer ([customer_id], [gender], [income_group], [customer_segment]) VALUES (951259, 'Male', 'Middle', 'Platinum');
GO
-- Sample rows for dbo.dim_product
INSERT INTO dbo.dim_product ([product_id], [brand], [unit_price], [cost_price], [profit_margin]) VALUES (355908, 'Nike', 2465, 1602.25, 35.0);
INSERT INTO dbo.dim_product ([product_id], [brand], [unit_price], [cost_price], [profit_margin]) VALUES (248676, 'LG', 69, 44.85, 35.0);
INSERT INTO dbo.dim_product ([product_id], [brand], [unit_price], [cost_price], [profit_margin]) VALUES (318965, 'Adidas', 1909, 1240.85, 34.99999999999999);
INSERT INTO dbo.dim_product ([product_id], [brand], [unit_price], [cost_price], [profit_margin]) VALUES (253185, 'Dell', 1112, 722.8000000000001, 34.99999999999999);
INSERT INTO dbo.dim_product ([product_id], [brand], [unit_price], [cost_price], [profit_margin]) VALUES (367447, 'Nike', 3003, 1951.95, 35.0);
GO
-- Sample rows for dbo.fact_inventory
INSERT INTO dbo.fact_inventory ([product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time]) VALUES (355908, 5, 742, 46, 156, 7);
INSERT INTO dbo.fact_inventory ([product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time]) VALUES (248676, 2, 47, 44, 93, 6);
INSERT INTO dbo.fact_inventory ([product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time]) VALUES (318965, 3, 479, 22, 197, 4);
INSERT INTO dbo.fact_inventory ([product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time]) VALUES (253185, 4, 501, 25, 24, 2);
INSERT INTO dbo.fact_inventory ([product_id], [warehouse_id], [current_stock], [safety_stock], [reorder_point], [lead_time]) VALUES (367447, 3, 628, 49, 134, 6);
GO
-- Sample rows for dbo.fact_sales
INSERT INTO dbo.fact_sales ([sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit]) VALUES (1.0, 599528.0, 356475.0, 2.0, 20150602.0, 3.0, 3087.0, 9261.0, 6019.65, 3241.3500000000004);
INSERT INTO dbo.fact_sales ([sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit]) VALUES (2.0, 121688.0, 15335.0, 2.0, 20150601.0, 4.0, 3179.0, 12716.0, 8265.4, 4450.6);
INSERT INTO dbo.fact_sales ([sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit]) VALUES (3.0, 552148.0, 81345.0, 2.0, 20150601.0, 1.0, 3214.0, 3214.0, 2089.1, 1124.9);
INSERT INTO dbo.fact_sales ([sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit]) VALUES (4.0, 102019.0, 150318.0, 4.0, 20150601.0, 3.0, 3284.0, 9852.0, 6403.799999999999, 3448.2000000000007);
INSERT INTO dbo.fact_sales ([sales_id], [customer_id], [product_id], [warehouse_id], [date_key], [quantity], [unit_price], [sales_amount], [cost_amount], [profit]) VALUES (5.0, 189384.0, 310791.0, 1.0, 20150601.0, 3.0, 960.0, 2880.0, 1872.0, 1008.0);
GO
