import kagglehub
import shutil
from pathlib import Path

# Download the latest RetailRocket dataset
source_path = Path(
    kagglehub.dataset_download(
        "retailrocket/ecommerce-dataset"
    )
)

print(f"Downloaded to: {source_path}")

# Project root folder
project_root = Path.cwd()

# Create destination folder
destination = project_root / "data" / "raw"
destination.mkdir(parents=True, exist_ok=True)

# Copy all CSV files
for file in source_path.glob("*.csv"):
    print(f"Copying: {file.name}")
    shutil.copy2(file, destination / file.name)

print("\nDataset successfully copied!")
print(f"Destination: {destination}")

print("\nFiles:")
for file in destination.glob("*.csv"):
    print(f" - {file.name}")