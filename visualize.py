# %%
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# %%
# Load JSON data
with open('extracted_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define multiple indicators and frequency
## quarterly data
indicators_q = [
    "NGDP_R_PA_XDC", "NGDPVA_R_ISIC4_A_XDC", "VNM_NGDPVA_R_ISIC4_BTF_XDC",
    "VNM_NGDPVA_R_ISIC4_GTT_XDC", "LUR_PT", "LUR15O_PT", "LEU_PT", "LME_AVG_XDC",
    "PPPI_ISIC4_A_BY_PP_IX", "VNM_PPPI_ISIC4_BTE_BY_PP_IX", "VNM_PPPI_ISIC4_HTJ_PTR_BY_PP_IX"
]
frequency_q = "Q"

## annual data
indicators_a = [
    "NGDP_R_XDC", "NC_R_XDC", "NCGG_R_XDC", "NCP_R_XDC", "NI_R_XDC", "NFI_R_XDC",
    "NNXGS_R_XDC", "NGDP_R_BY1994_XDC", "NC_R_BY1994_XDC", "NCG_R_BY1994_XDC",
    "NCP_R_BY1994_XDC", "NI_R_BY1994_XDC", "NFI_R_BY1994_XDC", "NNXGS_R_BY1994_XDC",
    "LP_PE_NUM"
]
frequency_a = "A"

## monthly data
indicators_m = [
    "VNM_VN_EOP_IX", "VNM_HNX_EOP_IX", "VNM_VN30_EOP_IX", "VNM_HNX30_EOP_IX",
    "PCPI_IX", "PCPI_CP_01_IX", "PCPI_CP_04_IX", "PCPI_CP_06_IX", "PCPIFFA_IX",
    "PCPI_CP_07_IX", "PCPI_CP_08_IX"
]
frequency_m = "M"

# Flatten all entries into one list
all_entries = []
for block in data:
    if isinstance(block, list):
        all_entries.extend(block)
    else:
        all_entries.append(block)

### Helper function to safely convert values to float
def safe_float(value):
    try:
        return float(value.replace(" ", ""))
    except (ValueError, AttributeError):
        return None

### QUARTERLY DATA
series_dict_q = {}
for entry in all_entries:
    if entry.get("@FREQ") == frequency_q and entry.get("@INDICATOR") in indicators_q:
        indicator = entry["@INDICATOR"]
        obs_list = entry.get("Obs", [])
        series_dict_q[indicator] = {}
        for obs in obs_list:
            val = safe_float(obs.get("@OBS_VALUE", ""))
            if val is not None:
                series_dict_q[indicator][obs["@TIME_PERIOD"]] = val

df_q = pd.DataFrame(series_dict_q)
df_q.index.name = "Date"
df_q = df_q.sort_index().reset_index()

### ANNUAL DATA
series_dict_a = {}
for entry in all_entries:
    if entry.get("@FREQ") == frequency_a and entry.get("@INDICATOR") in indicators_a:
        indicator = entry["@INDICATOR"]
        obs_list = entry.get("Obs", [])
        series_dict_a[indicator] = {}
        for obs in obs_list:
            val = safe_float(obs.get("@OBS_VALUE", ""))
            if val is not None:
                series_dict_a[indicator][obs["@TIME_PERIOD"]] = val

df_a = pd.DataFrame(series_dict_a)
df_a.index.name = "Date"
df_a = df_a.sort_index().reset_index()

### MONTHLY DATA
series_dict_m = {}
for entry in all_entries:
    if entry.get("@FREQ") == frequency_m and entry.get("@INDICATOR") in indicators_m:
        indicator = entry["@INDICATOR"]
        obs_list = entry.get("Obs", [])
        series_dict_m[indicator] = {}
        for obs in obs_list:
            val = safe_float(obs.get("@OBS_VALUE", ""))
            if val is not None:
                series_dict_m[indicator][obs["@TIME_PERIOD"]] = val

df_m = pd.DataFrame(series_dict_m)
df_m.index.name = "Date"
df_m = df_m.sort_index().reset_index()


# %%
# Load the CSV from GitHub (raw URL)
desc_url = "https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv"
desc_df = pd.read_csv(desc_url)

# Create a mapping from indicator code to description
label_map = dict(zip(desc_df["indicator"], desc_df["desc"]))

# Select indicators you want to plot
indicators = [
    "LUR_PT",
    "LUR15O_PT",
    "LEU_PT",
]

# Melt the DataFrame for Plotly
df_long = df_q[["Date"] + indicators].melt(
    id_vars="Date",
    value_vars=indicators,
    var_name="Indicator",
    value_name="Value"
)
df_long = df_long.dropna(subset=["Value"])
# if we want to log it
# df_long["Value"] = np.log(df_long["Value"])
# df_long["Value"] = df_long["Value"]/1000
# Map labels using the CSV
df_long["Label"] = df_long["Indicator"].map(label_map).fillna(df_long["Indicator"])

# Plot
fig = px.line(
    df_long,
    x="Date",
    y="Value",
    color="Label",  # Use descriptive labels for the legend
    title="Unemployment"
)
fig.update_layout(
    width=800,
    height=500,
    xaxis_title="Date",
    yaxis_title="per cent"
)
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("q_unemp.html", full_html=False, include_plotlyjs='cdn')

# %%
# Load the CSV from GitHub (raw URL)
desc_url = "https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv"
desc_df = pd.read_csv(desc_url)

# Create a mapping from indicator code to description
label_map = dict(zip(desc_df["indicator"], desc_df["desc"]))

# Select indicators you want to plot
indicators = [
    "LME_AVG_XDC"
]

# Melt the DataFrame for Plotly
df_long = df_q[["Date"] + indicators].melt(
    id_vars="Date",
    value_vars=indicators,
    var_name="Indicator",
    value_name="Value"
)
df_long = df_long.dropna(subset=["Value"])
# if we want to log it
# df_long["Value"] = np.log(df_long["Value"])
# df_long["Value"] = df_long["Value"]/1000
# Map labels using the CSV
df_long["Label"] = df_long["Indicator"].map(label_map).fillna(df_long["Indicator"])

# Plot
fig = px.line(
    df_long,
    x="Date",
    y="Value",
    color="Label",  # Use descriptive labels for the legend
    title="Monthly Earnings"
)
fig.update_layout(
    width=800,
    height=500,
    xaxis_title="Date",
    yaxis_title="VND"
)
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("q_earnings.html", full_html=False, include_plotlyjs='cdn')

# %%
# Load the CSV from GitHub (raw URL)
desc_url = "https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv"
desc_df = pd.read_csv(desc_url)

# Create a mapping from indicator code to description
label_map = dict(zip(desc_df["indicator"], desc_df["desc"]))

# Select indicators you want to plot
indicators = [
    "NGDP_R_PA_XDC",
    "NGDPVA_R_ISIC4_A_XDC",
    "VNM_NGDPVA_R_ISIC4_BTF_XDC",
    "VNM_NGDPVA_R_ISIC4_GTT_XDC"
]

# Melt the DataFrame for Plotly
df_long = df_q[["Date"] + indicators].melt(
    id_vars="Date",
    value_vars=indicators,
    var_name="Indicator",
    value_name="Value"
)
# if we want to log it
df_long["Value"] = np.log(df_long["Value"])
# df_long["Value"] = df_long["Value"]/1000
# Map labels using the CSV
df_long["Label"] = df_long["Indicator"].map(label_map).fillna(df_long["Indicator"])

# Plot
fig = px.line(
    df_long,
    x="Date",
    y="Value",
    color="Label",  # Use descriptive labels for the legend
    title="Real GDP (Supply side)"
)
fig.update_layout(
    width=800,
    height=500,
    xaxis_title="Date",
    yaxis_title="Log"
)
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("q_Gdp.html", full_html=False, include_plotlyjs='cdn')

# %%
# Load the CSV from GitHub (raw URL)
desc_url = "https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv"
desc_df = pd.read_csv(desc_url)

# Create a mapping from indicator code to description
label_map = dict(zip(desc_df["indicator"], desc_df["desc"]))

# Select indicators you want to plot
indicators = [
    "PPPI_ISIC4_A_BY_PP_IX",
    "VNM_PPPI_ISIC4_HTJ_PTR_BY_PP_IX",
    "VNM_PPPI_ISIC4_BTE_BY_PP_IX"
]

# Melt the DataFrame for Plotly
df_long = df_q[["Date"] + indicators].melt(
    id_vars="Date",
    value_vars=indicators,
    var_name="Indicator",
    value_name="Value"
)
# if we want to log it
# df_long["Value"] = df_long["Value"]/1000
# Map labels using the CSV
df_long["Label"] = df_long["Indicator"].map(label_map).fillna(df_long["Indicator"])

# Plot
fig = px.line(
    df_long,
    x="Date",
    y="Value",
    color="Label",  # Use descriptive labels for the legend
    title="Producer Price Index"
)
fig.update_layout(
    width=800,
    height=500,
    xaxis_title="Date",
    yaxis_title=""
)
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("q_ppi.html", full_html=False, include_plotlyjs='cdn')

# %%
df_m

# %%
# Load the CSV from GitHub (raw URL)
desc_url = "https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv"
desc_df = pd.read_csv(desc_url)

# Create a mapping from indicator code to description
label_map = dict(zip(desc_df["indicator"], desc_df["desc"]))

# Select indicators you want to plot
indicators = [
    "PCPI_IX",
    "PCPI_CP_01_IX",
    "PCPIFFA_IX",
    "PCPI_CP_04_IX",
    "PCPI_CP_06_IX",
    "PCPI_CP_07_IX",
    "PCPI_CP_08_IX"
]

# Melt the DataFrame for Plotly
df_long = df_m[["Date"] + indicators].melt(
    id_vars="Date",
    value_vars=indicators,
    var_name="Indicator",
    value_name="Value"
)
df_long = df_long.dropna(subset=["Value"])

# Map and shorten labels
df_long["Label"] = df_long["Indicator"].map(label_map).fillna(df_long["Indicator"])
df_long["Label"] = df_long["Label"].str[:30]  # Shorten to first 30 characters

# Plot
fig = px.line(
    df_long,
    x="Date",
    y="Value",
    color="Label",  # Use descriptive labels for the legend
    title="Consumer Price Index (CPI) - Monthly"
)
fig.update_layout(
    width=800,
    height=500,
    xaxis_title="Date",
    yaxis_title="per cent"
)
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("q_cpi.html", full_html=False, include_plotlyjs='cdn')

# %%
# Load the CSV from GitHub (raw URL)
desc_url = "https://raw.githubusercontent.com/thanhqtran/gso-macro-monitor/main/dsbb_indicator_desc.csv"
desc_df = pd.read_csv(desc_url)

# Create a mapping from indicator code to description
label_map = dict(zip(desc_df["indicator"], desc_df["desc"]))

# Select indicators you want to plot
indicators = [
    "VNM_VN_EOP_IX",
    "VNM_HNX_EOP_IX",
    "VNM_VN30_EOP_IX",
    "VNM_HNX30_EOP_IX"
]

# Melt the DataFrame for Plotly
df_long = df_m[["Date"] + indicators].melt(
    id_vars="Date",
    value_vars=indicators,
    var_name="Indicator",
    value_name="Value"
)
df_long = df_long.dropna(subset=["Value"])

# Map and shorten labels
df_long["Label"] = df_long["Indicator"].map(label_map).fillna(df_long["Indicator"])
df_long["Label"] = df_long["Label"].str[:30]  # Shorten to first 30 characters

# Plot
fig = px.line(
    df_long,
    x="Date",
    y="Value",
    color="Label",  # Use descriptive labels for the legend
    title="Stock Market Indices - Monthly"
)
fig.update_layout(
    width=800,
    height=500,
    xaxis_title="Date",
    yaxis_title=""
)
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("m_stock.html", full_html=False, include_plotlyjs='cdn')

# %%
import plotly.express as px
import pandas as pd

ilo_url = 'https://rplumber.ilo.org/data/indicator/?id=HOW_TEMP_SEX_AGE_ECO_NB_Q&ref_area=VNM&sex=SEX_T&classif1=AGE_AGGREGATE_TOTAL&classif2=ECO_SECTOR_TOTAL&timefrom=2007&timeto=2023&type=code&format=.csv'
lab_data = pd.read_csv(ilo_url)
lab_df = pd.DataFrame(lab_data)

# Option 1: Use string version of quarter for plotting
lab_df['time_q'] = lab_df['time']  # keep as '2021Q3', etc.

# Convert for calculations if needed
lab_df['time_dt'] = pd.PeriodIndex(lab_df['time'], freq='Q').to_timestamp()
lab_df['labor'] = lab_df['obs_value'] / (24 * 5)
lab_df = lab_df.sort_values('time_dt')

# Use string quarter labels on x-axis
fig = px.line(lab_df, x="time_q", y="obs_value")
fig.update_layout(
    width=600,
    height=400,
    yaxis_title="Weekly Hours Worked",
    xaxis_title=""
    )
fig.show()

# Output html that you can copy paste
fig.to_html(full_html=False, include_plotlyjs='cdn')
# Saves a html doc that you can copy paste
fig.write_html("q_labor.html", full_html=False, include_plotlyjs='cdn')


