import pandas as pd 

data_xls = pd.read_excel('dataset/secondvacc compagnies.xlsx', dtype=str, index_col=None)
data_xls.to_csv('secondvacc.csv', encoding='utf-8', index=False)