import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import json
import urllib.request
import os
# database 
url = 'https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/gso_database.json'
response = urllib.request.urlopen(url)
# convert database to python dict 
database = json.loads(response.read().decode("utf-8"))
# extract csv link to the data 
db = pd.DataFrame(database)
na_database = db.iloc[1][0]
# extract csv link to the data
# na_database hierarchy
parent = 'National Accounts and State budget'
query = 'Gross domestic product at current prices by economic sector by Year Items and Economic sector'
# use get method twice to extract desired variable
query_url = na_database.get(parent, {}).get(query, {})
# plot 
## helper function to fix output folder 
def generate_output_folder() -> None:
    """
    Create the output folder if it does not already exist
    """
    if not os.path.isdir("generated"):
        os.mkdir("generated")

generate_output_folder()
# extract csv link to the data
data = pd.read_csv(query_url, skiprows=1)
df = pd.DataFrame(data)
df.replace("..", 0, inplace=True)
df['Year'] = [year for year in np.arange(1986, 2021)]
# GDP in constant price
df_gdp = df.iloc[:,[0,2,3,4,5]]
usdvnd = 23125 
df_gdp.iloc[:,1:] = df_gdp.iloc[:,1:].astype(float)/usdvnd
df_gdp.columns = ['Year', 'Agriculture', 'Industrial', 'Service', 'Tax Subsidy']
x = df_gdp['Year']
y1 = df_gdp['Agriculture']
y2 = df_gdp['Industrial']
y3 = df_gdp['Service']
y4 = df_gdp['Tax Subsidy']
fig, ax = plt.subplots(figsize=(10,7))
plt.stackplot(x, y1, y2, y3, y4, labels=['Agriculture', 'Industrial', 'Service', 'Tax Subsidy'])
plt.legend(loc='upper left')
plt.title('Gross Domestic Product')
plt.xlabel('Year')
plt.ylabel('Billion USD (2020)')
plt.ticklabel_format(style='plain', axis='y')
output = plt.savefig('generated/gdp.png', bbox_inches='tight', dpi=300)
# GDP structure 
df_structure = df.iloc[:,[0,7,8,9,10]]
df_structure.iloc[:,1:] = df_structure.iloc[:,1:].astype(float)
df_structure.columns = ['Year', 'Agriculture', 'Industrial', 'Service', 'Tax Subsidy']
x = df_structure['Year']
z1 = df_structure['Agriculture']
z2 = df_structure['Industrial']
z3 = df_structure['Service']
z4 = df_structure['Tax Subsidy']
fig, ax = plt.subplots(figsize=(10,7))
plt.stackplot(x, z1, z2, z3, z4, labels=['Agriculture', 'Industrial', 'Service', 'Tax Subsidy'])
plt.legend(loc='upper left')
plt.title('GDP Structure')
plt.xlabel('Year')
plt.ylabel('Percent')
plt.ticklabel_format(style='plain', axis='y')
output = plt.savefig('generated/gdp_structure.png', dpi=300, bbox_inches='tight')