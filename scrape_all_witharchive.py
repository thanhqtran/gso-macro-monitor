import pandas as pd
import requests
from bs4 import BeautifulSoup
import xmltodict, json
import numpy as np

# Load database list
database_csv = pd.read_csv('https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/refs/heads/main/dsbb_indicator_desc.csv')
database_df = pd.DataFrame(database_csv)
database_df = database_df.drop_duplicates(subset=['database', 'database_link', 'database_link_archive']).reset_index(drop=True)

# Function: fetch XML from URL
def get_data(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, 'xml')
    data = xmltodict.parse(str(soup))
    return data

# Function: fallback to Wayback Machine (get latest snapshot)
def get_latest_wayback_url(original_url):
    query_url = f'https://archive.org/wayback/available?url={original_url}'
    try:
        r = requests.get(query_url, timeout=10)
        snapshots = r.json()
        archived_snap = snapshots.get('archived_snapshots', {})
        if 'closest' in archived_snap:
            return archived_snap['closest']['url']
    except Exception as e:
        print(f"Wayback fallback failed for {original_url}: {e}")
    return None

# Function: get observations
def get_obs_data(dataframe):
    x_dict, y_dict = [], []
    for obs in dataframe.get('Obs', []):
        try:
            x = pd.to_datetime(obs['@TIME_PERIOD'])
            y = float(obs['@OBS_VALUE'])
        except:
            x, y = pd.NaT, np.nan
        x_dict.append(x)
        y_dict.append(y)
    return x_dict, y_dict

# Extract data from database_link_archive (with fallback)
extracted_database = []

for i in range(len(database_df)):
    database = database_df.loc[i, 'database']
    print(f"Scraping: {database}")
    url = database_df.loc[i, 'database_link_archive']
    original_url = database_df.loc[i, 'database_link']

    try:
        data = get_data(url)
        series = data['message:StructureSpecificData']['message:DataSet']['Series']
        extracted_database.append(series)
    except Exception as e:
        print(f"Primary archive failed: {e}")
        fallback_url = get_latest_wayback_url(original_url)
        if fallback_url:
            print(f"Trying Wayback snapshot: {fallback_url}")
            try:
                data = get_data(fallback_url)
                series = data['message:StructureSpecificData']['message:DataSet']['Series']
                extracted_database.append(series)
            except Exception as e2:
                print(f"Wayback snapshot failed: {e2}")
        else:
            print(f"No Wayback snapshot found for: {original_url}")

# Save extracted data
with open('extracted_database.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_database, f, ensure_ascii=False, indent=2)
