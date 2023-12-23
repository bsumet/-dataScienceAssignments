# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print("SITES: ", spacex_df['Launch Site'].unique().tolist())
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                   options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique().tolist()],
                                    ],
                                    value='All',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value=[0, 10000]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    data = spacex_df 
    # print("ENTER SITE", entered_site.upper())
    # print('Type:', type(entered_site.upper()))
    # print('IS IT TRUE', entered_site.upper() == "ALL")
    # print('Type:', type("ALL"))
    # print('Length of entered_site:', len(entered_site))
    # print('Length of ALL:', len('ALL'))
    # print('entered_site in hex:', entered_site.upper().encode('utf-8').hex())
    # print('ALL in hex:', 'ALL'.encode('utf-8').hex())
    if entered_site.upper() == 'ALL': 
        fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else: 
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        failure_count = filtered_df[filtered_df['class'] == 0].shape[0]
    
        data = pd.DataFrame({
            'Status':['1', '0'],
            'Count': [success_count, failure_count]
            })
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(data, values='Count', names='Status', title='Total Success Launches by Site {}'.format(entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, slider_val):
    print("SLIDER VAL ", slider_val)
    print("SLIDER VAL 0 ", slider_val[0])
    print("SLIDER VAL 0 TYPE ", type(slider_val[0]))
    print("SLIDER VAL 1 ", slider_val[1])
    print("DATA TYPEs ", spacex_df.dtypes)
    
    data = spacex_df[(spacex_df['Payload Mass (kg)'] >= float(slider_val[0])) & (spacex_df['Payload Mass (kg)'] <= float(slider_val[1]))]
    if entered_site.upper() == 'ALL': 
        fig = px.scatter(data, x="Payload Mass (kg)", y='class', color="Booster Version Category")
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        data = filtered_df[(filtered_df['Payload Mass (kg)'] >= float(slider_val[0])) & (filtered_df['Payload Mass (kg)'] <= float(slider_val[1]))]
        fig = px.scatter(data, x="Payload Mass (kg)", y='class', color="Booster Version Category")
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
