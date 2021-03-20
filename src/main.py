"""
Interactive Covid dashboard authored by Gabriela Sau and Rayen Dhahri .
The dashboard gives an overview about the covid situation in germany and the progress
of the vaccination and allows a range of customization
The datas were rawly provided by Rki in a 4 page excel sheet and we cleaned them and converted them
to be prepared for the usage and to avoid some alphabetical sorting while ploting
"""
import base64
from pathlib import Path
from math import log10
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go


# Reading and preparing datas
df_vac1_repartion = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/first dosage.csv')
df_vac2_repartion = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/second dosage.csv')

df_daily = pd.read_csv(
    Path(__file__).parent.parent / 'dataset/Dailyvac.csv')


df_1comp =pd.read_csv(
    Path(__file__).parent.parent / 'dataset/firstvaccvacc.csv',index_col=False)

df_2comp =pd.read_csv(
    Path(__file__).parent.parent / 'dataset/secondvacc.csv',index_col=False)

# will be used for callbacks in order to select which dataframe to use
df_comp ={'First dosage':df_1comp,'Second dosage':df_2comp}


BY = pd.read_csv("https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-states/de-state-BY.tsv", sep="\t")
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
dfs = {'Bayern': BY, 'Berlin': BE, 'Nordhein-Westfalen': NW,
       'Sachsen': SN, 'Thüringen': TH}
#print(NW.shape, BY.shape, SN.shape)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# calculations for some annotations


def global_max_annotation():
    ymax = max(max(BY["Cases_Last_Week"]), max(BE["Cases_Last_Week"]), max(
        NW["Cases_Last_Week"]), max(SN["Cases_Last_Week"]), max(TH["Cases_Last_Week"]))
    state = ""
    max_by = max(BY["Cases_Last_Week"])
    max_be = max(BE["Cases_Last_Week"])
    max_nw = max(NW["Cases_Last_Week"])
    max_sn = max(SN["Cases_Last_Week"])
    max_th = max(TH["Cases_Last_Week"])
    xmax = 0
    if max_by == ymax:
        state = 'BY'
        index_max = BY["Cases_Last_Week"].idxmax()
        xmax = BY.iloc[index_max, 1]
    if max_be == ymax:
        state = 'BE'
        index_max = BE["Cases_Last_Week"].idxmax()
        xmax = BE.iloc[index_max, 1]
    if max_nw == ymax:
        state = 'NW'
        index_max = NW["Cases_Last_Week"].idxmax()
        xmax = NW.iloc[index_max, 1]
    if max_sn == ymax:
        state = 'SN'
        index_max = SN["Cases_Last_Week"].idxmax()
        xmax = SN.iloc[index_max, 1]
    if max_th == ymax:
        state = 'TH'
        index_max = TH["Cases_Last_Week"].idxmax()
        xmax = TH.iloc[index_max, 1]

    # axis is logarithmic so we need to perform a log on our ymax for the right positionning
    y_max_log = log10(ymax)
    # preparing annotation to be displayed in fig
    max_annotation = {
        'x': xmax, 'y': y_max_log,
        'showarrow': True, 'arrowhead': 3,
        'text': 'the overall Maximum n={} in {} \n @{}'.format(ymax, state, xmax),
        'font': {'size': 10, 'color': 'black'}
    }
    return max_annotation


# preparing the display of the tum logo to be used inside the html.DiV
tumlogo = Path(__file__).parent.parent / 'assets/tumlogo.png'
logo_base64 = base64.b64encode(open(tumlogo, 'rb').read()).decode('ascii')

# creating second figure
# it will be inside the callback
# Dropdown fig dict to generate 2nd figure
factors_dict = {'Indication per age': 'Indikation nach Alter*', 'Indication per job': 'Berufliche Indikation*', 'Medical Indication': 'Medizinische Indikation*',
                'Nursing home residents': 'Pflegeheim-bewohnerIn*'}

# using pure plotly advance interactivity options for the 3rd figure
fig3 = go.Figure()
# markers + lines to show that at the begining that the total is the same as first dosage
fig3.add_trace(go.Scatter(
    x=df_daily['Datum'], y=df_daily['Erstimpfung'], name='Given as First dosage ', mode='markers+lines'))
fig3.add_trace(go.Scatter(
    x=df_daily['Datum'], y=df_daily['Zweitimpfung'], name='Given as Second dosage '))
fig3.add_trace(go.Scatter(
    x=df_daily['Datum'], y=df_daily['Gesamtzahl verabreichter Impfstoffdosen'], name='Total number of daily doses given'))

