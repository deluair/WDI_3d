# 🌍 World Bank 3D Visualization - Quick Start Guide

## 🚀 Getting Started

Your World Bank 3D visualization system is now ready! Here's how to use it:

### 1. **Main Application** (Recommended)
```bash
python main_app.py
```
- **URL**: http://127.0.0.1:8050/
- **Features**: 20 most popular World Bank indicators
- **Interface**: Professional web interface with rich features

### 2. **Simple Test Application**
```bash
python simple_app.py
```
- **URL**: http://127.0.0.1:8051/
- **Features**: Basic interface for quick testing

### 3. **Command Line Usage**
```bash
# Generate specific visualizations
python wb_globe.py --indicator NY.GDP.PCAP.CD --year 2023

# Process data only
python process_wb_data.py --indicator SP.POP.TOTL --year 2022
```

### 4. **Interactive Demo**
```bash
python demo.py
```
- **Features**: Guided demo with 3 example visualizations

## 📊 Top 20 Popular Indicators Available

| **Category** | **Indicator** | **Code** |
|--------------|---------------|----------|
| **💰 Economic** | GDP per capita (current US$) | `NY.GDP.PCAP.CD` |
| | Unemployment, total (% of total labor force) | `SL.UEM.TOTL.ZS` |
| | Inflation, consumer prices (annual %) | `FP.CPI.TOTL.ZG` |
| | Foreign direct investment, net inflows (% of GDP) | `BX.KLT.DINV.WD.GD.ZS` |
| | Exports of goods and services (% of GDP) | `NE.EXP.GNFS.ZS` |
| **👥 Social** | Population, total | `SP.POP.TOTL` |
| | Life expectancy at birth, total (years) | `SP.DYN.LE00.IN` |
| | Rural population (% of total population) | `SP.RUR.TOTL.ZS` |
| | Urban population (% of total population) | `SP.URB.TOTL.IN.ZS` |
| | Literacy rate, adult total (% of people ages 15 and above) | `SE.ADT.LITR.ZS` |
| | Poverty headcount ratio at $2.15 a day (2017 PPP) (%) | `SI.POV.DDAY` |
| **🏥 Health & Education** | Current health expenditure per capita (current US$) | `SH.XPD.CHEX.PC.CD` |
| | Government expenditure on education (% of GDP) | `SE.XPD.TOTL.GD.ZS` |
| **🌱 Environmental** | CO2 emissions per capita | `EN.GHG.CO2.PC.CE.AR5` |
| | Forest area (% of land area) | `AG.LND.FRST.ZS` |
| | Access to clean fuels for cooking (% of population) | `EG.CFT.ACCS.ZS` |
| | Renewable energy consumption (% of total final energy consumption) | `EG.FEC.RNEW.ZS` |
| **📱 Technology** | Access to electricity (% of population) | `EG.ELC.ACCS.ZS` |
| | Internet users (% of population) | `IT.NET.USER.ZS` |
| | Mobile cellular subscriptions (per 100 people) | `IT.CEL.SETS.P2` |

## 🎯 How to Use the Main Application

1. **Open the application**: Go to http://127.0.0.1:8050/
2. **Select an indicator**: Choose from 20 popular development indicators
3. **Choose a year**: Recent years (2018-2024) have better data coverage
4. **Generate globe**: Click "Generate 3D Globe" to create visualization
5. **Explore**: 
   - Drag to rotate the globe
   - Scroll to zoom in/out
   - Hover over countries for detailed data

## 🔧 Additional Features

- **📈 Show Available Years**: Check which years have data for an indicator
- **ℹ️ Indicator Details**: Get detailed information about an indicator
- **📊 Statistics**: View top/bottom countries and distribution data
- **🎨 Auto Color Schemes**: Colors automatically adjust based on indicator type

## 💡 Tips for Best Results

1. **Recent years** (2018-2024) typically have the most complete data
2. **Economic indicators** work well with log scale for better visualization
3. **Population data** is available for most years and countries
4. **Environmental indicators** may have less coverage for older years
5. **Try different years** if your first choice has limited data

## 🛠️ Troubleshooting

- **No data for indicator/year**: Try recent years (2020-2023)
- **App won't start**: Make sure port 8050 is free
- **Slow loading**: Large datasets may take a moment to process
- **Missing countries**: Some countries may not have data for specific indicators

## 📁 File Structure

```
WB_visualization/
├── main_app.py              # Main web application
├── simple_app.py            # Simple test application  
├── wb_globe.py              # 3D globe visualization
├── process_wb_data.py       # Data processing
├── config.py                # Configuration & indicators
├── demo.py                  # Demo script
├── utility.py               # Utility functions
├── setup_check.py           # System validation
├── requirements.txt         # Dependencies
├── processed_data/          # Cached processed data
└── WDI*.csv                 # World Bank data files
```

## 🎉 Enjoy Exploring!

You now have a powerful tool to explore global development patterns through stunning 3D visualizations. Each indicator tells a story about our world - discover the patterns, trends, and insights hidden in the data!

**Happy exploring! 🌍📊✨**
