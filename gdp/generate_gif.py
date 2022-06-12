import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import json
import urllib.request
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio

# database 
url = 'https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/gso_database.json'
response = urllib.request.urlopen(url)
# convert database to python dict 
database = json.loads(response.read().decode("utf-8"))
db = pd.DataFrame(database)
# extract csv link to the data 
na_database = db.iloc[1][0]
# na_database hierarchy
parent = 'National Accounts and State budget'
query = 'Gross domestic product at current prices by economic sector by Year Items and Economic sector'
# use get method twice to extract desired variable
query_url = na_database.get(parent, {}).get(query, {})

# extract csv link to the data
data = pd.read_csv(query_url, skiprows=1)
df = pd.DataFrame(data)
df.replace("..", 0, inplace=True)
df['Year'] = [year for year in np.arange(1986, 2021)]
# GDP in constant price
df_gdp = df.iloc[:,[0,2,3,4,5]]
df_gdp.iloc[:,1:] = df_gdp.iloc[:,1:].astype(float)
df_gdp.columns = ['Year', 'Agriculture', 'Industrial', 'Service', 'Tax Subsidy']
x = df_gdp['Year']
y1 = df_gdp['Agriculture']
y2 = df_gdp['Industrial']
y3 = df_gdp['Service']
y4 = df_gdp['Tax Subsidy']


# ======== gif for gdp ======================
filenames = []

for i in range(0, len(x)):
    # plot the line chart
    fig, ax = plt.subplots(figsize=(8,5))
    plt.stackplot(x[:i], y1[:i], y2[:i], y3[:i], y4[:i], labels=['Agriculture', 'Industrial', 'Service', 'Tax Subsidy'])
    plt.legend(loc='upper left')
    plt.title('Gross Domestic Product for Vietnam (national currency)')
    plt.xlabel('Year')
    plt.ylabel('VND')
    plt.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
# build gif

directory = os.getcwd()
gif_filename = f'{directory}/generated_gif/gdp_na.gif'
images = []

for filename in filenames:
    images.append(imageio.imread(filename))
duration = 0.15
imageio.mimsave(gif_filename, images, duration=duration, loop=1)
       
# Remove files
for filename in set(filenames):
    os.remove(filename)

#======= gif for gdp structure ======================
#stacked area chart
df_structure = df.iloc[:,[0,7,8,9,10]]
df_structure.iloc[:,1:] = df_structure.iloc[:,1:].astype(float)
df_structure.columns = ['Year', 'Agriculture', 'Industrial', 'Service', 'Tax Subsidy']
x = df_structure['Year']
y1 = df_structure['Agriculture']
y2 = df_structure['Industrial']
y3 = df_structure['Service']
y4 = df_structure['Tax Subsidy']

filenames = []

for i in range(0, len(x)):
    # plot the line chart
    fig, ax = plt.subplots(figsize=(8,5))
    plt.stackplot(x[:i], y1[:i], y2[:i], y3[:i], y4[:i], labels=['Agriculture', 'Industrial', 'Service', 'Tax Subsidy'])
    plt.legend(loc='upper left')
    plt.title('Vietnam. Contribution to GDP by sector')
    plt.xlabel('Year')
    plt.ticklabel_format(style='plain', axis='y')
    
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
# build gif

gif_filename = f'{directory}/generated_gif/gdp_sector.gif'
images = []

for filename in filenames:
    images.append(imageio.imread(filename))
duration = 0.15
imageio.mimsave(gif_filename, images, duration=duration, loop=1)
       
# Remove files
for filename in set(filenames):
    os.remove(filename)