import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import numpy as np
import base64


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_vac1_repartion = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/first dosage.csv')
df_vac2_repartion = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/second dosage.csv')


# print(df_vac2_repartion)
BY = pd.read_csv(
    "https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-BY.tsv", sep="\t")
BE = pd.read_csv(
    "https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-BE.tsv", sep="\t")
NW = pd.read_csv(
    "https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-NW.tsv", sep="\t")
SN = pd.read_csv(
    "https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-SN.tsv", sep="\t")
TH = pd.read_csv(
    "https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-TH.tsv", sep="\t")
# print(BY)

# dataframes
dfs = {'Bayern': BY, 'Berlin': BE, 'Nordrhein-Westfalen': NW,
       'Sachsen': SN, 'Thüringen': TH}
# ax=fig.add_subplot(111)

fig = go.Figure()
for i in dfs:
    fig = fig.add_trace(go.Scatter(x=dfs[i]["Date"],
                                   y=dfs[i]["Cases_Last_Week"],
                                   name=i))

fig.update_xaxes(title_text='Date')
fig.update_yaxes(type="log", title_text='Cases Last Week')



fig.update_layout(title='7 day incidenz', title_x=0.5, template="simple_white")

tumlogo = Path(__file__).parent.parent / 'assets/tumlogo.png'
logo_base64 = base64.b64encode(open(tumlogo, 'rb').read()).decode('ascii')


fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df_vac1_repartion['Bundesland'], y=df_vac1_repartion['Indikation nach Alter*'],
                      name='indication per age'))
fig2.add_trace(go.Bar(x=df_vac1_repartion['Bundesland'], y=df_vac1_repartion['Berufliche Indikation*'],
                      name='indication per job'))
fig2.add_trace(go.Bar(x=df_vac1_repartion['Bundesland'], y=df_vac1_repartion['Medizinische Indikation*'],
                      name='Medical staff'))
fig2.add_trace(go.Bar(x=df_vac1_repartion['Bundesland'],
                      y=df_vac1_repartion['Pflegeheim-bewohnerIn*'], name='Nursing home residents'))
fig2.update_layout(title="Vaccine repartition due to factors",
                   title_x=0.5, template="simple_white")


app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(logo_base64),
             style={'height': '10%', 'width': '10%', 'display': 'e'}),
    html.Center(html.H1(children='Covid Interactive dashboard',
                        style={'color': '#7FDBFF'})),

    dcc.Markdown('''
        This dashboard gives an overview about the current covid situation in **germany** as well as the **progress** and **details** about the **vaccination**.
    ''', style={'fontSize': 16}),
    html.Div([
        html.Br(),
        dcc.Markdown("Please Select **cities** for the visualization of **the 7 day incidence** :"),
        dcc.Dropdown(
            options=[
                {'label': 'Bayern', 'value': 'BY'},
                {'label': 'Berlin', 'value': 'BE'},
                {'label': 'Nordhein-Westfalen', 'value': 'NW'},
                {'label': 'Sachsen', 'value': 'SE'},
                {'label': 'Thüringen', 'value': 'TH'}
            ],
            placeholder="Select a region",
            value=['BY', 'BE', 'NW', 'SE', 'TH'],
            multi=True
        ),
        dcc.Slider(
            min=1,
            max=12,
            marks={i: 'Month {}'.format(i) for i in range(13)},
            value=12,
        ),

        dcc.Graph(
            id='7_week_inzidenz',
            figure=fig
        )
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        
        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Markdown(" Select the **factors**  to see **vaccine's** progress based on the fields in **german cities** :"),
        html.Center(dcc.RadioItems(
            options=[
                {'label': 'Age', 'value': 'AGE'},
                {'label': 'Job', 'value': 'JOB'},
                {'label': 'Medical Staff', 'value': 'MED'},
                {'label': 'Nursing house residents', 'value': 'NHR'}
            ],
            value=['AGE','JOB','MED','NHR'],
            labelStyle={'display': 'inline-block'}
            
        )),
        dcc.Graph(
            id='graph2',
            figure=fig2
        )
    ],
        style={'width': '40%', 'display': 'inline-block', 'float': 'right'},


    )


]             
)


if __name__ == '__main__':
    app.run_server()
