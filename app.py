import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import pandas as pd
import os
from typing import List, Dict, Optional

# Import our custom modules
import config
from wb_globe import create_enhanced_3d_globe, add_indicator_statistics
from process_wb_data import (
    process_indicator_for_year, 
    get_indicator_info, 
    get_available_years_for_indicator
)

# Ensure data directory exists
if not os.path.exists(config.DATA_DIR):
    os.makedirs(config.DATA_DIR)

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment

# Load available indicators
def get_available_indicators() -> List[Dict[str, str]]:
    """Get list of available indicators from the WDI series file."""
    try:
        series_df = pd.read_csv(config.WDI_SERIES_FILE)
        indicators = []
        
        # Add popular indicators first
        for name, code in config.POPULAR_INDICATORS.items():
            indicators.append({'label': f"⭐ {name}", 'value': code})
        
        # Add separator
        indicators.append({'label': '--- All Indicators ---', 'value': '', 'disabled': True})
        
        # Add all other indicators
        for _, row in series_df.iterrows():
            code = row['Series Code']
            name = row['Indicator Name']
            if code not in config.POPULAR_INDICATORS.values():
                # Truncate long names
                if len(name) > 80:
                    name = name[:77] + "..."
                indicators.append({'label': f"{name} ({code})", 'value': code})
        
        return indicators
    except Exception as e:
        print(f"Error loading indicators: {e}")
        # Fallback to popular indicators only
        return [{'label': name, 'value': code} for name, code in config.POPULAR_INDICATORS.items()]

# Get indicator options
INDICATOR_OPTIONS = get_available_indicators()

