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
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
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
                searchable=True),

            html.Br(),

            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P("Payload range (Kg):"),
# TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)
            dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000',
                4000: '4000', 5000: '5000', 6000:'6000', 7000:'7000',
                8000:'8000', 9000:'9000', 10000:'10000'},
                value=[min_payload, max_payload]),
            

            html.Div(dcc.Graph(id='success-payload-scatter-chart')),
            html.Br()])           

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')])
# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
def update_graph(site_dropdown):
        if site_dropdown == 'ALL':
            filtered_df=spacex_df
            #filtered_df=spacex_df.loc[spacex_df['class'] == 1]
            figure = px.pie(data_frame= filtered_df, values='class',names='Launch Site', title=f'Total Launches from All Sites')
            return figure
        else:
            specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
            figure = px.pie(data_frame= specific_df, names='class', values=specific_df.value_counts().values, title=f'Total Launch for {site_dropdown}')
            return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
             Input(component_id='payload-slider', component_property='value')])

# TASK 4: Add a scatter chart to show the correlation between payload and launch success
def get_scatter_plot(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        data=spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        figure = px.scatter(data_frame= data, y='class', x='Payload Mass (kg)', color='Booster Version Category',
        title='Payload Mass by Success of Launch')
        return figure
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        data=specific_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        figure= px.scatter(data_frame=data, x='Payload Mass (kg)', y='class',
        color='Booster Version Category')
        return figure

            

# Run the app
if __name__ == '__main__':
    app.run_server()
