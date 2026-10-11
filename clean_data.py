import pandas as pd
import numpy as np

# 1. Load the raw dataset
file_path = "Copy of #Opportunity Data.xlsx.xlsx"  # Ensure this matches your file name exactly
xls = pd.ExcelFile(file_path)
print("Available sheets:", xls.sheet_names)

# Read the first sheet
df = pd.read_excel(file_path, sheet_name=0)
print(f"Original dataset shape: {df.shape}")

# 2. Drop redundant/constant columns
# 'pk' contains only 'Opportunity#' across all rows, offering no analytical value
if 'pk' in df.columns:
    df = df.drop(columns=['pk'])
    print("Dropped column: pk")

# 3. Drop rows missing critical identifiers
# If an opportunity is missing its unique ID or name, it cannot be effectively visualized
initial_row_count = len(df)
df = df.dropna(subset=['opportunity_id', 'name'])
print(f"Removed {initial_row_count - len(df)} rows missing critical identifiers.")

# 4. Transform epoch millisecond timestamps into proper datetime format
epoch_cols = ['created_at', 'last_date_to_apply', 'modified_at']
for col in epoch_cols:
    if col in df.columns:
        numeric_epoch = pd.to_numeric(df[col], errors='coerce')
        df[col] = pd.to_datetime(numeric_epoch, unit='ms', errors='coerce')
        print(f"Converted timestamp column '{col}' to datetime.")

# 5. Fix numeric data types
if 'fee' in df.columns:
    df['fee'] = pd.to_numeric(df['fee'], errors='coerce')
    print("Converted 'fee' to numeric.")

if 'duration' in df.columns:
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    print("Converted 'duration' to numeric.")

# 6. Handle missing values for boolean/flags
if 'is_archived' in df.columns:
    df['is_archived'] = df['is_archived'].fillna(False)
    print("Handled missing values in 'is_archived'.")

# 7. Summary of final cleaned dataset
print("\n--- Cleaning Complete ---")
print(f"Final cleaned dataset shape: {df.shape}")
print(df.info())

# 8. Export the cleaned dataset for Power BI
output_filename = "Cleaned_Opportunity_Dataset.xlsx"
df.to_excel(output_filename, index=False)
print(f"\nSuccess! Cleaned dataset saved as '{output_filename}' ready for Power BI import.")