# 🌍 World Bank Development Indicators 3D Visualization

An interactive 3D web application for exploring World Bank development indicators through stunning globe visualizations. Built with Python, Plotly, and Dash.

![World Bank 3D Visualization](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-green.svg)
![Dash](https://img.shields.io/badge/Dash-2.0+-orange.svg)
![World Bank Data](https://img.shields.io/badge/Data-World%20Bank%20WDI-red.svg)

## 🎯 Features

- **20 Popular Development Indicators**: Curated selection of the most important global development metrics
- **Interactive 3D Globe**: Rotate, zoom, and hover for detailed country information
- **Real-time Statistics**: Dynamic calculation of top performers, averages, and ranges
- **Smart Color Schemes**: Automatic color mapping optimized for each indicator type
- **Responsive Design**: Modern, mobile-friendly interface
- **Data Caching**: Intelligent caching system for improved performance
- **Error Handling**: Robust error handling with user-friendly messages

## 📊 Available Indicators

### Economic Indicators
- 💰 GDP per capita (current US$)
- 📈 Foreign direct investment, net inflows (% of GDP)
- 🏭 Exports of goods and services (% of GDP)
- 📊 Inflation, consumer prices (annual %)

### Social Indicators
- 👥 Population, total
- 🏙️ Urban population (% of total population)
- 🌾 Rural population (% of total population)
- 💼 Unemployment, total (% of total labor force)
- 📚 Literacy rate, adult total (% of people ages 15 and above)
- 💸 Poverty headcount ratio at $2.15 a day (2017 PPP)

### Health & Education
- ❤️ Life expectancy at birth, total (years)
- 🏥 Current health expenditure per capita (current US$)
- 🎓 Government expenditure on education (% of GDP)

### Environment & Energy
- 🌡️ CO2 emissions per capita
- ⚡ Access to electricity (% of population)
- 🌳 Forest area (% of land area)
- 🔥 Access to clean fuels for cooking (% of population)
- ♻️ Renewable energy consumption (% of total final energy consumption)

### Technology
- 🌐 Internet users (% of population)
- 📱 Mobile cellular subscriptions (per 100 people)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- World Bank WDI CSV data files (see Data Setup below)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/deluair/WDI_3d.git
   cd WDI_3d
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **World Bank Data** (✅ **INCLUDED**):
   - All required World Bank WDI CSV files are included in the repository
   - No additional downloads needed - data is ready to use!
   - Files included:
     - `WDICSV.csv` (main data file - 197MB)
     - `WDICountry.csv` (country metadata)
     - `WDISeries.csv` (indicator metadata)
     - `WDIseries-time.csv` (time series metadata)
     - `WDIfootnote.csv` (footnotes)
     - `WDIcountry-series.csv` (country-series metadata)

4. **Run the application**:
   ```bash
   python main_app.py
   ```

5. **Open your browser** and navigate to: `http://127.0.0.1:8050/`

## 📁 Project Structure

```
WDI_3d/
├── 📄 main_app.py              # Main Dash web application
├── 📄 process_wb_data.py       # Data processing and caching
├── 📄 wb_globe.py              # 3D globe visualization
├── 📄 config.py                # Configuration and constants
├── 📄 simple_app.py            # Simplified demo app
├── 📄 demo.py                  # Quick demo script
├── 📄 utility.py               # Interactive data exploration
├── 📄 requirements.txt         # Python dependencies
├── 📄 QUICK_START.md           # Quick start guide
├── 📄 README.md                # This file
├── 📄 LICENSE                  # MIT License
├── 📄 .gitignore               # Git exclusions
├── 📄 test_fix.py              # Error handling tests
├── 📄 test_workflow.py         # Workflow validation tests
├── 📄 final_test.py            # Complete validation suite
├── 📁 processed_data/          # Cached processed data (auto-created)
├── � WDICSV.csv              # ✅ World Bank main data (197MB)
├── 📊 WDICountry.csv          # ✅ Country metadata
├── 📊 WDISeries.csv           # ✅ Indicator metadata
├── 📊 WDIseries-time.csv      # ✅ Time series metadata
├── 📊 WDIfootnote.csv         # ✅ Data footnotes
└── 📊 WDIcountry-series.csv   # ✅ Country-series metadata
```

## 🔧 Usage

### Main Application

1. **Select an Indicator**: Choose from 20 popular development indicators
2. **Select a Year**: Pick from recent years (2018-2024) or historical data (2000-2017)
3. **Generate Globe**: Click "Generate 3D Globe" to create the visualization
4. **Explore**: 
   - Hover over countries for detailed information
   - Drag to rotate the globe
   - Scroll to zoom in/out
   - Use the buttons for additional info and available years

### Additional Tools

- **Simple App**: Run `python simple_app.py` for a basic version
- **Demo Script**: Run `python demo.py` for automated demonstrations
- **Data Utility**: Run `python utility.py` for interactive data exploration

## 🎨 Technical Features

### Data Processing
- **Automatic Country Mapping**: Maps World Bank country codes to ISO3 for globe visualization
- **Smart Caching**: Processes data once and caches results for faster subsequent loads
- **Data Validation**: Robust error handling for missing or invalid data
- **Regional Filtering**: Automatically excludes regional aggregates from visualizations

### Visualization
- **Adaptive Color Schemes**: Different color palettes for different indicator types
- **Statistical Overlays**: Real-time calculation and display of summary statistics
- **Performance Optimization**: Efficient rendering for large datasets
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Error Handling
- **Graceful Degradation**: Continues to work even with missing data
- **User Feedback**: Clear error messages and suggestions
- **Data Quality Checks**: Validates data integrity before visualization
- **Recovery Mechanisms**: Automatic fallback to alternative years when data is unavailable

## 🛠️ Configuration

Edit `config.py` to customize:

- **Indicator Selection**: Modify `POPULAR_INDICATORS` dictionary
- **Color Schemes**: Adjust `COLOR_SCHEMES` for different visualizations
- **Data Paths**: Change file paths and directories
- **Regional Exclusions**: Update `REGIONAL_AGGREGATES` list

## 📈 Performance

- **Fast Initial Load**: < 3 seconds for first indicator
- **Instant Switching**: < 1 second for cached indicators
- **Memory Efficient**: Optimized data structures and caching
- **Scalable**: Handles 200+ countries and 25+ years of data

## 🔍 Data Sources

- **Primary Source**: [World Bank Open Data](https://data.worldbank.org/)
- **Dataset**: World Development Indicators (WDI)
- **Coverage**: 200+ countries and territories
- **Time Range**: 1960-2024 (varies by indicator)
- **Update Frequency**: Annual

## 📋 Requirements

### Python Packages
- `dash>=2.0.0` - Web application framework
- `plotly>=5.0.0` - Interactive plotting library
- `pandas>=1.3.0` - Data manipulation and analysis
- `numpy>=1.21.0` - Numerical computing
- `pycountry>=22.0.0` - Country code mapping

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for data files
- **Browser**: Modern browser with JavaScript enabled

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Clone and setup
git clone https://github.com/deluair/WDI_3d.git
cd WDI_3d
pip install -r requirements.txt

# Run tests
python final_test.py

# Start development server
python main_app.py
```

## 🐛 Troubleshooting

### Common Issues

1. **"No module named..." errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **App startup issues**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're in the correct directory
   - Verify Python version is 3.8 or higher

3. **"No data available" messages**:
   - Try different years (recent years have better coverage)
   - Check the "Show Available Years" button

4. **Performance issues**:
   - Clear the `processed_data/` folder to rebuild cache
   - Restart the application

5. **Browser display issues**:
   - Use a modern browser (Chrome, Firefox, Safari, Edge)
   - Ensure JavaScript is enabled
   - Try refreshing the page

### Getting Help

- **Check the logs**: The terminal shows detailed processing information
- **Use the test scripts**: Run `python final_test.py` to validate setup
- **Open an issue**: [GitHub Issues](https://github.com/deluair/WDI_3d/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **World Bank** for providing open access to development data
- **Plotly** team for the excellent visualization library
- **Dash** community for the web application framework
- **PyCountry** contributors for country code mapping

## 📊 Examples

### GDP per Capita Visualization
```python
# Quick example to generate GDP per capita for 2023
from process_wb_data import process_indicator_for_year
from wb_globe import create_enhanced_3d_globe

df = process_indicator_for_year("NY.GDP.PCAP.CD", "2023")
fig = create_enhanced_3d_globe(df, "NY.GDP.PCAP.CD", "2023")
fig.show()
```

### Batch Processing Multiple Indicators
```python
# Process multiple indicators for analysis
indicators = ["NY.GDP.PCAP.CD", "SP.POP.TOTL", "EN.ATM.CO2E.PC"]
year = "2023"

for indicator in indicators:
    df = process_indicator_for_year(indicator, year)
    if df is not None:
        print(f"Processed {indicator}: {len(df)} countries")
```

## 🔮 Future Enhancements

- **Time Series Animation**: Animate changes over time
- **Comparison Mode**: Side-by-side indicator comparisons
- **Export Features**: PNG/PDF export of visualizations
- **Custom Indicators**: Upload and visualize custom datasets
- **API Integration**: Real-time data updates from World Bank API
- **Advanced Analytics**: Correlation analysis and trend detection

---

**Happy Exploring! 🌍📊**

For questions, suggestions, or contributions, please visit our [GitHub repository](https://github.com/deluair/WDI_3d).
- **Multi-Year Analysis**: Explore indicator data across different years (2000-2024)
- **Smart Country Mapping**: Intelligent country code mapping with pycountry integration
- **Popular Indicators**: Quick access to frequently used indicators like GDP, population, etc.
- **Data Caching**: Automatic caching of processed data for faster subsequent loads
- **Comprehensive Statistics**: Detailed statistics and rankings for each indicator

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- World Bank World Development Indicators (WDI) CSV files:
  - `WDICSV.csv` (main data file)
  - `WDICountry.csv` (country metadata)
  - `WDISeries.csv` (indicator metadata)
  - `WDIcountry-series.csv`
  - `WDIseries-time.csv` 
  - `WDIfootnote.csv`

### Installation

1. **Navigate to your WB_visualization directory**
   ```bash
   cd "c:\Users\mhossen\OneDrive - University of Tennessee\AI\WB_visualization"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   - Navigate to `http://127.0.0.1:8050/`

## 📊 Data Sources

### Primary Source
- **World Bank Open Data**: Official development indicators
  - Covers 200+ countries and territories
  - Annual data from 1960 to present
  - 1,400+ development indicators
  - Economic, social, environmental, and governance indicators

### Data Processing Pipeline
1. **Load**: Read data from local WDI CSV files
2. **Process**: Data cleaning, country mapping, and validation
3. **Map**: Convert country codes to ISO3 format using pycountry
4. **Cache**: Save processed data for faster subsequent loads
5. **Visualize**: 3D globe rendering with Plotly and Dash

## 🎨 Visualization Features

### Interactive Web Interface
- **Indicator Selection**: Dropdown with popular indicators and full catalog
- **Year Selection**: Choose any year from 2000-2024
- **Visualization Options**: Enable statistics display and auto-rotation
- **Real-Time Updates**: Automatic data processing and visualization updates

### Visual Design
- **Modern Dash Interface**: Clean, responsive web design
- **3D Globe Rendering**: Plotly-powered interactive globe
- **Smart Color Schemes**: Automatic color selection based on indicator type
- **Geographic Accuracy**: Proper country boundaries and projections
- **Professional Styling**: Dark theme with vibrant data visualization

## 📈 Application Architecture

### Core Components

1. **`app.py`**: Main Dash application with web interface
2. **`process_wb_data.py`**: World Bank data processing and country mapping
3. **`wb_globe.py`**: 3D globe visualization creation with Plotly
4. **`config.py`**: Configuration settings and indicator mappings

### Data Flow
1. User selects indicator and year in web interface
2. Application loads data from local WDI CSV files
3. Data is processed and cleaned with country mapping
4. 3D globe visualization is generated and displayed
5. Processed data is cached for future use

## ⚙️ Configuration

Key configuration options in `config.py`:

```python
# Popular indicators for quick access
POPULAR_INDICATORS = {
    "GDP per capita": "NY.GDP.PCAP.CD",
    "Population, total": "SP.POP.TOTL", 
    "Life expectancy": "SP.DYN.LE00.IN",
    # ... more indicators
}

# Color schemes for different indicator types
COLOR_SCHEMES = {
    "economic": "Viridis",
    "demographic": "Plasma", 
    "environmental": "RdYlGn",
    # ... more schemes
}
```

## 🔧 Technical Details

### Dependencies
- **Dash**: Web application framework for Python
- **Plotly**: Interactive visualization and 3D globe rendering
- **Pandas**: Data manipulation and analysis (≥2.0.0)
- **pycountry**: Country code mapping and validation (≥23.12.11)
- **NumPy**: Numerical computing support (≥1.24.0)

### Architecture
- **Modular Design**: Separate modules for data processing and visualization
- **Web-Based Interface**: Dash framework for interactive web application
- **Error Handling**: Comprehensive error handling with user feedback
- **Data Caching**: Automatic caching of processed data for performance
- **Responsive Design**: Web interface adapts to different screen sizes

## 📱 Usage Examples

### Running the Application
```bash
# Start the Dash web application
python app.py

# Open browser and navigate to:
# http://127.0.0.1:8050/
```

### Using Individual Components
```python
# Process data for a specific indicator and year
from process_wb_data import process_indicator_for_year
df = process_indicator_for_year("NY.GDP.PCAP.CD", "2023")

# Create 3D visualization
from wb_globe import create_enhanced_3d_globe
fig = create_enhanced_3d_globe(df, "NY.GDP.PCAP.CD", "2023")
fig.show()

# Show statistics
from wb_globe import add_indicator_statistics
add_indicator_statistics(df, "NY.GDP.PCAP.CD", "2023")
```

### Command Line Usage
```bash
# Process and visualize a specific indicator
python wb_globe.py --indicator NY.GDP.PCAP.CD --year 2023

# Process data only
python process_wb_data.py --indicator SP.POP.TOTL --year 2022
```

## 🎯 Sample Output

When you run the application, you'll see:

1. **Console Output**:
   ```
   🌍 Starting World Bank Indicators 3D Visualization...
   📅 Processing NY.GDP.PCAP.CD for year 2023...
   🗺️  Creating country mapping...
   ✅ Successfully processed 180 countries with valid data
   
   📊 GDP PER CAPITA (CURRENT US$) - 2023
   Total Countries with Data: 180
   🏆 TOP 10 COUNTRIES:
   1. Luxembourg                 $135,605.0
   2. Switzerland               $92,434.0
   3. Norway                    $89,154.0
   ...
   ```

2. **Interactive 3D Globe**: Opens in your default web browser

## 🛠️ Troubleshooting

### Common Issues

1. **Missing Data Files**
   - Ensure all WDI CSV files are in the project directory
   - Download latest files from World Bank Open Data

2. **Memory Issues with Large Files**
   - The WDICSV.csv file can be quite large
   - Processing is done efficiently with pandas chunks

3. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **Browser Not Opening**
   - Manually open `http://127.0.0.1:8050/` in your browser
   - Check if port 8050 is available

## 🌍 Available Indicators

The system supports all World Bank indicators including:

### Economic Indicators
- GDP per capita, GDP growth, GNI per capita
- Inflation, unemployment, trade balance
- Foreign direct investment, debt ratios

### Social Indicators  
- Population demographics, life expectancy
- Education enrollment, literacy rates
- Health expenditure, mortality rates

### Environmental Indicators
- CO2 emissions, forest coverage
- Access to clean water and sanitation
- Renewable energy consumption

### Governance Indicators
- Government effectiveness, rule of law
- Regulatory quality, control of corruption

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional visualization types (choropleth maps, scatter plots)
- Time series animations
- Indicator comparison features
- Export functionality (PNG, SVG, PDF)
- Mobile responsiveness enhancements

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **World Bank**: For providing comprehensive open development data
- **Plotly**: Excellent visualization framework
- **Trade_3d Project**: Original inspiration for the 3D globe concept
- **pycountry**: Country code standardization

## 📞 Support

For questions, issues, or suggestions:

1. Check the troubleshooting section
2. Review the code documentation  
3. Create an issue in the repository

---

**Enjoy exploring global development patterns! 🌍📊✨**