# Define year range
YEARS = [str(year) for year in config.DEFAULT_YEARS_RANGE]

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("🌍 World Bank Indicators 3D Visualization", 
                style={'textAlign': 'center', 'color': '#ffffff', 'marginBottom': '30px'}),
        
        html.P("Explore World Bank development indicators in stunning 3D visualizations", 
               style={'textAlign': 'center', 'color': '#cccccc', 'fontSize': '16px'})
    ], style={'backgroundColor': '#0a0a14', 'padding': '20px', 'marginBottom': '20px'}),

    # Control panel
    html.Div([
        html.Div([
            html.Label("Select Indicator:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=INDICATOR_OPTIONS,
                value=config.POPULAR_INDICATORS["GDP per capita"],  # Default
                placeholder="Choose an indicator...",
                style={'marginBottom': '10px'}
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'marginRight': '5%', 'verticalAlign': 'top'}),

        html.Div([
            html.Label("Select Year:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in YEARS],
                value=config.DEFAULT_YEAR,
                style={'marginBottom': '10px'}
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'marginRight': '5%', 'verticalAlign': 'top'}),

        html.Div([
            html.Label("Visualization Options:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Checklist(
                id='viz-options',
                options=[
                    {'label': ' Show Statistics', 'value': 'stats'},
                    {'label': ' Auto-rotate Globe', 'value': 'rotate'}
                ],
                value=['stats'],
                style={'marginTop': '10px'}
            )
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    ], style={'marginBottom': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),

    # Action buttons
    html.Div([
        html.Button('🌍 Generate Globe', id='generate-button', n_clicks=0, 
                   style={
                       'backgroundColor': '#007bff', 'color': 'white', 'border': 'none',
                       'padding': '12px 24px', 'fontSize': '16px', 'borderRadius': '5px',
                       'marginRight': '10px', 'cursor': 'pointer'
                   }),
        html.Button('📊 Show Available Years', id='years-button', n_clicks=0,
                   style={
                       'backgroundColor': '#28a745', 'color': 'white', 'border': 'none',
                       'padding': '12px 24px', 'fontSize': '16px', 'borderRadius': '5px',
                       'marginRight': '10px', 'cursor': 'pointer'
                   }),
        html.Button('ℹ️ Indicator Info', id='info-button', n_clicks=0,
                   style={
                       'backgroundColor': '#17a2b8', 'color': 'white', 'border': 'none',
                       'padding': '12px 24px', 'fontSize': '16px', 'borderRadius': '5px',
                       'cursor': 'pointer'
                   }),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Status messages
    html.Div(id='status-message', style={
        'textAlign': 'center', 'minHeight': '50px', 'padding': '10px',
        'backgroundColor': '#e9ecef', 'borderRadius': '5px', 'marginBottom': '20px'
    }),

    # Main visualization
    dcc.Graph(id='wb-globe-graph', style={'height': '800px'}),

    # Additional info panel
    html.Div(id='info-panel', style={
        'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 
        'borderRadius': '5px', 'minHeight': '100px'
    }),

    # Footer
    html.Div([
        html.Hr(),
        html.P([
            "Data Source: ",
            html.A("World Bank Open Data", href="https://data.worldbank.org/", target="_blank"),
            " | Built with ",
            html.A("Plotly Dash", href="https://dash.plotly.com/", target="_blank")
        ], style={'textAlign': 'center', 'color': '#666', 'fontSize': '12px'})
    ], style={'marginTop': '40px'})

], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px'})

# Callback for the main globe generation
@app.callback(
    [Output('wb-globe-graph', 'figure'),
     Output('status-message', 'children'),
     Output('info-panel', 'children')],
    [Input('generate-button', 'n_clicks')],
    [State('indicator-dropdown', 'value'),
     State('year-dropdown', 'value'),
     State('viz-options', 'value')]
)
def update_globe(n_clicks, selected_indicator, selected_year, viz_options):
    """Update the 3D globe visualization."""
    if n_clicks == 0:
        return {}, "👆 Select an indicator and year, then click 'Generate Globe' to start exploring!", ""

    if not selected_indicator:
        return {}, "⚠️ Please select an indicator first.", ""

    status_messages = []
    info_content = []
    
    try:
        status_messages.append(f"🔄 Processing {selected_indicator} for year {selected_year}...")
        
        # Get indicator info
        indicator_info = get_indicator_info(selected_indicator)
        indicator_name = indicator_info['name']
        
        # Process data
        df = process_indicator_for_year(selected_indicator, selected_year)
        
        if df is None or df.empty:
            status_messages.append(f"❌ No data available for {indicator_name} in {selected_year}")
            return {}, html.Ul([html.Li(msg) for msg in status_messages]), ""
        
        # Create the globe
        fig = create_enhanced_3d_globe(df, selected_indicator, selected_year)
        
        if fig:
            status_messages.append(f"✅ Successfully generated globe with data for {len(df)} countries")
            
            # Add rotation if requested
            if 'rotate' in (viz_options or []):
                fig.update_layout(
                    updatemenus=[{
                        'type': 'buttons',
                        'showactive': False,
                        'buttons': [{
                            'label': 'Rotate',
                            'method': 'animate',
                            'args': [None, {
                                'frame': {'duration': 100, 'redraw': True},
                                'transition': {'duration': 0},
                                'fromcurrent': True,
                                'mode': 'immediate'
                            }]
                        }]
                    }]
                )
            
            # Prepare info panel
            info_content = [
                html.H4(f"📊 {indicator_name}", style={'color': '#007bff'}),
                html.P(f"📅 Year: {selected_year}"),
                html.P(f"🌍 Countries with data: {len(df)}"),
                html.P(f"🏆 Top performer: {df.iloc[0]['CountryName']} ({df.iloc[0]['IndicatorValue']:,.2f})"),
                html.P(f"📈 Average: {df['IndicatorValue'].mean():,.2f}"),
            ]
            
            # Add unit if available
            if indicator_info['unit']:
                info_content.append(html.P(f"📏 Unit: {indicator_info['unit']}"))
            
            # Add definition if available
            if indicator_info['definition']:
                info_content.append(html.P(f"ℹ️ Definition: {indicator_info['definition'][:200]}..."))
        else:
            status_messages.append("❌ Failed to generate visualization")
            return {}, html.Ul([html.Li(msg) for msg in status_messages]), ""
            
    except Exception as e:
        status_messages.append(f"❌ Error: {str(e)}")
        return {}, html.Ul([html.Li(msg) for msg in status_messages]), ""

    return fig, html.Ul([html.Li(msg) for msg in status_messages]), info_content

# Callback for showing available years
@app.callback(
    Output('status-message', 'children', allow_duplicate=True),
    [Input('years-button', 'n_clicks')],
    [State('indicator-dropdown', 'value')],
    prevent_initial_call=True
)
def show_available_years(n_clicks, selected_indicator):
    """Show available years for the selected indicator."""
    if n_clicks == 0 or not selected_indicator:
        return "Please select an indicator first."
    
    try:
        years = get_available_years_for_indicator(selected_indicator)
        if years:
            years_text = ", ".join(years[-10:])  # Show last 10 years
            if len(years) > 10:
                years_text = f"...{years_text}"
            return f"📅 Available years for this indicator: {years_text} (showing recent years)"
        else:
            return "❌ No years with data found for this indicator"
    except Exception as e:
        return f"❌ Error retrieving years: {str(e)}"

# Callback for showing indicator info
@app.callback(
    Output('info-panel', 'children', allow_duplicate=True),
    [Input('info-button', 'n_clicks')],
    [State('indicator-dropdown', 'value')],
    prevent_initial_call=True
)
def show_indicator_info(n_clicks, selected_indicator):
    """Show detailed information about the selected indicator."""
    if n_clicks == 0 or not selected_indicator:
        return "Please select an indicator first."
    
    try:
        info = get_indicator_info(selected_indicator)
        
        content = [
            html.H4(f"📊 {info['name']}", style={'color': '#007bff'}),
            html.P(f"🔢 Code: {selected_indicator}"),
        ]
        
        if info['topic']:
            content.append(html.P(f"🏷️ Topic: {info['topic']}"))
        
        if info['unit']:
            content.append(html.P(f"📏 Unit: {info['unit']}"))
        
        if info['definition']:
            content.append(html.P(f"ℹ️ Definition: {info['definition']}"))
        
        return content
    
    except Exception as e:
        return f"❌ Error retrieving indicator info: {str(e)}"

# Run the app
if __name__ == '__main__':
    print("🌍 Starting World Bank Indicators 3D Visualization...")
    print("📱 Open your web browser and navigate to: http://127.0.0.1:8050/")
    print("🚀 Loading application...")
    
    app.run_server(debug=True, host='127.0.0.1', port=8050)
