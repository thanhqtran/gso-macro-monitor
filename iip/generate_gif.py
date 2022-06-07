import pandas as pd 
import requests
from bs4 import BeautifulSoup
import xmltodict, json
import matplotlib.pyplot as plt
import os
import numpy as np
import imageio
# extract .xml data from gso and convert to python dictionary 
url = 'http://nsdp.gso.gov.vn/GSO-chung/SDMXFiles/GSO/GSO.%20Chi%20so%20cong%20nghiep.IIP_Vietnam.xml'
# read xml file from url 
r = requests.get(url)
soup = BeautifulSoup(r.text, 'xml')
# convert xml to python dict
data = xmltodict.parse(str(soup))
# data structure 
structure = {0: {'AIP_ISIC4_IX':'Industry (2015=100)'}, 1:{'AIP_ISIC4_B_IX':'Mining and Quarying (2015=100)'}, 2:{'AIP_ISIC4_C_IX':'Manufacturing (2015=100)'}, 3:{'AIP_ISIC4_D_IX':'Electricity, Gas (2015=100)'}, 4:{'AIP_ISIC4_E_IX':'Water Supply: Sewerage, Waste Mgt/Remediation Activities(2015=100)'}}
data_series = data['message:StructureSpecificData']['message:DataSet']['Series']
df_industry = data_series[0]
df_mining = data_series[1]
df_manufacturing = data_series[2]
df_electricity = data_series[3]
df_water = data_series[4]
# a function to extract industry-specific data 
def get_industry_data(dataframe):
   x_dict = []
   y_dict = []
   for i in range(0,len(dataframe['Obs'])):
      x = dataframe['Obs'][i]['@TIME_PERIOD'] 
      y = dataframe['Obs'][i]['@OBS_VALUE']
      x = pd.to_datetime(x).strftime('%Y-%m') #convert x to datetime
      x_dict.append(x)
      y_dict.append(float(y)) #convert y to float
   return x_dict, y_dict

# ======== gif for iip ======================

# helper function to create folder
def generate_output_folder() -> None:
    """
    Create the output folder if it does not already exist
    """
    if not os.path.isdir("generated"):
        os.mkdir("generated")

generate_output_folder()

# generate gif 
filenames = []
x = get_industry_data(df_industry)[0]

for i in range(0, len(x)):
    fig, ax = plt.subplots(figsize=(10,7))
    fontsize = 14
    # plot data
    plt.bar(get_industry_data(df_industry)[0][:i], get_industry_data(df_industry)[1][:i], color='#ff7f0e', width=0.5, label='All Industry', alpha=0.2)
    #plt.plot(get_industry_data(df_industry)[0][:i], get_industry_data(df_industry)[1][:i], label='All Industry', ls='-', marker='o', color='blue')
    plt.plot(get_industry_data(df_manufacturing)[0][:i], get_industry_data(df_manufacturing)[1][:i], label='Manufacturing')
    plt.plot(get_industry_data(df_electricity)[0][:i], get_industry_data(df_electricity)[1][:i], label='Electricity, Gas')
    plt.plot(get_industry_data(df_water)[0][:i], get_industry_data(df_water)[1][:i], label='Water/Sewage')
    plt.plot(get_industry_data(df_mining)[0][:i], get_industry_data(df_mining)[1][:i], label='Mining and Quarying')
    #legend outside 
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fontsize=fontsize)
    #set x-ticks every 3 months 
    ax.xaxis.set_major_locator(plt.MultipleLocator(4))
    plt.xlabel('Month', fontsize=fontsize)
    plt.xticks(rotation=60, fontsize=10)
    plt.ylabel('Index, 2015=100', fontsize=fontsize)
    plt.title('Vietnam Industrial Production Index (monthly)', fontsize=16)
    
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
# build gif

gif_filename = 'generated/iip.gif'
images = []

for filename in filenames:
    images.append(imageio.imread(filename))
duration = 0.15
imageio.mimsave(gif_filename, images, duration=duration, loop=1)
       
# Remove files
for filename in set(filenames):
    os.remove(filename)