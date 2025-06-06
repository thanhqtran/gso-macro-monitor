import json
import pandas as pd

# Load JSON data
with open('extracted_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define multiple indicators and frequency
indicators = ["PCPI_IX", "PCPI_CP_01_IX", "PCPI_CP_011_IX"]  # Add more as needed
frequency = "M"

# Initialize dictionary to store all series
series_dict = {}

# Iterate through the dataset and collect matching series
for entry in data[0]:
    if entry.get("@FREQ") == frequency and entry.get("@INDICATOR") in indicators:
        indicator = entry["@INDICATOR"]
        obs_list = entry["Obs"]
        series_dict[indicator] = {obs["@TIME_PERIOD"]: float(obs["@OBS_VALUE"]) for obs in obs_list}

# Convert each series to a DataFrame and merge them on Date
df = pd.DataFrame(series_dict)
df.index.name = "Date"
df = df.sort_index()

# Reset index to get Date as a column
df = df.reset_index()

print(df)
