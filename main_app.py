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

# Define recent years for quick access
RECENT_YEARS = [str(year) for year in range(2018, 2025)]
ALL_YEARS = [str(year) for year in range(2000, 2025)]

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌍 World Bank Development Indicators", 
                style={'textAlign': 'center', 'color': '#ffffff', 'marginBottom': '10px', 'fontSize': '2.5em'}),
        
        html.P("Explore the world's development data through stunning 3D visualizations", 
               style={'textAlign': 'center', 'color': '#e0e0e0', 'fontSize': '1.2em', 'marginBottom': '5px'}),
        
        html.P("Select from 20 most popular indicators and visualize global patterns", 
               style={'textAlign': 'center', 'color': '#cccccc', 'fontSize': '1em'})
    ], style={
        'backgroundColor': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '30px', 
        'marginBottom': '30px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),

    # Control panel
    html.Div([
        # Indicator selection
        html.Div([
            html.Label("📊 Select Development Indicator:", 
                      style={'fontWeight': 'bold', 'marginBottom': '10px', 'fontSize': '1.1em', 'color': '#333'}),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=[{'label': f"🔹 {name}", 'value': code} for name, code in config.POPULAR_INDICATORS.items()],
                value=list(config.POPULAR_INDICATORS.values())[0],  # GDP per capita as default
                placeholder="Choose an indicator to visualize...",
                style={'fontSize': '14px'},
                clearable=False
            ),
        ], style={
            'width': '60%', 
            'display': 'inline-block', 
            'marginRight': '3%', 
            'verticalAlign': 'top',
            'padding': '15px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }),

        # Year selection
        html.Div([
            html.Label("📅 Select Year:", 
                      style={'fontWeight': 'bold', 'marginBottom': '10px', 'fontSize': '1.1em', 'color': '#333'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': '--- Recent Years ---', 'value': '', 'disabled': True},
                    *[{'label': f"🕐 {year}", 'value': year} for year in reversed(RECENT_YEARS)],
                    {'label': '--- All Years ---', 'value': '', 'disabled': True},
                    *[{'label': year, 'value': year} for year in reversed(ALL_YEARS[:-7])]  # Exclude recent years already shown
                ],
                value="2023",
                style={'fontSize': '14px'},
                clearable=False
            ),
            
            html.Div([
                html.Small("💡 Tip: Recent years typically have better data coverage", 
                          style={'color': '#666', 'fontStyle': 'italic'})
            ], style={'marginTop': '8px'})
        ], style={
            'width': '34%', 
            'display': 'inline-block', 
            'verticalAlign': 'top',
            'padding': '15px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }),
    ], style={'marginBottom': '25px'}),

    # Action buttons
    html.Div([
        html.Button(
            '🌍 Generate 3D Globe', 
            id='generate-button', 
            n_clicks=0, 
            style={
                'backgroundColor': '#28a745', 
                'color': 'white', 
                'border': 'none',
                'padding': '15px 30px', 
                'fontSize': '18px', 
                'fontWeight': 'bold',
                'borderRadius': '8px',
                'marginRight': '15px', 
                'cursor': 'pointer',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.2)',
                'transition': 'all 0.3s ease'
            }
        ),
        html.Button(
            '📈 Show Available Years', 
            id='years-button', 
            n_clicks=0,
            style={
                'backgroundColor': '#17a2b8', 
                'color': 'white', 
                'border': 'none',
                'padding': '15px 30px', 
                'fontSize': '16px', 
                'borderRadius': '8px',
                'marginRight': '15px', 
                'cursor': 'pointer',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
            }
        ),
        html.Button(
            'ℹ️ Indicator Details', 
            id='info-button', 
            n_clicks=0,
            style={
                'backgroundColor': '#6f42c1', 
                'color': 'white', 
                'border': 'none',
                'padding': '15px 30px', 
                'fontSize': '16px', 
                'borderRadius': '8px',
                'cursor': 'pointer',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
            }
        ),
    ], style={'textAlign': 'center', 'marginBottom': '25px'}),

    # Status messages
    html.Div(id='status-message', style={
        'textAlign': 'center', 
        'minHeight': '60px', 
        'padding': '15px',
        'backgroundColor': '#e9ecef', 
        'borderRadius': '8px', 
        'marginBottom': '25px',
        'fontSize': '16px',
        'border': '1px solid #dee2e6'
    }),

    # Main visualization
    html.Div([
        dcc.Graph(id='wb-globe-graph', style={'height': '700px'})
    ], style={
        'backgroundColor': '#ffffff',
        'borderRadius': '10px',
        'padding': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),

    # Information panel
    html.Div(id='info-panel', style={
        'marginTop': '25px', 
        'padding': '20px', 
        'backgroundColor': '#f8f9fa', 
        'borderRadius': '8px', 
        'minHeight': '80px',
        'border': '1px solid #dee2e6'
    }),

    # Quick stats panel
    html.Div(id='stats-panel', style={
        'marginTop': '15px', 
        'padding': '20px', 
        'backgroundColor': '#ffffff', 
        'borderRadius': '8px', 
        'minHeight': '60px',
        'border': '1px solid #dee2e6',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
    }),

    # Footer
    html.Div([
        html.Hr(style={'margin': '40px 0 20px 0'}),
        html.Div([
            html.P([
                "📊 Data Source: ",
                html.A("World Bank Open Data", href="https://data.worldbank.org/", target="_blank", 
                      style={'color': '#007bff', 'textDecoration': 'none'}),
                " | 🛠️ Built with ",
                html.A("Plotly Dash", href="https://dash.plotly.com/", target="_blank",
                      style={'color': '#007bff', 'textDecoration': 'none'}),
                " | 🌟 Top 20 Development Indicators"
            ], style={'textAlign': 'center', 'color': '#666', 'fontSize': '14px', 'marginBottom': '10px'}),
            
            html.P([
                "💡 Tip: Hover over countries for detailed data, drag to rotate globe, scroll to zoom"
            ], style={'textAlign': 'center', 'color': '#888', 'fontSize': '12px'})
        ])
    ], style={'marginTop': '40px'})

], style={
    'maxWidth': '1400px', 
    'margin': '0 auto', 
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif'
})

# Callback for the main globe generation
@app.callback(
    [Output('wb-globe-graph', 'figure'),
     Output('status-message', 'children'),
     Output('info-panel', 'children'),
     Output('stats-panel', 'children')],
    [Input('generate-button', 'n_clicks')],
    [State('indicator-dropdown', 'value'),
     State('year-dropdown', 'value')]
)
def update_globe(n_clicks, selected_indicator, selected_year):
    """Update the 3D globe visualization."""
    if n_clicks == 0:
        return (
            {}, 
            "👆 Select an indicator and year above, then click 'Generate 3D Globe' to explore global development patterns!",
            html.Div([
                html.H4("🌟 Welcome to World Bank 3D Visualizations!", style={'color': '#007bff', 'marginBottom': '15px'}),
                html.P("This tool lets you explore 20 of the most important development indicators in stunning 3D:"),
                html.Ul([
                    html.Li("💰 Economic indicators (GDP, trade, investment)"),
                    html.Li("👥 Social indicators (population, health, education)"),
                    html.Li("🌱 Environmental indicators (emissions, energy, forests)"),
                    html.Li("📱 Technology indicators (internet, mobile access)")
                ], style={'textAlign': 'left', 'display': 'inline-block'}),
                html.P("Select any indicator and year to get started!", style={'marginTop': '15px'})
            ], style={'textAlign': 'center'}),
            ""
        )

    if not selected_indicator:
        return {}, "⚠️ Please select an indicator first.", "", ""

    status_messages = []
    info_content = []
    stats_content = []
    
    try:
        # Get indicator name for display
        indicator_name = None
        for name, code in config.POPULAR_INDICATORS.items():
            if code == selected_indicator:
                indicator_name = name
                break
        
        if not indicator_name:
            indicator_name = selected_indicator
        
        status_messages.append(f"🔄 Processing {indicator_name} for year {selected_year}...")
        
        # Get indicator info
        indicator_info = get_indicator_info(selected_indicator)
        
        # Process data
        df = process_indicator_for_year(selected_indicator, selected_year)
        
        if df is None or df.empty:
            status_messages.append(f"❌ No data available for {indicator_name} in {selected_year}")
            
            # Try to suggest alternative years
            available_years = get_available_years_for_indicator(selected_indicator)
            if available_years:
                recent_years = [y for y in available_years if int(y) >= 2015][-5:]
                suggestion = f"💡 Try these recent years with data: {', '.join(recent_years)}"
                status_messages.append(suggestion)
            
            return {}, html.Div([html.P(msg) for msg in status_messages]), "", ""
        
        # Create the globe
        fig = create_enhanced_3d_globe(df, selected_indicator, selected_year)
        
        if fig:
            status_messages.append(f"✅ Successfully generated globe with data for {len(df)} countries!")
            
            # Prepare info panel content
            info_content = [
                html.H4(f"📊 {indicator_name}", style={'color': '#007bff', 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.P(f"📅 Year: {selected_year}", style={'margin': '5px 0'}),
                        html.P(f"🌍 Countries with data: {len(df)}", style={'margin': '5px 0'}),
                        html.P(f"🔢 Indicator code: {selected_indicator}", style={'margin': '5px 0', 'fontSize': '12px', 'color': '#666'}),
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                    
                    html.Div([
                        html.P(f"🏆 Top performer: {df.iloc[0]['CountryName']}", style={'margin': '5px 0'}),
                        html.P(f"📈 Average value: {df['IndicatorValue'].mean():,.2f}", style={'margin': '5px 0'}),
                        html.P(f"📏 Range: {df['IndicatorValue'].min():,.0f} - {df['IndicatorValue'].max():,.0f}", style={'margin': '5px 0'}),
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'}),
                ]),
            ]
              # Add unit and definition if available
            if indicator_info.get('unit') and str(indicator_info['unit']).strip() and str(indicator_info['unit']) != 'nan':
                info_content.append(html.P(f"📏 Unit: {indicator_info['unit']}", style={'margin': '10px 0 5px 0'}))
            
            if indicator_info.get('definition') and isinstance(indicator_info['definition'], str) and len(indicator_info['definition'].strip()) > 10:
                definition = indicator_info['definition']
                if len(definition) > 300:
                    definition = definition[:300] + "..."
                info_content.append(html.P(f"ℹ️ {definition}", style={'margin': '10px 0', 'fontSize': '14px', 'lineHeight': '1.5'}))
            
            # Prepare stats panel
            top_5 = df.head(5)
            stats_content = [
                html.H5("🏆 Top 5 Countries", style={'color': '#28a745', 'marginBottom': '10px'}),
                html.Div([
                    html.Div([
                        html.P(f"{i}. {row['CountryName']}", style={'margin': '2px 0', 'fontWeight': 'bold'}),
                        html.P(f"   {row['IndicatorValue']:,.2f}", style={'margin': '2px 0', 'fontSize': '14px', 'color': '#666'})
                    ]) for i, (_, row) in enumerate(top_5.iterrows(), 1)
                ], style={'columnCount': '2', 'columnGap': '20px'})
            ]
        else:
            status_messages.append("❌ Failed to generate visualization")
            return {}, html.Div([html.P(msg) for msg in status_messages]), "", ""
            
    except Exception as e:
        status_messages.append(f"❌ Error: {str(e)}")
        return {}, html.Div([html.P(msg) for msg in status_messages]), "", ""

    return fig, html.Div([html.P(msg) for msg in status_messages]), info_content, stats_content

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
            # Show recent years and total count
            recent_years = [y for y in years if int(y) >= 2015]
            years_text = ", ".join(recent_years[-8:]) if recent_years else ", ".join(years[-8:])
            
            return html.Div([
                html.P(f"📅 Available years for this indicator: {len(years)} total years"),
                html.P(f"🕐 Recent years (2015+): {years_text}"),
                html.P(f"📊 Full range: {years[0]} - {years[-1]}", style={'fontSize': '14px', 'color': '#666'})
            ])
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
          # Get the friendly name
        indicator_name = None
        for name, code in config.POPULAR_INDICATORS.items():
            if code == selected_indicator:
                indicator_name = name
                break
        
        content = [
            html.H4(f"📊 {indicator_name or info['name']}", style={'color': '#007bff', 'marginBottom': '15px'}),
            html.P(f"🔢 Code: {selected_indicator}", style={'fontFamily': 'monospace', 'backgroundColor': '#f8f9fa', 'padding': '5px', 'borderRadius': '3px'}),
        ]
        
        if info.get('topic'):
            content.append(html.P(f"🏷️ Category: {info['topic']}", style={'margin': '10px 0'}))
        
        if info.get('unit') and str(info['unit']).strip() and str(info['unit']) != 'nan':
            content.append(html.P(f"📏 Unit of measurement: {info['unit']}", style={'margin': '10px 0'}))
        
        if info.get('definition') and isinstance(info['definition'], str) and len(info['definition'].strip()) > 10:
            content.append(html.Div([
                html.P("ℹ️ Definition:", style={'fontWeight': 'bold', 'margin': '15px 0 5px 0'}),
                html.P(info['definition'], style={'lineHeight': '1.6', 'textAlign': 'justify'})
            ]))
        
        return content
    
    except Exception as e:
        return f"❌ Error retrieving indicator info: {str(e)}"

# Run the app
if __name__ == '__main__':
    print("🌍 Starting World Bank Development Indicators 3D Visualization...")
    print("📊 Featuring 20 most popular development indicators")
    print("📱 Open your web browser and navigate to: http://127.0.0.1:8050/")
    print("🚀 Loading application...")
    
    app.run(debug=True, host='127.0.0.1', port=8050)
