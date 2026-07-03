import pandas as pd

warehouse = pd.DataFrame({
    "warehouse_id":[1,2,3,4,5],
    "warehouse_name":[
        "North Hub",
        "South Hub",
        "East Hub",
        "West Hub",
        "Central Hub"
    ],
    "city":[
        "Delhi",
        "Mumbai",
        "Kolkata",
        "Bangalore",
        "Hyderabad"
    ],
    "capacity":[
        100000,
        80000,
        90000,
        110000,
        95000
    ]
})

warehouse.to_csv(
    "data/staging/warehouse_dimension.csv",
    index=False
)

print(warehouse)