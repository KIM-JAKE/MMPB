# import json
# import os

# # Paths to the JSON files
# json_paths = [
#     "/workspace/MMPB/human/descriptions_simple.json",
#     "/workspace/MMPB/character/descriptions_simple.json",
#     "/workspace/MMPB/animal/descriptions_simple.json"
#     "/workspace/MMPB/object/descriptions_simple.json"
# ]

# # Output file path
# output_path = "/workspace/MMPB/formatted_descriptions_simple.json"

# # List to store merged data
# merged_data = []

# # Read and merge JSON files
# for path in json_paths:
#     if os.path.exists(path):  # Ensure file exists
#         with open(path, "r", encoding="utf-8") as f:
#             try:
#                 data = json.load(f)
#                 if isinstance(data, list):
#                     merged_data.extend(data)  # If list, extend
#                 elif isinstance(data, dict):
#                     merged_data.append(data)  # If dict, append as an item
#             except json.JSONDecodeError as e:
#                 print(f"Error reading {path}: {e}")

# # Write merged data to a new JSON file
# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump(merged_data, f, ensure_ascii=False, indent=4)

# print(f"Merged JSON saved to {output_path}")

import json
import os

# Input file paths
json_files = {
    "simple": "/workspace/MMPB/formatted_descriptions_simple.json",
    "moderate": "/workspace/MMPB/formatted_descriptions_moderate.json",
    "detailed": "/workspace/MMPB/formatted_descriptions_detailed.json"
}

# Output file path
output_path = "/workspace/MMPB/formatted_descriptions_full.json"

# Dictionary to store merged content
merged_data = {}

# Read and merge JSON files
for category, path in json_files.items():
    if os.path.exists(path):  # Ensure file exists
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    merged_data[category] = data  # Store under category
                else:
                    print(f"Warning: {path} does not contain a list.")
            except json.JSONDecodeError as e:
                print(f"Error reading {path}: {e}")

# Write merged data to a new JSON file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print(f"Merged JSON saved to {output_path}")

