import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import os
import argparse
from typing import Optional, Dict, List
import config
from process_wb_data import get_indicator_info

def determine_color_scheme(indicator_code: str) -> str:
    """Determine appropriate color scheme based on indicator category."""
    for category, prefixes in config.INDICATOR_CATEGORIES.items():
        if any(indicator_code.startswith(prefix) for prefix in prefixes):
            return config.COLOR_SCHEMES.get(category, config.COLOR_SCHEMES["default"])
    return config.COLOR_SCHEMES["default"]

def create_enhanced_3d_globe(df_processed: pd.DataFrame, 
                           indicator_code: str,
                           year: str,
                           geojson_url: str = config.GEOJSON_URL,
                           color_column: str = 'IndicatorValue', 
                           hover_name_column: str = 'CountryName') -> go.Figure:
    """Creates an enhanced 3D globe visualization for World Bank indicators."""
    
    if df_processed.empty:
        print("Warning: No data to visualize")
        return go.Figure()
    
    # Get indicator information
    indicator_info = get_indicator_info(indicator_code)
    indicator_name = indicator_info['name']
    unit = indicator_info['unit']
    
    # Determine color scheme based on indicator type
    color_scheme = determine_color_scheme(indicator_code)
    
    # Apply log transformation for better color differentiation if values span multiple orders of magnitude
    values = df_processed[color_column]
    use_log_scale = (values.max() / values.min()) > 1000 if values.min() > 0 else False
    
    if use_log_scale:
        df_processed = df_processed.copy()
        df_processed['LogValue'] = np.log10(df_processed[color_column])
        color_col = 'LogValue'
        scale_note = " (Log Scale)"
    else:
        color_col = color_column
        scale_note = ""
    
    # Create custom hover template
    hover_template = (
        '<b>%{text}</b><br>' +
        f'{indicator_name}: %{{customdata[0]:,.2f}} {unit}<br>' +
        'ISO Code: %{location}<br>' +
        f'Year: {year}<br>' +
        '<extra></extra>'
    )
    
    # Create the main choropleth trace
    choropleth_trace = go.Choropleth(
        locations=df_processed['ISO3'],
        z=df_processed[color_col],
        text=df_processed[hover_name_column],
        customdata=df_processed[[color_column]],  # Pass original values for hover
        hovertemplate=hover_template,
        colorscale=color_scheme,
        colorbar=dict(
            title=f"{indicator_name} {unit}{scale_note}",
            titleside="right",
            thickness=15,
            len=0.7,
            x=1.02
        ),
        marker_line_color='rgba(255,255,255,0.3)',
        marker_line_width=0.5
    )
    
    # Create the figure
    fig = go.Figure(data=[choropleth_trace])
    
    # Enhanced layout with better styling
    fig.update_layout(
        title={
            'text': f"🌍 {indicator_name} ({year}) 🗺️<br><sub>{unit}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#ffffff', 'family': 'Arial Black'}
        },
        geo=dict(
            projection_type='orthographic',
            projection_rotation=dict(lon=0, lat=20, roll=0),
            showland=True,
            landcolor='rgba(50, 50, 50, 0.8)',
            showocean=True,
            oceancolor='rgba(0, 20, 40, 0.9)',
            showlakes=True,
            lakecolor='rgba(0, 30, 60, 0.7)',
            showcountries=True,
            countrycolor='rgba(255, 255, 255, 0.2)',
            coastlinecolor='rgba(255, 255, 255, 0.4)',
            showframe=False,
            showcoastlines=True,
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        paper_bgcolor='rgba(10, 10, 20, 1)',
        plot_bgcolor='rgba(10, 10, 20, 1)',
        font=dict(color='white', family='Arial'),
        margin=dict(l=0, r=100, t=80, b=0),
        width=config.CHART_WIDTH,
        height=config.CHART_HEIGHT,
        annotations=[
            dict(
                text=f"Data Source: World Bank Open Data<br>" +
                     f"Interactive 3D Globe - Drag to rotate, scroll to zoom",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.02,
                xanchor="left", yanchor="bottom",
                font=dict(size=10, color="rgba(255,255,255,0.7)")
            )
        ]
    )
    
    return fig

def add_indicator_statistics(df: pd.DataFrame, indicator_code: str, year: str) -> None:
    """Prints comprehensive statistics for the indicator."""
    if df.empty:
        print("No data available for statistics")
        return
    
    indicator_info = get_indicator_info(indicator_code)
    indicator_name = indicator_info['name']
    unit = indicator_info['unit']
    
    print("\\n" + "="*80)
    print(f"📊 {indicator_name.upper()} - {year}")
    print("="*80)
    
    total_countries = len(df)
    mean_value = df['IndicatorValue'].mean()
    median_value = df['IndicatorValue'].median()
    std_value = df['IndicatorValue'].std()
    min_value = df['IndicatorValue'].min()
    max_value = df['IndicatorValue'].max()
    
    print(f"Total Countries with Data: {total_countries}")
    unit_str = unit if unit and str(unit) != 'nan' else ''
    print(f"Mean Value: {mean_value:,.2f} {unit_str}")
    print(f"Median Value: {median_value:,.2f} {unit_str}")
    print(f"Standard Deviation: {std_value:,.2f} {unit_str}")
    print(f"Range: {min_value:,.2f} - {max_value:,.2f} {unit_str}")
    
    print("\\n🏆 TOP 10 COUNTRIES:")
    print("-" * 50)
    top_10 = df.head(10)
    for i, (_, row) in enumerate(top_10.iterrows(), 1):
        print(f"{i:2d}. {row['CountryName']:<25} {row['IndicatorValue']:>12,.2f} {unit_str}")
    
    print("\\n📉 BOTTOM 10 COUNTRIES:")
    print("-" * 50)
    bottom_10 = df.tail(10)[::-1]  # Reverse to show lowest first
    for i, (_, row) in enumerate(bottom_10.iterrows(), 1):
        print(f"{i:2d}. {row['CountryName']:<25} {row['IndicatorValue']:>12,.2f} {unit_str}")
    
    print("\\n📈 DISTRIBUTION:")
    print("-" * 30)
    quartiles = df['IndicatorValue'].quantile([0.25, 0.5, 0.75])
    print(f"25th Percentile: {quartiles[0.25]:,.2f} {unit_str}")
    print(f"50th Percentile: {quartiles[0.5]:,.2f} {unit_str}")
    print(f"75th Percentile: {quartiles[0.75]:,.2f} {unit_str}")
    print("="*80 + "\\n")

def create_time_series_visualization(indicator_code: str, years: List[str], country_limit: int = 20) -> Optional[go.Figure]:
    """Create a time series visualization showing top countries over multiple years."""
    
    from process_wb_data import process_indicator_for_year
    
    print(f"\\nCreating time series visualization for {indicator_code}...")
    
    # Collect data for all years
    all_data = []
    for year in years:
        df = process_indicator_for_year(indicator_code, year)
        if df is not None:
            df['Year'] = int(year)
            all_data.append(df)
    
    if not all_data:
        print("No data available for time series")
        return None
    
    # Combine all years
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Get top countries by latest year average
    latest_year = max(years)
    latest_df = process_indicator_for_year(indicator_code, latest_year)
    if latest_df is None:
        return None
    
    top_countries = latest_df.head(country_limit)['ISO3'].tolist()
    
    # Filter for top countries only
    time_series_df = combined_df[combined_df['ISO3'].isin(top_countries)]
    
    # Create line plot
    fig = px.line(
        time_series_df, 
        x='Year', 
        y='IndicatorValue',
        color='CountryName',
        title=f"Time Series: {get_indicator_info(indicator_code)['name']}",
        hover_data=['ISO3']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(10, 10, 20, 1)',
        paper_bgcolor='rgba(10, 10, 20, 1)',
        font=dict(color='white'),
        width=config.CHART_WIDTH,
        height=600
    )
    
    return fig

def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description="Generate 3D globe visualizations for World Bank indicators")
    parser.add_argument("--indicator", type=str, required=True,
                       help="World Bank indicator code (e.g., NY.GDP.PCAP.CD)")
    parser.add_argument("--year", type=str, default=config.DEFAULT_YEAR,
                       help="Year to visualize (default: 2023)")
    parser.add_argument("--time-series", action="store_true",
                       help="Create time series visualization")
    parser.add_argument("--years", type=str, nargs='+', 
                       default=[str(y) for y in range(2018, 2024)],
                       help="Years for time series (default: 2018-2023)")
    
    args = parser.parse_args()
    
    print(f"--- Starting 3D Globe Visualization ---")
    print(f"Indicator: {args.indicator}")
    print(f"Year: {args.year}")
    
    # Import here to avoid circular imports
    from process_wb_data import process_indicator_for_year
    
    # Load and process data
    df = process_indicator_for_year(args.indicator, args.year)
    
    if df is None or df.empty:
        print(f"No data available for {args.indicator} in {args.year}")
        return
    
    # Create and show 3D globe
    print("Creating 3D globe visualization...")
    fig = create_enhanced_3d_globe(df, args.indicator, args.year)
    
    if fig:
        print("Displaying 3D Globe...")
        fig.show()
        
        # Show statistics
        add_indicator_statistics(df, args.indicator, args.year)
    
    # Create time series if requested
    if args.time_series:
        print("Creating time series visualization...")
        ts_fig = create_time_series_visualization(args.indicator, args.years)
        if ts_fig:
            print("Displaying time series...")
            ts_fig.show()
    
    print(f"\\n--- Visualization Complete ---")

if __name__ == '__main__':
    main()
