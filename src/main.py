import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from pathlib import Path

df_vac1_repartion = pd.read_csv(Path(__file__).parent.parent /'dataset/first dosage.csv')
df_vac2_repartion = pd.read_csv(Path(__file__).parent.parent /'dataset/second dosage.csv')
print(df_vac2_repartion)
