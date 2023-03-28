import pandas as pd 
import requests
from bs4 import BeautifulSoup
import xmltodict, json
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
import textwrap

################################################################################
# Helper Functions
################################################################################

def generate_output_folder() -> None:
    """
    Create the output folder if it does not already exist
    """
    if not os.path.isdir("generated"):
        os.mkdir("generated")


def make_gif_multivar(plotname, df, shorten=True):
    """
    Create a gif from a list of dataframes
    """
    plotname = str(plotname)
    filenames = []
    labels = []
    ys = {}
    xs = {}
    x = get_obs_data(df[0])[0]
    for i in range(0, len(df)):
        label_raw = desc[desc['indicator'] ==
                         df[i]['@INDICATOR']]['desc'].values[0]
        if shorten:
            label = textwrap.fill(label_raw, 15)
        else:
            label = label_raw
        labels.append(label)
        xs[label], ys[label] = get_obs_data(df[i])
    for time in range(0, len(x)):
        fig, ax = plt.subplots(figsize=(10, 5))
        for j in range(0, len(labels)):
            plt.plot(xs[labels[j]][:time], ys[labels[j]]
                     [:time], label=labels[j])
        plt.xticks(rotation=45, size=10)
        plt.legend(bbox_to_anchor=(1.04, 0.5),
                   loc="center left", borderaxespad=0)
        plt.tight_layout()
        #create file name and add to list
        filename = f'{time}.png'
        filenames.append(filename)
        #save frames
        plt.title(plotname)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    # build gif
    gif_filename = f'{save_loc}{plotname}.gif'
    images = []
    duration = 0.15

    with imageio.get_writer(gif_filename, mode='I', duration=duration, loop=1) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove files
    for filename in set(filenames):
        os.remove(filename)

#directory 
directory = os.getcwd()
save_loc = f'{directory}/generated_gif/'

################################################################################
# Functions to get Data
################################################################################

# get indicator descriptions
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

#database with url
database = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_database.csv')).reset_index(drop=True)
#convert data values to string 
database['url'].apply(lambda x: str(x))
database['var'].apply(lambda x: str(x))

#database description
desc = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv')).reset_index(drop=True)
desc['indicator'].apply(lambda x: str(x))
desc['desc'].apply(lambda x: str(x))
desc['domain'].apply(lambda x: str(x))
# do not display output 
pd.set_option('display.max_columns', None)

# dataframes from database
df_gdp = get_data(database['url'][1])
df_cpi = get_data(database['url'][2])
df_govbudget = get_data(database['url'][3])
df_gov_debt = get_data(database['url'][4])
df_interest = get_data(database['url'][5])
df_stock = get_data(database['url'][6])
df_bop = get_data(database['url'][7])
df_extdebt = get_data(database['url'][8])
df_exr = get_data(database['url'][9])
df_iip = get_data(database['url'][10])
df_lab = get_data(database['url'][11])
df_ppi = get_data(database['url'][12])
df_pop = get_data(database['url'][13])
df_trade = get_data(database['url'][14])

################################################################################
# Individual DataFrame Processing
################################################################################


### GDP data
df_gdp1 = df_gdp['message:StructureSpecificData']['message:DataSet']['Series']
# extract data based on INDICATOR
agri_inds = ['NGDPVA_R_ISIC4_A01_XDC', 'NGDPVA_R_ISIC4_A02_XDC', 'NGDPVA_R_ISIC4_A03_XDC']
industrial_inds = ['NGDPVA_R_ISIC4_B_XDC','NGDPVA_R_ISIC4_C_XDC','NGDPVA_R_ISIC4_D_XDC','NGDPVA_R_ISIC4_E_XDC','NGDPVA_R_ISIC4_F_XDC']
service_inds = ['NGDPVA_R_ISIC4_G_XDC','NGDPVA_R_ISIC4_H_XDC','NGDPVA_R_ISIC4_I_XDC','NGDPVA_R_ISIC4_J_XDC','NGDPVA_R_ISIC4_K_XDC','NGDPVA_R_ISIC4_L_XDC','NGDPVA_R_ISIC4_M_XDC','NGDPVA_R_ISIC4_N_XDC','NGDPVA_R_ISIC4_O_XDC','NGDPVA_R_ISIC4_P_XDC','NGDPVA_R_ISIC4_Q_XDC','NGDPVA_R_ISIC4_R_XDC','NGDPVA_R_ISIC4_S_XDC']
extracted_agri = []
extracted_inds = []
extracted_serv = []
#loop through the list and extract matched indicators
for item in df_gdp1:
    if item['@INDICATOR'] in agri_inds and item['@FREQ'] == 'Q':
        extracted_agri.append(item)
    elif item['@INDICATOR'] in industrial_inds and item['@FREQ'] == 'Q':
        extracted_inds.append(item)
    elif item['@INDICATOR'] in service_inds and item['@FREQ'] == 'Q':
        extracted_serv.append(item)
    else:
        pass