# have 3 different type of figures
showoptions = [{'label': "Line", 'method': "update", 'args': [{"type": "scatter", 'mode': 'lines'}]},
               {'label': "Scatter", 'method': "update", 'args': [
                   {"type": "scatter", 'mode': 'markers'}]},
               {'label': "Bar", 'method': "update", 'args': [{"type": "bar"}]}]


# updating axes range for better visibility while zooming
fig3.update_yaxes(
    range=[0, df_daily['Gesamtzahl verabreichter Impfstoffdosen'].max()+10000])
fig_int = go.Figure()
# preparing datas for slider using an intermidiate
for stage in ['Erstimpfung', 'Zweitimpfung', 'Gesamtzahl verabreichter Impfstoffdosen']:
    fig_int.add_trace(
        go.Bar(x=df_daily['Datum'], y=df_daily[stage], name=stage))
# creating in plot slider
Slider = [
    {'steps': [
        {'method': 'update', 'label': 'daily given as First dosage',
         'args': [{'visible': [True, False, False]}]},
        {'method': 'update', 'label': 'daily given as second dosage',
         'args': [{'visible': [False, True, False]}]},
        {'method': 'update', 'label': 'daily total given dosage',
         'args': [{'visible': [False, False, True]}]},
        {'method': 'update', 'label': 'All ', 'args': [
            {'visible': [True, True, True]}]},
        {'method': 'update', 'label': 'First vs Second ', 'args': [{'visible': [True, True, False]}]}]},
]

fig3.update_layout({'sliders': Slider})

fig3.update_layout(title="Daily vaccination ",
                   title_x=0.3,title_y=0.9, template="plotly_white", updatemenus=[{
                       'type': "buttons", 'direction': 'down',
                       'x': 1.5, 'y': 0.5,
                       'showactive': True, 'active': 0,
                       'buttons': showoptions}])

# moving the slider a little bit down
fig3['layout']['sliders'][0]['pad'] = dict(r=10, t=100,)


# Calculating the sum of first dosage and second dosage to create a pie chart
def sum_func(numpy_arr):
    """[summary]
    callculate the sum over the arrays
    Args:
        numpy_1 ([array]): [array to sum on ]
        numpy_2 ([ar]): [second dosage]

    Returns:
        [type]: [the sum over 2 numpy arrays]
    """
    sum_pie = 0
    for k in numpy_arr:
        sum_pie = sum_pie+k
    return sum_pie


# figure 4 as a pie chart
fig_pie = go.Figure()
fig_pie.add_trace(go.Pie(labels=['First dosage', 'Second dosage'], values=[
               sum_func(df_daily['Erstimpfung'].values), sum_func(df_daily['Zweitimpfung'].values)]))
fig_pie.update_layout(title='Vaccines distribution',
                   title_x=0.5,title_y=0.9, template="plotly_white")
colors=[ 'darkorange', 'lightgreen']
fig_pie.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
# Preparing the slider dates
BY['Date'] = pd.to_datetime(BY['Date'], errors='coerce')

crop_30 = []

for s in range(0, len(BY['Date'])-1, 30):
    crop_30.append(BY.iloc[s, 1])
crop_30.append(BY.iloc[-1,1])

# print(crop_30)
date = [x for x in range(len(BY['Date'].unique()))]
# print(date)
dates_30 = []
for n in range(0, len(date)-1, 30):
    dates_30.append(date[n])
    # include last actual date
dates_30.append(date[-1])
#print (dates_30)
#print (crop_30)


def auto_gendict (column):
    """
    in order to manage huge amount of options in the dropdown this function auto generations a dictonary from a given column
    this will be passed after to the option argument in the dcc component
    Args:
        column: a column/row of a data frame that contains labeled data

    Returns:
        [dict]: a dictionany with label and value set to a numerical index
    """
    dict_gen=[]
    j=0
    for i in column:
        dict_gen.append({'label': i, 'value': j})
        j+=1
    return dict_gen
    
print ()


