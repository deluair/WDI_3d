"""
Final setup validation and quick start guide for World Bank 3D Visualization
"""

import pandas as pd
import os
import sys

def check_setup():
    """Check if the setup is complete and working."""
    print("🔍 World Bank 3D Visualization - Setup Check")
    print("=" * 60)
    
    # Check data files
    print("📂 Checking data files...")
    required_files = [
        'WDICSV.csv',
        'WDICountry.csv', 
        'WDISeries.csv',
        'WDIcountry-series.csv',
        'WDIseries-time.csv',
        'WDIfootnote.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                print(f"   ✅ {file} - Found ({len(df):,} rows)")
            except Exception as e:
                print(f"   ⚠️  {file} - Error reading: {e}")
                missing_files.append(file)
        else:
            print(f"   ❌ {file} - Missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    # Check Python packages
    print("\n📦 Checking Python packages...")
    required_packages = [
        'pandas', 'plotly', 'dash', 'numpy', 'pycountry'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Test data processing
    print("\n🧪 Testing data processing...")
    try:
        from process_wb_data import process_indicator_for_year
        df = process_indicator_for_year("NY.GDP.PCAP.CD", "2023")
        if df is not None and not df.empty:
            print(f"   ✅ Data processing works ({len(df)} countries)")
        else:
            print("   ❌ Data processing failed - no data returned")
            return False
    except Exception as e:
        print(f"   ❌ Data processing error: {e}")
        return False
    
    # Test visualization
    print("\n🌐 Testing visualization...")
    try:
        from wb_globe import create_enhanced_3d_globe
        fig = create_enhanced_3d_globe(df, "NY.GDP.PCAP.CD", "2023")
        if fig:
            print("   ✅ Visualization creation works")
        else:
            print("   ❌ Visualization creation failed")
            return False
    except Exception as e:
        print(f"   ❌ Visualization error: {e}")
        return False
    
    print("\n🎉 All checks passed! Setup is complete and working.")
    return True

def show_quick_start():
    """Show quick start options."""
    print("\n🚀 Quick Start Options:")
    print("=" * 40)
    
    print("1. 🌐 Web Interface (Recommended):")
    print("   python simple_app.py")
    print("   Then open: http://127.0.0.1:8051/")
    
    print("\n2. 🎮 Interactive Demo:")
    print("   python demo.py")
    
    print("\n3. 📊 Command Line:")
    print("   python wb_globe.py --indicator NY.GDP.PCAP.CD --year 2023")
    
    print("\n4. 🔧 Interactive Utility:")
    print("   python utility.py")
    
    print("\n📖 Popular Indicators:")
    print("   • NY.GDP.PCAP.CD - GDP per capita")
    print("   • SP.DYN.LE00.IN - Life expectancy") 
    print("   • EN.GHG.CO2.PC.CE.AR5 - CO2 emissions per capita")
    print("   • SP.POP.TOTL - Population total")
    print("   • EG.ELC.ACCS.ZS - Access to electricity")

def main():
    """Main function."""
    print("🌍 World Bank Indicators 3D Visualization")
    print("   Setup Validation & Quick Start Guide")
    print("=" * 60)
    
    # Check setup
    if check_setup():
        show_quick_start()
        
        print("\n" + "="*60)
        choice = input("\nWould you like to start the web interface now? (y/n): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🚀 Starting web interface...")
            print("📱 Opening in browser at: http://127.0.0.1:8051/")
            
            try:
                os.system("python simple_app.py")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
        else:
            print("\n👋 Setup complete! Use the commands above to get started.")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")

if __name__ == "__main__":
    main()
