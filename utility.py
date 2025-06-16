"""
Utility script to quickly test and explore World Bank indicators
"""

import pandas as pd
import config
from process_wb_data import get_available_years_for_indicator, get_indicator_info
from wb_globe import create_enhanced_3d_globe, add_indicator_statistics

def list_popular_indicators():
    """List popular indicators available for quick access."""
    print("🌟 Popular World Bank Indicators:")
    print("=" * 50)
    for i, (name, code) in enumerate(config.POPULAR_INDICATORS.items(), 1):
        print(f"{i:2d}. {name}")
        print(f"     Code: {code}")
        print()

def quick_visualization(indicator_code=None, year=None):
    """Create a quick visualization for testing."""
    # Use defaults if not provided
    if not indicator_code:
        indicator_code = config.POPULAR_INDICATORS["GDP per capita"]
    if not year:
        year = "2023"
    
    print(f"🚀 Creating quick visualization for {indicator_code} ({year})")
    
    # Import here to avoid circular imports
    from process_wb_data import process_indicator_for_year
    
    # Process data
    df = process_indicator_for_year(indicator_code, year)
    
    if df is None or df.empty:
        print(f"❌ No data available for {indicator_code} in {year}")
        # Try a different year
        available_years = get_available_years_for_indicator(indicator_code)
        if available_years:
            latest_year = available_years[-1]
            print(f"🔄 Trying latest available year: {latest_year}")
            df = process_indicator_for_year(indicator_code, latest_year)
            year = latest_year
    
    if df is not None and not df.empty:
        # Create visualization
        fig = create_enhanced_3d_globe(df, indicator_code, year)
        fig.show()
        
        # Show statistics
        add_indicator_statistics(df, indicator_code, year)
        
        print(f"✅ Successfully created visualization with {len(df)} countries")
    else:
        print("❌ Could not create visualization - no data available")

def check_data_files():
    """Check if all required data files are present."""
    print("🔍 Checking for required data files...")
    print("=" * 40)
    
    required_files = [
        config.WDI_MAIN_DATA_FILE,
        config.WDI_COUNTRY_FILE,
        config.WDI_SERIES_FILE,
        config.WDI_COUNTRY_SERIES_FILE,
        config.WDI_SERIES_TIME_FILE,
        config.WDI_FOOTNOTE_FILE
    ]
    
    all_present = True
    for file in required_files:
        try:
            df = pd.read_csv(file)
            print(f"✅ {file} - Found ({len(df):,} rows)")
        except FileNotFoundError:
            print(f"❌ {file} - Missing")
            all_present = False
        except Exception as e:
            print(f"⚠️  {file} - Error: {e}")
            all_present = False
    
    if all_present:
        print("\n🎉 All required files are present!")
        return True
    else:
        print("\n❌ Some files are missing. Please ensure all WDI CSV files are in the directory.")
        return False

def explore_indicator(indicator_code):
    """Explore an indicator in detail."""
    print(f"🔍 Exploring indicator: {indicator_code}")
    print("=" * 50)
    
    # Get indicator info
    info = get_indicator_info(indicator_code)
    print(f"Name: {info['name']}")
    print(f"Topic: {info['topic']}")
    print(f"Unit: {info['unit']}")
    print(f"Definition: {info['definition'][:200]}..." if len(info['definition']) > 200 else f"Definition: {info['definition']}")
    
    # Get available years
    years = get_available_years_for_indicator(indicator_code)
    if years:
        print(f"Available years: {len(years)} years from {years[0]} to {years[-1]}")
        print(f"Recent years: {', '.join(years[-5:])}")
    else:
        print("No years with data found")

def main():
    """Main menu for the utility script."""
    print("🌍 World Bank Indicators 3D Visualization - Utility Script")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Check data files")
        print("2. List popular indicators")
        print("3. Quick visualization (GDP per capita)")
        print("4. Custom visualization")
        print("5. Explore indicator")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            check_data_files()
        
        elif choice == "2":
            list_popular_indicators()
        
        elif choice == "3":
            quick_visualization()
        
        elif choice == "4":
            indicator = input("Enter indicator code (e.g., NY.GDP.PCAP.CD): ").strip()
            year = input("Enter year (e.g., 2023): ").strip()
            if indicator:
                quick_visualization(indicator, year if year else None)
            else:
                print("❌ Please provide an indicator code")
        
        elif choice == "5":
            indicator = input("Enter indicator code to explore: ").strip()
            if indicator:
                explore_indicator(indicator)
            else:
                print("❌ Please provide an indicator code")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter a number between 1-6.")

if __name__ == "__main__":
    main()
