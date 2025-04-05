import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import datetime
import numpy as np

# Sample station data
stations_data = {
    'Station': ['Mumbai', 'Delhi', 'Kolkata', 'Chennai', 'Ahmedabad'],
    'Latitude': [19.0760, 28.6139, 22.5726, 13.0827, 23.0225],
    'Longitude': [72.8777, 77.2090, 88.3639, 80.2707, 72.5714]
}

stations_df = pd.DataFrame(stations_data)

# Generate fake fuel consumption data
def generate_fuel_data(station):
    dates = pd.date_range(start='2024-01-01', periods=90)
    fuel_values = np.random.randint(1000, 3000, size=len(dates))
    return pd.DataFrame({'Date': dates, 'Fuel_Consumption': fuel_values})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("HPCL Fuel Demand Visualization Dashboard", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='station-dropdown',
        options=[{'label': city, 'value': city} for city in stations_df['Station']],
        value='Mumbai',
        clearable=False
    ),

    dcc.Graph(id='fuel-graph'),
    dcc.Graph(id='map-graph')
])

@app.callback(
    Output('fuel-graph', 'figure'),
    Output('map-graph', 'figure'),
    Input('station-dropdown', 'value')
)
def update_dashboard(selected_station):
    # Fuel Forecast
    df = generate_fuel_data(selected_station)
    fuel_fig = px.line(df, x='Date', y='Fuel_Consumption', title=f'Fuel Consumption Forecast - {selected_station}')

    # Map Display
    map_fig = px.scatter_geo(
        stations_df,
        lat='Latitude',
        lon='Longitude',
        text='Station',
        title='HPCL Fuel Stations in India'
    )
    map_fig.update_layout(geo_scope='asia', height=500)

    return fuel_fig, map_fig

if __name__ == '__main__':
    app.run_server(debug=True)
