from math import log10
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from plotly.subplots import make_subplots
import numpy as np
import base64


# Reading and preparing datas
df_vac1_repartion = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/first dosage.csv')
df_vac2_repartion = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/second dosage.csv')

df_daily = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/Dailyvac.csv')

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
BY.to_csv('check.csv')

# dataframes dictionary necessary for the legends
dfs = {'Bayern': BY, 'Berlin': BE, 'Nordrhein-Westfalen': NW,
       'Sachsen': SN, 'Thüringen': TH}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#calculations for some annotations
ymax=max(max(BY["Cases_Last_Week"]),max(BE["Cases_Last_Week"]), max(NW["Cases_Last_Week"]), max(SN["Cases_Last_Week"]), max(TH["Cases_Last_Week"]) )
state=""
max_by= max(BY["Cases_Last_Week"])
max_be=max(BE["Cases_Last_Week"])
max_nw=max(NW["Cases_Last_Week"])
max_sn=max(SN["Cases_Last_Week"])
max_th=max(TH["Cases_Last_Week"])
xmax=0
if max_by==ymax :
    state='BY'
    s = BY["Cases_Last_Week"].idxmax()
    xmax=BY.iloc[s,1]
if max_be==ymax :
    state='BE'
    s = BE["Cases_Last_Week"].idxmax()
    xmax=BE.iloc[s,1]
if max_nw==ymax :
    state='NW'
    s = NW["Cases_Last_Week"].idxmax()
    xmax=NW.iloc[s,1]
if max_sn==ymax :
    state='SN'
    s = SN["Cases_Last_Week"].idxmax()
    xmax=SN.iloc[s,1]
if max_th==ymax :
    state='TH'
    s = TH["Cases_Last_Week"].idxmax()
    xmax=TH.iloc[s,1]

#axis is logarithmic
y_max_log = log10(ymax)

max_annotation = {
    'x':xmax,'y':y_max_log,
    'showarrow':True,'arrowhead':3,
    'text':'Maximum n={} in {} \n @{}'.format(ymax, state, xmax),
    'font':{'size':10,'color':'black'}
    }

    




#figure of the last week cases 
fig = go.Figure()
for i in dfs:
    fig = fig.add_trace(go.Scatter(x=dfs[i]["Date"],
                                   y=dfs[i]["Cases_Last_Week"],
                                   name=i))

fig.update_xaxes(title_text='Date')
fig.update_yaxes(type="log", title_text='Cases Last Week')

date_buttons = [{'count': 12, 'step': "month", 'stepmode': "todate", 'label': "1 Year"},
                {'count': 6, 'step': "month", 'stepmode': "todate", 'label': "6 Months"},
                {'count': 14, 'step': "day", 'stepmode': "todate", 'label': "2 Weeks"}
            
]
fig.update_layout(    {'xaxis':      {'rangeselector':        {'buttons': date_buttons}    }})



fig.update_layout(title='7 day incidenz', title_x=0.5, template="plotly_white")
fig.update_layout({'annotations':[max_annotation]})

# preparing the display of the tum logo to be used inside the html.DiV
tumlogo = Path(__file__).parent.parent / 'assets/tumlogo.png'
logo_base64 = base64.b64encode(open(tumlogo, 'rb').read()).decode('ascii')

# creating second figure
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
                   title_x=0.5, template="plotly_white")



fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df_daily['Datum'],y=df_daily['Erstimpfung'],name = 'Daily First dosage ' ) )
fig3.add_trace(go.Scatter(x=df_daily['Datum'],y=df_daily['Zweitimpfung'],name = 'Daily Second dosage ' ) )
fig3.add_trace(go.Scatter(x=df_daily['Datum'],y=df_daily['Gesamtzahl verabreichter Impfstoffdosen'],name = 'Total number of daily vaccine doses' ) )

fig3.update_layout(title="Daily vaccination ",
                   title_x=0.5, template="plotly_white")

# conversion to numpy to calculate the sum
first_numpy = df_daily['Erstimpfung'].values
second_numpy =  df_daily['Zweitimpfung'].values

# Calculating the sum of first dosage and second dosage to create a pie chart
sum_first=0
sum_second = 0
for i in first_numpy:
    sum_first=sum_first+i 
for i in second_numpy:
    sum_second=sum_second+i 

# figure 4 as a pie chart 
fig4 = go.Figure()
fig4.add_trace(go.Pie(labels=['First dosage','Second dosage'],values=[sum_first,sum_second]))

print(BY.iloc[1,1])
#Preparing the slider dates
BY['Date'] = pd.to_datetime(BY['Date'], errors='coerce')

crop_30=[]

for i in range(0,len(BY['Date']),30):
    crop_30.append(BY.iloc[i,1])

print (crop_30)
date= [x for x in range(len(BY['Date'].unique()))]
print(date)
dates_30 = []
for i in range(0,len(date),30):
    dates_30.append(date[i])

# application layout
app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(logo_base64),
             style={'height': '10%', 'width': '10%', 'display': 'e'}),
    html.Center(html.H1(children='Covid Interactive dashboard',
                        style={'color': '#0065bd'})),

    html.Center(dcc.Markdown('''
        This dashboard gives an overview about the current covid situation in **germany** as well as the **progress** and **details** about the **vaccination**.
    ''', style={'fontSize': 16,'color': '#000000'})),
    html.Div([
        html.Br(),
        dcc.Markdown("Please Select **cities** for the visualization of **the 7 day incidence** :",style={'color': '#000000'}),
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
            min=dates_30[0],
            max=dates_30[-1],
            value=BY.iloc[0,1],
            marks={numd:date.strftime('%d/%m/%y') for numd,date in zip(dates_30, crop_30)},
            step=80
            
        ),
        dcc.Graph(
            id='7_week_inzidenz',
            figure=fig
        )
    ], style={'width': '55%', 'display': 'inline-block'}),

    html.Div([
        
        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Markdown(" Select the **factors**  to see **vaccine's** progress based on the fields in **german cities** :",style={'color': '#000000'}),
        dcc.Dropdown(
            options=[
                {'label': 'Age', 'value': 'AGE'},
                {'label': 'Job', 'value': 'JOB'},
                {'label': 'Medical Staff', 'value': 'MED'},
                {'label': 'Nursing house residents', 'value': 'NHR'}
            ],
            value=['AGE','JOB','MED','NHR'],
            multi = True
            
        ),
        dcc.Graph(
            id='graph2',
            figure=fig2
        )
    ],
        style={'width': '40%', 'display': 'inline-block', 'float': 'right'},


    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Markdown("The graph below shows the daily vaccines given and their classification if they are given as first dosage or second as well as the total given vaccine",style={'color': '#000000'}),
        dcc.Graph(
            figure=fig3
            )
        ],
        style={'width': '50%', 'display': 'inline-block', 'float': 'left'},
        ),
    html.Div([
        dcc.Graph(
            figure=fig4
            )
        ],
    
    style={'width': '50%', 'display': 'inline-block', 'float': 'right'},
    )

    


]            
)


if __name__ == '__main__':
    app.run_server()