# application layout
app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(logo_base64),
             style={'height': '10%', 'width': '10%', 'display': 'e'}),
    html.Center(html.H1(children='Covid Interactive dashboard',
                        style={'color': '#0065bd'})),

    html.Center(dcc.Markdown('''
        This dashboard gives an overview about the current covid situation in **germany** as well as the **progress** and **details** about the **vaccination**.
    ''', style={'fontSize': 16, 'color': '#000000'})),
    html.Div([
        html.Br(),
        html.Br(),
        dcc.Markdown("Please Select **cities** for the visualization of **the 7 day incidence** :",
                     style={'color': '#000000'}),
        dcc.Dropdown(
            id='city_selected',
            options=[
                {'label': 'Bayern', 'value': 'Bayern'},
                {'label': 'Berlin', 'value': 'Berlin'},
                {'label': 'Nordhein-Westfalen', 'value': 'Nordhein-Westfalen'},
                {'label': 'Sachsen', 'value': 'Sachsen'},
                {'label': 'Thüringen', 'value': 'Thüringen'}
            ],
            placeholder="Select a region",
            value=['Bayern', 'Berlin', 'Nordhein-Westfalen',
                   'Sachsen', 'Thüringen'],
            multi=True
        ),
        dcc.RangeSlider(
            min=dates_30[0],
            max=dates_30[-1],
            marks={numd: date.strftime('%y-%m-%d')
                    for numd, date in zip(dates_30, crop_30)},
            step=dates_30[1]-dates_30[0]

        ),
        dcc.Graph(
            id='7_week_inzidenz'

        )
    ], style={'width': '55%', 'display': 'inline-block'}),
    html.Div([
        html.Br(),
        html.Br(),
        dcc.Markdown(" Select the **factors**  to see their effect and importance in the **vaccine's** progress  in **german cities** :",
                     style={'color': '#000000'}),
        dcc.Dropdown(
            id='drop_fac',
            options=[
                {'label': 'Age', 'value': 'Indication per age'},
                {'label': 'Job', 'value': 'Indication per job'},
                {'label': 'Medical Staff', 'value': 'Medical Indication'},
                {'label': 'Nursing house residents',
                    'value': 'Nursing home residents'}
            ],
            value=['Indication per age', 'Indication per job',
                   'Medical Indication', 'Nursing home residents'],
            multi=True

        ),
        dcc.Graph(
            id='factors',
        )
    ],
        style={'width': '40%', 'display': 'inline-block', 'float': 'right'},


    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Center(html.Label('Vaccination Progress',style={'fontSize':25,'color':'#0065bd','marginBottom': 10, 'marginTop': 25})),
        html.Center(dcc.Markdown("The graphs below show the daily vaccines given and their classification if they were given as first dosage or second as well as the total vaccines and its  distribution",
         style={
                     'color': '#000000'})),
    html.Div([
        
        dcc.Graph(
            figure=fig3
        )
    ],
        style={'width': '70%', 'display': 'inline-block', 'float': 'left'},
    ),
    html.Div([
        dcc.Graph(
            figure=fig_pie
        )
    ],
        style={'width': '30%', 'display': 'inline-block', 'float': 'right'},
    ),
     html.Br(),
    html.Br(),
    html.Center(html.Label('Leading vaccine manufacturers',style={'fontSize':25,'color':'#0065bd','marginBottom': 10, 'marginTop': 25})),
    html.Div([
        # too many values in the dropdown => auto generated dictionnay 
        dcc.Dropdown(
            id='comp_drop',
            options=auto_gendict(df_2comp['Bundesland'].unique()),
            value = [i for i in range(4)],
            multi=True

        ),
        dcc.Checklist(
            id='check_dos',
            options=[
                {'label': 'First dosage', 'value': 'First dosage'},
                {'label': 'Second dosage', 'value': 'Second dosage'}
            ],
            value=['First dosage'],
            labelStyle={'display': 'inline-block'}
        ),  
        dcc.Graph(
            id ="vacc_comp"
        )
    ],
        style={'width': '100%', 'display': 'inline-block'},
    )




]
)

#print (dfs.keys())
#print(crop_30[-1])

@app.callback(
    Output('7_week_inzidenz', 'figure'),
    Input('city_selected', 'value'))
