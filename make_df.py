import json
import pandas as pd

# Load JSON data
with open('extracted_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define multiple indicators and frequency
indicators = ["NC_R_XDC", "NI_R_XDC", "NFI_R_XDC", "NNXGS_R_XDC"]
frequency = "A"

# Flatten all entries into one list
all_entries = []
for block in data:
    if isinstance(block, list):
        all_entries.extend(block)
    else:
        all_entries.append(block)

# Initialize dictionary to store time series
series_dict = {}

# Iterate and collect matching series
for entry in all_entries:
    #print(entry.get("@INDICATOR"), entry.get("@FREQ"))  # Optional: for debugging
    if entry.get("@FREQ") == frequency and entry.get("@INDICATOR") in indicators:
        indicator = entry["@INDICATOR"]
        obs_list = entry.get("Obs", [])
        series_dict[indicator] = {obs["@TIME_PERIOD"]: float(obs["@OBS_VALUE"]) for obs in obs_list}

# Create DataFrame
if series_dict:
    df = pd.DataFrame(series_dict)
    df.index.name = "Date"
    df = df.sort_index().reset_index()
    print(df)
else:
    print("No matching data found.")
