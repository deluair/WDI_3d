import pandas as pd
import pycountry
import numpy as np
import os
import argparse
from typing import Dict, List, Optional, Tuple
import config

# Ensure the directory for saving files exists
if not os.path.exists(config.DATA_DIR):
    os.makedirs(config.DATA_DIR)

def get_country_iso3_mapping() -> Dict[str, str]:
    """Create mapping from country codes to ISO3 codes using pycountry."""
    print("Creating country code to ISO3 mapping...")
    
    # Load WDI country data
    try:
        country_df = pd.read_csv(config.WDI_COUNTRY_FILE)
        print(f"Loaded {len(country_df)} countries from WDI country file")
    except FileNotFoundError:
        print(f"Error: Could not find {config.WDI_COUNTRY_FILE}")
        return {}
    
    country_mapping = {}
    
    for _, row in country_df.iterrows():
        wb_code = row['Country Code']
        wb_name = row['Short Name']
        
        # Skip regional aggregates
        if wb_code in config.REGIONAL_AGGREGATES:
            continue
            
        # Try to find ISO3 code using pycountry
        iso3_code = None
        
        # First try with World Bank's 2-alpha code if available
        if '2-alpha code' in row and pd.notna(row['2-alpha code']):
            try:
                country_obj = pycountry.countries.get(alpha_2=row['2-alpha code'])
                if country_obj:
                    iso3_code = country_obj.alpha_3
            except (LookupError, AttributeError):
                pass
        
        # If that fails, try with country name
        if not iso3_code:
            try:
                country_obj = pycountry.countries.search_fuzzy(wb_name)[0]
                iso3_code = country_obj.alpha_3
            except (LookupError, AttributeError):
                pass
        
        # Manual mappings for special cases
        special_mappings = {
            'KSV': 'XKX',  # Kosovo
            'PSE': 'PSE',  # Palestine
            'TWN': 'TWN',  # Taiwan
            'HKG': 'HKG',  # Hong Kong
            'MAC': 'MAC',  # Macao
        }
        
        if wb_code in special_mappings:
            iso3_code = special_mappings[wb_code]
        
        if iso3_code:
            country_mapping[wb_code] = iso3_code
        else:
            print(f"Warning: Could not map {wb_code} ({wb_name}) to ISO3")
    
    print(f"Successfully mapped {len(country_mapping)} countries to ISO3 codes")
    return country_mapping

def get_country_name_from_iso3(iso3_code: str) -> str:
    """Get country name from ISO3 code."""
    try:
        return pycountry.countries.get(alpha_3=iso3_code).name
    except (LookupError, AttributeError):
        return iso3_code

def load_and_process_indicator_data(indicator_code: str, year: str) -> Optional[pd.DataFrame]:
    """Load and process World Bank indicator data for a specific indicator and year."""
    print(f"\\nProcessing indicator {indicator_code} for year {year}...")
    
    try:
        # Load main WDI data
        print("Loading WDI main data file...")
        df = pd.read_csv(config.WDI_MAIN_DATA_FILE)
        print(f"Loaded {len(df)} rows from main data file")
        
        # Filter for specific indicator
        indicator_df = df[df['Indicator Code'] == indicator_code].copy()
        if indicator_df.empty:
            print(f"No data found for indicator {indicator_code}")
            return None
        
        print(f"Found {len(indicator_df)} countries with data for {indicator_code}")
        
        # Extract year column data
        if year not in indicator_df.columns:
            print(f"Year {year} not available in dataset")
            return None
        
        # Create country mapping
        country_mapping = get_country_iso3_mapping()
        
        # Process the data
        processed_data = []
        
        for _, row in indicator_df.iterrows():
            wb_code = row['Country Code']
            wb_name = row['Country Name']
            value = row[year]
            
            # Skip if no value for this year
            if pd.isna(value):
                continue
            
            # Skip regional aggregates
            if wb_code in config.REGIONAL_AGGREGATES:
                continue
            
            # Get ISO3 code
            iso3_code = country_mapping.get(wb_code)
            if not iso3_code:
                continue
            
            # Get country name from ISO3
            country_name = get_country_name_from_iso3(iso3_code)
            
            processed_data.append({
                'CountryCode': wb_code,
                'ISO3': iso3_code,
                'CountryName': country_name,
                'IndicatorValue': float(value),
                'Year': int(year)
            })
        
        if not processed_data:
            print(f"No valid data points found for {indicator_code} in {year}")
            return None
        
        result_df = pd.DataFrame(processed_data)
        result_df = result_df.sort_values('IndicatorValue', ascending=False)
        
        print(f"Successfully processed {len(result_df)} countries with valid data")
        return result_df
        
    except FileNotFoundError as e:
        print(f"Error: Could not find required data file: {e}")
        return None
    except Exception as e:
        print(f"Error processing indicator data: {e}")
        return None

