# Configuration for World Bank Indicators 3D Visualization

# Data files configuration
WDI_MAIN_DATA_FILE = "WDICSV.csv"
WDI_COUNTRY_FILE = "WDICountry.csv"
WDI_SERIES_FILE = "WDISeries.csv"
WDI_COUNTRY_SERIES_FILE = "WDIcountry-series.csv"
WDI_SERIES_TIME_FILE = "WDIseries-time.csv"
WDI_FOOTNOTE_FILE = "WDIfootnote.csv"

# Directory for storing processed data files
DATA_DIR = "processed_data"

# File templates for processed data
PROCESSED_INDICATOR_FILE_TEMPLATE = "processed_{indicator_code}_{year}.csv"
PROCESSED_SUMMARY_FILE_TEMPLATE = "summary_{indicator_code}.csv"

# GeoJSON URL for country boundaries
GEOJSON_URL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

# Default visualization settings
DEFAULT_YEAR = "2023"
DEFAULT_YEARS_RANGE = list(range(2000, 2025))  # 2000-2024

# Top 20 most popular World Bank indicators for quick access
POPULAR_INDICATORS = {
    "GDP per capita (current US$)": "NY.GDP.PCAP.CD",
    "Population, total": "SP.POP.TOTL", 
    "Life expectancy at birth, total (years)": "SP.DYN.LE00.IN",
    "CO2 emissions per capita": "EN.GHG.CO2.PC.CE.AR5",
    "Access to electricity (% of population)": "EG.ELC.ACCS.ZS",
    "Internet users (% of population)": "IT.NET.USER.ZS",
    "Unemployment, total (% of total labor force)": "SL.UEM.TOTL.ZS",
    "Inflation, consumer prices (annual %)": "FP.CPI.TOTL.ZG",
    "Government expenditure on education (% of GDP)": "SE.XPD.TOTL.GD.ZS",
    "Current health expenditure per capita (current US$)": "SH.XPD.CHEX.PC.CD",
    "Rural population (% of total population)": "SP.RUR.TOTL.ZS",
    "Forest area (% of land area)": "AG.LND.FRST.ZS",
    "Access to clean fuels for cooking (% of population)": "EG.CFT.ACCS.ZS",
    "Literacy rate, adult total (% of people ages 15 and above)": "SE.ADT.LITR.ZS",
    "Poverty headcount ratio at $2.15 a day (2017 PPP) (%)": "SI.POV.DDAY",
    "Mobile cellular subscriptions (per 100 people)": "IT.CEL.SETS.P2",
    "Foreign direct investment, net inflows (% of GDP)": "BX.KLT.DINV.WD.GD.ZS",
    "Exports of goods and services (% of GDP)": "NE.EXP.GNFS.ZS",
    "Urban population (% of total population)": "SP.URB.TOTL.IN.ZS",    "Renewable energy consumption (% of total final energy consumption)": "EG.FEC.RNEW.ZS"
}

# Color schemes for different indicator types
COLOR_SCHEMES = {
    "economic": "Viridis",
    "demographic": "Plasma", 
    "environmental": "RdYlGn",
    "health": "Blues",
    "education": "Oranges",
    "technology": "Cividis",
    "default": "Viridis"
}

# Indicator categories for color scheme selection
INDICATOR_CATEGORIES = {
    "economic": ["NY.", "FP.", "SL.UEM", "BX.", "GC.", "NE."],
    "demographic": ["SP.POP", "SP.DYN", "SP.RUR", "SP.URB"],
    "environmental": ["EN.", "AG.LND", "EG.CFT", "ER."],
    "health": ["SH.", "SP.DYN.LE"],
    "education": ["SE."],
    "technology": ["IT.", "IP.", "TX.VAL.TECH"]
}

# Regional aggregates to exclude from country-specific visualizations
REGIONAL_AGGREGATES = [
    'AFE', 'AFG', 'AFW', 'ARB', 'CEB', 'CSS', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EUU',
    'FCS', 'HIC', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 'LCN', 'LDC', 'LIC', 'LMC',
    'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'OED', 'OSS', 'PRE', 'PSS', 'PST', 'SAS',
    'SSA', 'SSF', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS', 'UMC', 'WLD'
]

# Minimum data points required for visualization
MIN_DATA_POINTS = 5

# Chart dimensions
CHART_WIDTH = 1200
CHART_HEIGHT = 800
