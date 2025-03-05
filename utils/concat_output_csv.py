import pandas as pd
import glob
import os

# Define the path pattern for CSV files
csv_pattern = "/workspace/VLMEvalKit/outputs/*/*_MMPB_acc.csv"

# Expected columns
expected_columns = {
    "split", "Overall", "preference", "recognition", "preference + awareness", 
    "preference + inconsistency", "preference + overconcept", "recognition + awareness", 
    "recognition + inconsistency", "recognition + overconcept", 
    "preference + awareness + entertainment", "preference + awareness + fashion", 
    "preference + awareness + lifestyle", "preference + awareness + shopping", 
    "preference + awareness + travel", "preference + inconsistency + entertainment", 
    "preference + inconsistency + fashion", "preference + inconsistency + lifestyle", 
    "preference + inconsistency + shopping", "preference + inconsistency + travel", 
    "preference + overconcept + entertainment", "preference + overconcept + fashion", 
    "preference + overconcept + lifestyle", "preference + overconcept + shopping", 
    "preference + overconcept + travel"
}

# Find all matching CSV files
csv_files = glob.glob(csv_pattern)

# List to store DataFrames
dfs = []

# Process each CSV file
for file in csv_files:
    try:
        df = pd.read_csv(file)
        # Check if all expected columns are present
        if expected_columns.issubset(df.columns):
            # Extract model name from file path
            model_name = os.path.basename(os.path.dirname(file))
            df["model"] = model_name  # Add model name column
            dfs.append(df)
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Concatenate all DataFrames
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    # Save the result to a CSV file
    combined_df.to_csv("concatenated_models.csv", index=False)
    print("Concatenated CSV saved as 'concatenated_models.csv'")
else:
    print("No valid CSV files found.")