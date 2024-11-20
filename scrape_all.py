import pandas as pd 
import requests
from bs4 import BeautifulSoup
import xmltodict, json
import textwrap

# read database
database_csv = pd.read_csv('https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/refs/heads/main/dsbb_indicator_desc.csv')
database_df = pd.DataFrame(database_csv)

# parse data from xml to python dictionary
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    data = xmltodict.parse(str(soup))
    return data

def get_obs_data(dataframe):
    x_dict = []
    y_dict = []
    for i in range(0,len(dataframe['Obs'])):
        x = dataframe['Obs'][i]['@TIME_PERIOD'] 
        y = dataframe['Obs'][i]['@OBS_VALUE']
        x = pd.to_datetime(x) #convert x to datetime
        try:
            y = float(y)
        except:
            y = np.nan
        x_dict.append(x)
        y_dict.append(y)
    return x_dict, y_dict

def get_meta_data(dataframe):
    meta_data = {}
    meta_data['REF_AREA'] = dataframe['@REF_AREA']
    meta_data['INDICATOR'] = dataframe['@INDICATOR']
    meta_data['FREQ'] = dataframe['@FREQ']
    meta_data['DATA_DOMAIN'] = dataframe['@DATA_DOMAIN']
    return meta_data

# return unique database and database_link pair
database_df = database_df.drop_duplicates(subset=['database', 'database_link', 'database_link_archive']).reset_index(drop=True)

# extract data from database_link_archive
extracted_database = []

# archived
for i in range(0, len(database_df)):
    database = database_df['database'][i]
    url = database_df['database_link_archive'][i]
    data = get_data(url)
    database_raw = data['message:StructureSpecificData']['message:DataSet']['Series']
    extracted_database.append(database_raw)

# save extracted data to json
with open('extracted_database.json', 'w') as f:
    json.dump(extracted_database, f)