def update_figure(selected_city):
    """[summary]

    Args:
        selected_city ([type]): [description]

    Returns:
        [type]: [description]
    """
    fig = go.Figure()
    for i in selected_city:
        fig = fig.add_trace(go.Scatter(x=dfs[i]["Date"],
                                       y=dfs[i]["Cases_Last_Week"],
                                       name=i))
        # Display the maximum of the new selection and global once there are 5 states
        y_inter = max(dfs[i]["Cases_Last_Week"])
        state = i
        s = dfs[i]["Cases_Last_Week"].idxmax()
        xmax_loc = dfs[i].iloc[s, 1]
        ymax_loc = log10(y_inter)
        max_loc_anno = {
            'x': xmax_loc, 'y': ymax_loc,
            'showarrow': True, 'arrowhead': 3,
            'text': 'the Maximum in {} n={}  \n @{}'.format(state, ymax_loc, xmax_loc),
            'font': {'size': 10, 'color': 'black'}
        }
        fig.update_layout({'annotations': [max_loc_anno]})

    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(type="log", title_text='Cases Last Week')

    date_buttons = [
        {'step': "all", 'stepmode': "todate", 'label': "All"},
        {'count': 12, 'step': "month",
         'stepmode': "todate", 'label': "1Y"},
        {'count': 6, 'step': "month",
         'stepmode': "todate", 'label': "6M"},
        {'count': 3, 'step': "month",
         'stepmode': "todate", 'label': "3M"}

    ]
    fig.update_layout(
        {'xaxis':      {'rangeselector':
                        {'buttons': date_buttons}}})
    #print (date_buttons)

    # add buttons
    fig.update_layout(title='7 day incidence',
                      title_x=0.5, template="plotly_white")
    #global max
    if len(selected_city) == 5:
        fig.update_layout({'annotations': [global_max_annotation()]})

    return fig


@app.callback(
    Output('factors', 'figure'),
    Input('drop_fac', 'value'))
def update_2figure(factors):
    """[summary]

    Args:
        factors ([type]): [description]

    Returns:
        [type]: [description]
    """
    fig2 = go.Figure()
    for j in factors:
        fig2 = fig2.add_trace(
            go.Bar(x=df_vac1_repartion['Bundesland'], y=df_vac1_repartion[factors_dict[j]], name=j))
    fig2.update_layout(title="Vaccine repartition due to factors",
                       title_x=0.5, template="plotly_white")

    return fig2

#solved without the need of alternances 
#red = ["#FF000"+str(i) for i in range (15)]

@app.callback(
    Output('vacc_comp', 'figure'),
    Input('comp_drop', 'value'),
    Input('check_dos', 'value'))
def update_vacfig(state,dosage):
    figcomp = go.Figure()
    print(dosage)
    duplicate_legend_fix = 0
    for i in state :
        duplicate_legend_fix = duplicate_legend_fix + 1
        for j in dosage :
                # avoid legends being duplicated so showlegend true only in first case
                
                if duplicate_legend_fix == 1:
                    figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=df_comp[j].iloc[[i],2],text=df_comp[j].iloc[[i],2] ,
                                                        marker={'color' :'orange'},textposition='auto', name = 'BioNTech',showlegend=True))
                    figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=df_comp[j].iloc[[i],3],text=df_comp[j].iloc[[i],3] ,
                                                        marker={'color' :'green'},textposition='auto',name = 'Moderna',showlegend=True))
                    #astrazeneca exists only in first given the data till 03/20/2021
                    if (j== 'First dosage'):
                        figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=df_comp[j].iloc[[i],4],text=df_comp[j].iloc[[i],4] ,
                                                            marker={'color' :'yellow'},textposition='auto',name = 'AstraZeneca',showlegend=True))
                    else :
                        # Not leaving empty but plotting with 0 
                        y_0 = np.zeros(len(df_1comp.iloc[:,0].values.shape))
                        figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=y_0,text='0' ,
                                                        marker={'color' :'yellow'},textposition='auto',name = 'AstraZeneca',showlegend=True))
                else : 
                    figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=df_comp[j].iloc[[i],2],text=df_comp[j].iloc[[i],2] ,
                                                        marker={'color' :'orange'},textposition='auto', name = 'BioNTech',showlegend=False))
                    figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=df_comp[j].iloc[[i],3],text=df_comp[j].iloc[[i],3] ,
                                                        marker={'color' :'green'},textposition='auto',name = 'Moderna',showlegend=False))
                    #astrazeneca exists only in first given the data till 03/20/2021
                    if (j== 'First dosage'):
                        figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=df_comp[j].iloc[[i],4],text=df_comp[j].iloc[[i],4] ,
                                                            marker={'color' :'yellow'},textposition='auto',name = 'AstraZeneca',showlegend=False))
                    else :
                        # Not leaving empty but plotting with 0 
                        y_0 = np.zeros(len(df_1comp.iloc[:,0].values.shape))
                        figcomp= figcomp.add_trace( go.Bar (x=df_comp[j].iloc[[i],0],y=y_0,text='0' ,
                                                        marker={'color' :'yellow'},textposition='auto',name = 'AstraZeneca',showlegend=False))
                        
                
    figcomp.update_layout(title="Vaccines used depending on the state",
                       title_x=0.5, template="plotly_white")
    return figcomp






if __name__ == '__main__':
    app.run_server()
