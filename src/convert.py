import pandas as pd 

data_xls = pd.read_excel('dataset/firstvacc.xlsx', dtype=str, index_col=None)
data_xls.to_csv('firstvaccvacc.csv', encoding='utf-8', index=False)