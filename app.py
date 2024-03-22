# import dependencies
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# load the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize the app
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

###DATA MANAGAMENT###
# read in data (data can be found in course folder)
df = pd.read_csv('gdp_pcap.csv')

# Get unique countries for dropdown options
countries = [{'label': country, 'value': country} for country in df['country'].unique()]

# Define fixed values for the slider [UNUSED]
# years = list(range(1800, 2100 + 1))

# Set the index to 'country'
df.set_index('country', inplace=True)

# Function to convert values with 'k'
def convert_with_k(value):
    if 'k' in str(value):  # Ensure value is converted to string before checking for 'k'
        return float(str(value).replace('k', '')) * 1000
    else:
        return float(value)

# Apply the function to each cell in the DataFrame
df = df.applymap(convert_with_k)

# Create line plot using plotly.express
fig = px.line(df.transpose(), x=df.columns, y=df.index, title='Population Over Time by Country')

# Update axis labels
fig.update_layout(xaxis_title='Year', yaxis_title='Population')

# Update line plot using plotly.express when callback is being used
def update_graph(selected_countries, selected_years):
    filtered_df = df.loc[selected_countries, str(selected_years[0]):str(selected_years[1])]
    fig = px.line(filtered_df.transpose(), x=filtered_df.columns, y=filtered_df.index, title='Population Over Time by Country')
    fig.update_layout(xaxis_title='Year', yaxis_title='Population')
    return fig

###LAYOUT###
app.layout = html.Div(children=[
    html.H1(children="GDP Data - Assignment 4"),
    html.Div(children="This application computes data analytics on GDP data. It takes into account of the GDP per country specified in the data set. Other features, like the dropdown and slider, can be messed with, but do not affect the graph in any way whatsoever."),
    
    # Dropdown for country selection
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=countries,
            multi=True,
            value=[],
            placeholder="Select country"
        ),
    ], style={'width': '49%', 'display': 'inline-block'}),
    
    # Slider for year selection
    html.Div([
        dcc.RangeSlider(
            id='year-slider',
            min=int(min(df.columns)),
            max=int(max(df.columns)),
            value=[int(min(df.columns)), int(max(df.columns))],
            marks={str(year): str(year) if year % 50 == 0 else '' for year in range(int(min(df.columns)), int(max(df.columns)) + 1)},
            tooltip={"placement": "bottom", "always_visible": True},
            step=1
        )
    ], style={'width': '49%', 'display': 'inline-block'}),
    
    # Graph
    dcc.Graph(id='population-graph', figure=fig),
])

# Define callback for updating the graph
@app.callback(
    Output('population-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph_callback(selected_countries, selected_years):
    return update_graph(selected_countries, selected_years)

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
