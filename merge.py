import os
import json
import re

#customize if need be
directory = "/workspaces/linear-regression" 

stage_pattern = re.compile(r"stage-\d{1,2}\.json$")

files = [
    os.path.join(directory, f)
    for f in os.listdir(directory)
    if stage_pattern.match(f)
]

#this file name should also be customized if need be
def stage_sort_key(filename):
    match = re.search(r"stage-(\d{1,2})\.json", filename)
    return int(match.group(1)) if match else 9999

files.sort(key=stage_sort_key)

merged_data = {}
merged_list = []  # for list-style merges

#works for dict or list JSON files
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

        if isinstance(data, dict):
            # Merge dict
            for key, value in data.items():
                if key not in merged_data:
                    merged_data[key] = value

        elif isinstance(data, list):
            # Merge list data but only if unique keys
            for item in data:
                if item not in merged_list:
                    merged_list.append(item)

# output based on observed dict or list structure
if merged_data:
    output = merged_data
    output_file = os.path.join(directory, "merged-stages.json")
else:
    output = merged_list
    output_file = os.path.join(directory, "merged-stages.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Merged {len(files)} stage files into {output_file}")
