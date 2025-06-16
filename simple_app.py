"""
Simple Dash app to test the World Bank 3D visualization
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import os

# Import our custom modules
import config
from wb_globe import create_enhanced_3d_globe
from process_wb_data import process_indicator_for_year, get_indicator_info

# Initialize Dash app
app = dash.Dash(__name__)

# Simple layout for testing
app.layout = html.Div([
    html.H1("🌍 World Bank 3D Visualization", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select Indicator:"),
        dcc.Dropdown(
            id='indicator-dropdown',            options=[
                {'label': 'GDP per capita', 'value': 'NY.GDP.PCAP.CD'},
                {'label': 'Life expectancy', 'value': 'SP.DYN.LE00.IN'},
                {'label': 'CO2 emissions per capita', 'value': 'EN.GHG.CO2.PC.CE.AR5'},
                {'label': 'Population total', 'value': 'SP.POP.TOTL'},
                {'label': 'Access to electricity', 'value': 'EG.ELC.ACCS.ZS'},
            ],
            value='NY.GDP.PCAP.CD'
        ),
        
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': str(year)} for year in range(2018, 2025)],
            value='2023'
        ),
        
        html.Button('Generate Globe', id='submit-button', n_clicks=0),
    ], style={'width': '50%', 'margin': '20px auto'}),
    
    html.Div(id='status-message', style={'textAlign': 'center', 'margin': '20px'}),
    
    dcc.Graph(id='globe-graph', style={'height': '600px'})
])

@app.callback(
    [Output('globe-graph', 'figure'),
     Output('status-message', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('indicator-dropdown', 'value'),
     State('year-dropdown', 'value')]
)
def update_globe(n_clicks, indicator, year):
    if n_clicks == 0:
        return {}, "Select an indicator and year, then click 'Generate Globe'"
    
    try:
        # Process data
        df = process_indicator_for_year(indicator, year)
        
        if df is None or df.empty:
            return {}, f"No data available for {indicator} in {year}"
        
        # Create globe
        fig = create_enhanced_3d_globe(df, indicator, year)
        
        # Get indicator info
        info = get_indicator_info(indicator)
        
        return fig, f"✅ Generated globe for {info['name']} ({year}) with {len(df)} countries"
        
    except Exception as e:
        return {}, f"❌ Error: {str(e)}"

if __name__ == '__main__':
    print("🌍 Starting World Bank 3D Visualization (Simple Version)...")
    print("📱 Open your browser and go to: http://127.0.0.1:8051/")
    
    app.run(debug=True, port=8051)
