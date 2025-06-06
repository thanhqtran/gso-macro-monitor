import pandas as pd 
import requests
from bs4 import BeautifulSoup
import xmltodict, json
import textwrap

# read database
database_csv = pd.read_csv('https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/refs/heads/main/dsbb_database.csv')
database_df = pd.DataFrame(database_csv)

# parse data from xml to python dictionary
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    data = xmltodict.parse(str(soup))
    return data


# extract data
extracted_database = []

for i in range(len(database_df)):
    database = database_df['database'][i]
    url_primary = database_df['database_link'][i]
    url_backup = database_df['database_link_archive'][i]
    
    print(f"Scraping: {database}")
    
    # Try primary link
    try:
        data = get_data(url_primary)
        database_raw = data['message:StructureSpecificData']['message:DataSet']['Series']
        extracted_database.append(database_raw)
        print(f"Success with primary link: {url_primary}")
        continue  # go to next database if success
    except Exception as e:
        print(f"Primary link failed for {database}: {e}")
    
    # Try archive link if primary fails
    try:
        print(f"Trying archive link: {url_backup}")
        data = get_data(url_backup)
        database_raw = data['message:StructureSpecificData']['message:DataSet']['Series']
        extracted_database.append(database_raw)
        print(f"Success (archive): {url_backup}")
    except Exception as e:
        print(f"Failed to scrape {database} from archive link: {e}")



# save extracted data to json
with open('extracted_database.json', 'w') as f:
    json.dump(extracted_database, f)