def get_indicator_info(indicator_code: str) -> Dict[str, str]:
    """Get indicator information from WDI series file."""
    try:
        series_df = pd.read_csv(config.WDI_SERIES_FILE)
        indicator_info = series_df[series_df['Series Code'] == indicator_code]
        
        if not indicator_info.empty:
            row = indicator_info.iloc[0]
            
            # Helper function to safely get string values, handling NaN
            def safe_get_str(column_name, default=''):
                value = row.get(column_name, default)
                if pd.isna(value):
                    return default
                return str(value)
            
            return {
                'name': safe_get_str('Indicator Name', indicator_code),
                'unit': safe_get_str('Unit of measure', ''),
                'topic': safe_get_str('Topic', ''),
                'definition': safe_get_str('Short definition', '')
            }
    except Exception as e:
        print(f"Warning: Could not load indicator info: {e}")
    
    return {
        'name': indicator_code,
        'unit': '',
        'topic': '',
        'definition': ''
    }

def get_available_years_for_indicator(indicator_code: str) -> List[str]:
    """Get list of years with data for a specific indicator."""
    try:
        df = pd.read_csv(config.WDI_MAIN_DATA_FILE)
        indicator_df = df[df['Indicator Code'] == indicator_code]
        
        if indicator_df.empty:
            return []
        
        # Check which year columns have data
        year_columns = [col for col in indicator_df.columns 
                       if col.isdigit() and len(col) == 4]
        
        available_years = []
        for year in year_columns:
            if indicator_df[year].notna().any():
                available_years.append(year)
        
        return sorted(available_years)
    except Exception as e:
        print(f"Error getting available years: {e}")
        return []

def save_processed_data(df: pd.DataFrame, indicator_code: str, year: str) -> str:
    """Save processed data to CSV file."""
    filename = config.PROCESSED_INDICATOR_FILE_TEMPLATE.format(
        indicator_code=indicator_code.replace('.', '_'), 
        year=year
    )
    filepath = os.path.join(config.DATA_DIR, filename)
    
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to {filepath}")
    return filepath

def load_processed_data(indicator_code: str, year: str) -> Optional[pd.DataFrame]:
    """Load processed data from CSV file if it exists."""
    filename = config.PROCESSED_INDICATOR_FILE_TEMPLATE.format(
        indicator_code=indicator_code.replace('.', '_'), 
        year=year
    )
    filepath = os.path.join(config.DATA_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"Loading cached processed data from {filepath}")
        return pd.read_csv(filepath)
    return None

def process_indicator_for_year(indicator_code: str, year: str, force_refresh: bool = False) -> Optional[pd.DataFrame]:
    """Process an indicator for a specific year, with caching."""
    
    # Try to load cached data first
    if not force_refresh:
        cached_df = load_processed_data(indicator_code, year)
        if cached_df is not None:
            return cached_df
    
    # Process fresh data
    df = load_and_process_indicator_data(indicator_code, year)
    if df is not None:
        save_processed_data(df, indicator_code, year)
    
    return df

def get_indicator_summary_stats(df: pd.DataFrame, indicator_code: str) -> Dict:
    """Calculate summary statistics for an indicator."""
    if df.empty:
        return {}
    
    return {
        'count': len(df),
        'mean': df['IndicatorValue'].mean(),
        'median': df['IndicatorValue'].median(),
        'std': df['IndicatorValue'].std(),
        'min': df['IndicatorValue'].min(),
        'max': df['IndicatorValue'].max(),
        'top_country': df.iloc[0]['CountryName'] if not df.empty else '',
        'top_value': df.iloc[0]['IndicatorValue'] if not df.empty else 0
    }

def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description="Process World Bank indicator data for 3D visualization")
    parser.add_argument("--indicator", type=str, required=True, 
                       help="World Bank indicator code (e.g., NY.GDP.PCAP.CD)")
    parser.add_argument("--year", type=str, default=config.DEFAULT_YEAR,
                       help="Year to process (default: 2023)")
    parser.add_argument("--force", action="store_true",
                       help="Force refresh of cached data")
    
    args = parser.parse_args()
    
    print(f"Processing indicator: {args.indicator}")
    print(f"Year: {args.year}")
    
    # Get indicator info
    info = get_indicator_info(args.indicator)
    print(f"Indicator name: {info['name']}")
    
    # Process data
    df = process_indicator_for_year(args.indicator, args.year, args.force)
    
    if df is not None:
        stats = get_indicator_summary_stats(df, args.indicator)
        print(f"\\nSummary Statistics:")
        print(f"Countries with data: {stats['count']}")
        print(f"Mean value: {stats['mean']:.2f}")
        print(f"Top country: {stats['top_country']} ({stats['top_value']:.2f})")
    else:
        print("Failed to process data")

if __name__ == "__main__":
    main()
