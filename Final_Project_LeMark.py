

from typing import Any
import csv
import pandas as pd
import dash
import dash_core_components as dcc
#import dash_html_components as html
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from dash import html
import dash_html_components as html

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("SEVEN_MAJOR_FELONY_OFFENSES_Rate.csv")
df = df.groupby(['OFFENSE', 'Year','LaborForce','Borough','Unemployed','Employed','State','Rate','Total For 2019', 'Total For 2020'])[['Unemployed']].mean()
df.reset_index(inplace=True)
print(df[:100000]) 

app = dash.Dash(__name__)

app.layout = html.Div([

    
    html.P('Hover over the circle to see crime information per Borough in NYC'),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='Year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(Year): str(Year) for Year in df['Year'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('Year-slider', 'value'))
def update_figure(selected_Year):
    filtered_df = df[df.Year == selected_Year]

    fig = px.scatter(filtered_df, x="Unemployed", y="Year",
                     size="Rate", color="OFFENSE", hover_name="Borough",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)