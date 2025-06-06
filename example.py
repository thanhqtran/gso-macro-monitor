import pandas as pd 
import requests
from bs4 import BeautifulSoup
import xmltodict, json
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import textwrap

## -------------------------------- ##
## ======= some functions
## -------------------------------- ##
## parse data from xml to python dictionary
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    data = xmltodict.parse(str(soup))
    return data

# get data from 'Obs'
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

# get the metadata
def get_meta_data(dataframe):
    meta_data = {}
    meta_data['REF_AREA'] = dataframe['@REF_AREA']
    meta_data['INDICATOR'] = dataframe['@INDICATOR']
    meta_data['FREQ'] = dataframe['@FREQ']
    meta_data['DATA_DOMAIN'] = dataframe['@DATA_DOMAIN']
    return meta_data

## -------------------------------- ##
## ======= example
## -------------------------------- ##

## -------------------------------- ##
# 1. read database
database_csv = pd.read_csv('https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/refs/heads/main/dsbb_indicator_desc.csv')
database_df = pd.DataFrame(database_csv)
# return unique database and database_link pair
database_df = database_df.drop_duplicates(subset=['database', 'database_link_archive']).reset_index(drop=True)

## EXAMPLE
## extract data from the first database
i = 0
url = database_df['database_link_archive'][i]

# get data from the xml format
ex_parsed_url = get_data(url)
# get raw data of all variables in this database
ex_raw_data = ex_parsed_url['message:StructureSpecificData']['message:DataSet']['Series']

## -------------------------------- ##
# 2. choose the indicator
# example: choose the first element (first indicator) in this database
j = 1 

# the data is stored in a list of dictionaries
ex_var = ex_raw_data[j]
# time-value data are stored in the 'Obs' key
ex_var_obs = get_obs_data(ex_var)
ex_var_meta = get_meta_data(ex_var)
# convert to pandas dataframe
ex_var_df = pd.DataFrame(ex_var_obs).T
ex_var_df.columns = ['TIME_PERIOD','OBS_VALUE']
# add metadata to the dataframe
ex_var_df['INDICATOR'] = ex_var_meta['INDICATOR']
ex_var_df['FREQ'] = ex_var_meta['FREQ']
ex_var_df['DATA_DOMAIN'] = ex_var_meta['DATA_DOMAIN']
ex_var_df['REF_AREA'] = ex_var_meta['REF_AREA']
ex_var_df['BASE_PER'] = ex_var_meta['BASE_PER']

# save as csv, set the file name to the indicator name
# ex_var_df.to_csv('data/'+ex_var_meta['DATA_DOMAIN']+'_'+ex_var_meta['INDICATOR']+'_'+ex_var_meta['FREQ']+'.csv')