import json
import os

#find files and read
directory = "/workspaces/linear-regression" 
input_file = os.path.join(directory, "merged-stages.json")
output_file = os.path.join(directory, "merged-stages-sorted.json")

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# dict or list, works either way
if isinstance(data, dict):
    # sort dict by keys alphabetically
    sorted_data = {k: data[k] for k in sorted(data.keys(), key=str.lower)}
elif isinstance(data, list):
    # Sort list alphabetically
    sorted_data = sorted(data, key=lambda x: str(x).lower())
else:
    raise TypeError("The JSON must be a dictionary or list")

# Write sorted JSON to new file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)

print(f"sorted JSON saved to {output_file}")