# make gif based on INDICATOR
make_gif_multivar('Real GDP Agriculture', extracted_agri)
make_gif_multivar('Real GDP Construction and Industry', extracted_inds)
make_gif_multivar('Real GDP Services', extracted_serv)

### Labor data 
df_lab1 = df_lab['message:StructureSpecificData']['message:DataSet']['Series']
unempl_inds = ['LUR_PT','LUR15O_PT','LEU_PT']
empl_inds = ['LLF_PE_NUM','LE_PE_NUM']
extracted_unempl = []
extracted_empl = []
for item in df_lab1:
    if item['@INDICATOR'] in unempl_inds and item['@FREQ'] == 'Q':
        extracted_unempl.append(item)
    elif item['@INDICATOR'] in empl_inds and item['@FREQ'] == 'Q':
        extracted_empl.append(item)
    else:
        pass
make_gif_multivar('Unemployment', extracted_unempl, shorten=True)
make_gif_multivar('Employment', extracted_empl, shorten=True)

### Earnings
earning_inds = ['LME_AVG_XDC','LMEM_AVG_XDC','LMEF_AVG_XDC']
extracted_earning = []
for item in df_lab1:
    if item['@INDICATOR'] in earning_inds and item['@FREQ'] == 'Q':
        extracted_earning.append(item)
    else:
        pass
make_gif_multivar('Earnings', extracted_earning, shorten=True)

### Exchange rate data
df_exr1 = df_exr['message:StructureSpecificData']['message:DataSet']['Series']
exchange_rate = ['ENDE_MID_XDC_USD_RATE', 'ENDA_MID_XDC_USD_RATE']
extracted_exr = []
for item in df_exr1:
    if item['@INDICATOR'] in exchange_rate and item['@FREQ'] == 'M':
        extracted_exr.append(item)
    else:
        pass
make_gif_multivar('Exchange Rate', extracted_exr, shorten=True)

### BOP 
df_bop1 = df_bop['message:StructureSpecificData']['message:DataSet']['Series']
bop_inds = ['VNM_BCA_BP6_USD','VNM_BK_BP6_USD','VNM_BF_BP6_USD']
inflow_inds = ['VNM_BFDL_BP6_USD','VNM_BFPL_BP6_USD','VNM_BFOL_BP6_USD']
outflow_inds = ['VNM_BFDA_BP6_USD','VNM_BFPA_BP6_USD','VNM_BFOA_BP6_USD']
extracted_bop = []
extracted_invest = []
for item in df_bop1:
    if item['@INDICATOR'] in bop_inds and item['@FREQ'] == 'Q':
        extracted_bop.append(item)
    elif item['@INDICATOR'] in inflow_inds and item['@FREQ'] == 'Q':
        extracted_invest.append(item)
    else:
        pass
make_gif_multivar('BOP', extracted_bop, shorten=True)
make_gif_multivar('Investment', extracted_invest, shorten=True)

### Producer Price Index 
df_ppi1 = df_ppi['message:StructureSpecificData']['message:DataSet']['Series']
ppi_inds = ['PPPI_ISIC4_A_BY_PP_IX','VNM_PPPI_ISIC4_BTE_BY_PP_IX','VNM_PPPI_ISIC4_HTJ_PTR_BY_PP_IX']
extracted_ppi = []
for item in df_ppi1:
    if item['@INDICATOR'] in ppi_inds and item['@FREQ'] == 'Q':
        extracted_ppi.append(item)
    else:
        pass
make_gif_multivar('Producer Price Index', extracted_ppi, shorten=True)

