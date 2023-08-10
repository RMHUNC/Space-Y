# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
# dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                     {'label': 'All Sites', 'value': 'ALL'},
                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                        ],
                value='ALL',
                placeholder="Select Launch Site",
                searchable=True)],

            html.Br(),

            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P("Payload range (Kg):"),

            dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000',
                4000: '4000', 5000: '5000', 6000:'6000', 7000:'7000',
                8000:'8000', 9000:'9000', 10000:'10000'},
                value=[min_value, max_value]),
            

            html.Div(dcc.Graph(id='success-payload-scatter-chart')),
            html.Br()            

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='fig'),
    Input(component_id='site-dropdown', component_property='value'))

def build_graph(site-dropdown):
    if site-dropdown == 'ALL':
        fig = px.pie(data_frame= spacex.df, values='class', 
        names='Launch Site', 
        title='Total Launches from All Sites'),
        return fig
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site-dropdown]
        piechart = px.pie(data_frame = specific_df, names='Launch Site', values='class',
        title='Total Launch for', & '[site-dropdown]'),
        return piechart

# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
# TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'),
              Output(component_id='success-payload-scatter-chart', component_property='figure))
# TASK 4: Add a scatter chart to show the correlation between payload and launch success
def update_graph(site-dropdown, payload-slider):
    if entered_site == 'ALL':
        data=spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatter = px.scatter(data_frame= data, y='class', x='Payload Mass (kg)', color='Booster Version'),
        title='Payload Mass by Success of Launch')
        return scatter
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        data=specific_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatter= px.scatter(data_frame=data, x='Payload Mass (kg)'), y='class',
        color='Booster Version')
        return scatter

            

# Run the app
if __name__ == '__main__':
    app.run_server()
