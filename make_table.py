import json
import pandas as pd

# Load JSON data
with open('extracted_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract entries matching the conditions
indicator = "PCPI_IX"
frequency = "M"
target_data = None
for entry in data[0]:
    if entry.get("@FREQ") == frequency and entry.get("@INDICATOR") == indicator:
        target_data = entry["Obs"]
        break

# Convert to DataFrame
if target_data:
    df = pd.DataFrame([
        {"Date": obs["@TIME_PERIOD"], "Value": float(obs["@OBS_VALUE"])}
        for obs in target_data
    ])
    print(df)
else:
    print("No matching data found.")
