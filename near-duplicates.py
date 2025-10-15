import json
import re
from rapidfuzz import fuzz

# settings
json_path = "merged-stages-sorted.json"  # your source JSON
output_path = "duplicate_groups.json"       # output file for groups
similarity_threshold = 85                   # Percentile similarity
min_group_size = 2                          # only output groups with >= this many entries

 
def normalize_text(text):
    """Normalize Latin flashcard strings for fuzzy comparison.
    
    Args: 
        text (str): input string
    Returns: 
        normalized string"""
    text = text.lower().strip()
    # Remove punctuation and brackets and separators
    text = re.sub(r"[\(\)\[\]\{\},;:/\\\-]", " ", text)
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    return text.strip()

def get_strings_from_json(data):
    """Extract all text strings from arbitrary JSON structure
    
    Args:
        data (dict or list): JSON data loaded as Python dict or list
    Returns:
        list of strings found in the JSON"""
    strings = []
    if isinstance(data, dict):
        for key, val in data.items():
            strings.append(str(key))
            #for nested strings
            if isinstance(val, str):
                strings.append(val)
            elif isinstance(val, dict): # for nested dicts
                strings += [str(v) for v in val.values() if isinstance(v, str)]
            elif isinstance(val, list): # for lists
                strings += [str(v) for v in val if isinstance(v, str)]
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                strings.append(item)
            elif isinstance(item, dict):
                strings += [str(v) for v in item.values() if isinstance(v, str)]
    return list(set(strings))  # remove exact duplicates


# Load source JSON 
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

strings = get_strings_from_json(data)
normalized = {s: normalize_text(s) for s in strings}

# Build similarity groups
groups = []
visited = set()

for i, s1 in enumerate(strings):
    if s1 in visited:
        continue

    group = [s1]
    visited.add(s1)
    n1 = normalized[s1]

    for j in range(i + 1, len(strings)):
        s2 = strings[j]
        if s2 in visited:
            continue
        
        #finding documentation on this did not have to be as hard as it was lol
        sim = fuzz.ratio(n1, normalized[s2])
        if sim >= similarity_threshold:
            group.append(s2)
            visited.add(s2)

    if len(group) >= min_group_size:
        groups.append(group)



# summary
print(f"\nFound {len(groups)} near-duplicate groups (threshold {similarity_threshold}%)\n")
for idx, group in enumerate(groups, 1):
    print(f"Group {idx} ({len(group)} items):")
    for item in group:
        print("  -", item)
    print()

# rite to json
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)

print(f"Groups saved to {output_path}")
