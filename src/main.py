import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)






df_vac1_repartion = pd.read_csv(Path(__file__).parent.parent /'dataset/first dosage.csv')
df_vac2_repartion = pd.read_csv(Path(__file__).parent.parent /'dataset/second dosage.csv')

#print(df_vac2_repartion)
BY = pd.read_csv("https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-BY.tsv",sep="\t")
BE= pd.read_csv("https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-BE.tsv",sep="\t")
NW= pd.read_csv("https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-NW.tsv",sep="\t")
SN= pd.read_csv("https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-SN.tsv",sep="\t")
TH= pd.read_csv("https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-TH.tsv",sep="\t")
#print(BY)

#dataframes
dfs = {'Bayern':BY,'Berlin':BE,'Nordrhein-Westfalen':NW,'Sachsen':SN,'Thüringen':TH}
#ax=fig.add_subplot(111)

fig = go.Figure()
for i in dfs : 
     fig = fig.add_trace(go.Scatter(x = dfs[i]["Date"],
                                   y = dfs[i]["Cases_Last_Week"],
                                   name = i ))

fig.update_xaxes(title_text='Date')
fig.update_yaxes(type="log",title_text='Cases Last Week')


'''fig=(px.line(BY["Date"], BY["Cases_Last_Week"]))
fig=(px.line(BE["Date"], BE["Cases_Last_Week"]))
fig=(px.line(NW["Date"], NW["Cases_Last_Week"]))
fig=(px.line(SN["Date"], SN["Cases_Last_Week"]))
fig=(px.line(TH["Date"], TH["Cases_Last_Week"]))'''
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

'''ax.annotate('Maximum n={} in {} \n @{}'.format(ymax, state, xmax), xy=(xmax, ymax), xytext = (xmax, ymax+10), arrowprops=dict(facecolor='black', shrink=0.05))
plt.yscale("log")
plt.title('7-day Incidence of Covid-cases')
plt.xlabel('Date')
plt.ylabel('n/week')
start, end = ax.get_xlim()
plt.xticks(np.arange(start, end, 30))
plt.grid(True)
plt.legend(loc=2)
plt.show()'''

fig.add_annotation(x=xmax, y=ymax,
            text='Maximum n={} in {} \n @{}'.format(ymax, state, xmax),
            showarrow=True,
            arrowhead=1,
            yshift=ymax+10)


app.layout = html.Div([
    html.Center(html.H1(children='Covid Interactive dashboard')),

    dcc.Markdown('''
        This dashboard gives an overview about the current covid situation in **germany** as well as the **progress** and **details** about the **vaccination**.
    ''',style={ 'fontSize': 16}),
    html.Div([
    html.Br(),
    dcc.Dropdown(
    options=[
        {'label': 'Bayern', 'value': 'BY'},
        {'label': 'Berlin', 'value': 'BE'},
        {'label': 'Nordhein-Westfalen', 'value': 'NW'},
        {'label': 'Sachsen', 'value': 'SE'},
        {'label': 'Thüringen', 'value': 'TH'}
    ],
    placeholder="Select a region",
    value =['BY','BE','NW','SE','TH'],
    multi=True
 ),  
    dcc.Slider(
    min=1,
    max=12,
    marks={i: 'Month {}'.format(i) for i in range(13)},
    value=12,
 ),

    dcc.Graph(
        id='7 week inzidenz',
        figure=fig
    )
    ]
    ,style={'width': '55%', 'display': 'inline-block'})
    
])

if __name__ == '__main__':
    app.run_server()