### CPI 
df_cpi1 = df_cpi['message:StructureSpecificData']['message:DataSet']['Series']
cpi_comp_inds = ['PCPI_CP_01_IX','PCPI_CP_02_IX','PCPI_CP_03_IX','PCPI_CP_04_IX','PCPI_CP_05_IX','PCPI_CP_06_IX','PCPI_CP_07_IX','PCPI_CP_08_IX','PCPI_CP_10_IX','PCPI_CP_09_IX','PCPI_CP_12_IX']
cpi_agg_inds = ['PCPI_IX','PCPICO_BY_CP_A_PT']
extracted_cpi_comp = []
extracted_cpi_agg = []
for item in df_cpi1:
    if item['@INDICATOR'] in cpi_comp_inds and item['@FREQ'] == 'M':
        extracted_cpi_comp.append(item)
    elif item['@INDICATOR'] in cpi_agg_inds and item['@FREQ'] == 'M':
        extracted_cpi_agg.append(item)
    else:
        pass
make_gif_multivar('CPI Components', extracted_cpi_comp, shorten=True)

# Main CPI index
cpi_agg = df_cpi1[0]
cpi_core = df_cpi1[32]
agg_x, agg_y = get_obs_data(cpi_agg)
core_x, core_y = get_obs_data(cpi_core)
label_agg = desc[desc['indicator'] == cpi_agg['@INDICATOR']]['desc'].values[0]
label_core = desc[desc['indicator'] == cpi_core['@INDICATOR']]['desc'].values[0]
# plot
filenames = []
for i in range(0, len(agg_x)):
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(agg_x[:i], agg_y[:i], label=label_agg, color='b', marker='o')
    ax1.set_ylabel(label_agg, color='b')
    ax1.tick_params(axis='x', labelrotation=90)
    ax2 = ax1.twinx()
    ax2.plot(core_x[:i], core_y[:i], label=label_core, color='r', marker='o')
    ax2.set_ylabel(label_core, color='r')
    fig.tight_layout()
    #create file name and add to list
    filename = f'{i}.png'
    filenames.append(filename)
    #save frames
    plt.title('Vietnam CPI Index and Core CPI change yoy')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
# build gif
gif_filename = f'{save_loc}cpi.gif'
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
duration = 0.15
imageio.mimsave(gif_filename, images, duration=duration, loop=1)
# Remove files
for filename in set(filenames):
    os.remove(filename)

### Population
df_pop1 = df_pop['message:StructureSpecificData']['message:DataSet']['Series']
pop_inds = ['LPM_PE_NUM','LPF_PE_NUM']
urban_inds = ['LPU_PE_NUM','LPR_PE_NUM']
extracted_pop = []
extracted_urban = []
for item in df_pop1:
    if item['@INDICATOR'] in pop_inds and item['@FREQ'] == 'A':
        extracted_pop.append(item)
    elif item['@INDICATOR'] in urban_inds and item['@FREQ'] == 'A':
        extracted_urban.append(item)
    else:
        pass
make_gif_multivar('Population', extracted_pop, shorten=True)

### Trade 
df_trade1 = df_trade['message:StructureSpecificData']['message:DataSet']['Series']
trade_inds = ['TXG_FOB_USD','TMG_CIF_USD']
export_inds = ['TXG_FOB_USD','TXG_DS_FOB_USD','TXG_FS_FOB_USD']
import_inds = ['TMG_CIF_USD','TMG_DS_CIF_USD','TMG_FS_CIF_USD']
extracted_trade = []
extracted_export = []
extracted_import = []
for item in df_trade1:
    if item['@INDICATOR'] in trade_inds and item['@FREQ'] == 'M':
        extracted_trade.append(item)
    elif item['@INDICATOR'] in export_inds and item['@FREQ'] == 'M':
        extracted_export.append(item)
    elif item['@INDICATOR'] in import_inds and item['@FREQ'] == 'M':
        extracted_import.append(item)
    else:
        pass
make_gif_multivar('Trade', extracted_trade, shorten=True)
make_gif_multivar('Export', extracted_export, shorten=True)
make_gif_multivar('Import', extracted_import, shorten=True)

### Stock market
df_stock1 = df_stock['message:StructureSpecificData']['message:DataSet']['Series']
stock_inds = ['VNM_VN_EOP_IX','VNM_HNX_EOP_IX','VNM_VNX_EOP_IX']
stock30_inds = ['VNM_VN30_EOP_IX','VNM_HNX30_EOP_IX']
extracted_stock = []
extracted_stock30 = []
for item in df_stock1:
    if item['@INDICATOR'] in stock_inds and item['@FREQ'] == 'M':
        extracted_stock.append(item)
    elif item['@INDICATOR'] in stock30_inds and item['@FREQ'] == 'M':
        extracted_stock30.append(item)
    else:
        pass
make_gif_multivar('Stock Main Indices', extracted_stock, shorten=True)
make_gif_multivar('Stock Main Indices Top 30', extracted_stock30, shorten=True)