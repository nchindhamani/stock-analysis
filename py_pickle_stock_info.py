'''
This is an one time script to pickle the csv file downloaded from bseindia website.
Unpickling will give a dataframe with columns 'SYMBOL', 'ISIN', 'NAME_OF_COMPANY','FV','INDUSTRY','SEGMENT'
Pickled filename is stock_info_bse.pkl
'''

import csv
import pandas as pd
df_stock_info = pd.DataFrame([], columns = ['SYMBOL', 'ISIN', 'NAME_OF_COMPANY','FV','INDUSTRY','SEGMENT'])
file = open('Equity_bse.csv')

csvreader = csv.reader(file)

header = []
header = next(csvreader)
#print(header)

for row in csvreader:
        row = [row[2], row[7], row[1], row[6],row[12], row[9]]
        df_stock_info.loc[len(df_stock_info)] = row

file.close()

df_stock_info.loc[df_stock_info["INDUSTRY"]=="-","INDUSTRY"] = "Others"
#print('df_stock_info industry null:: ',df_stock_info["INDUSTRY"].value_counts())
#print('df_stock_info industry null:: ',df_stock_info["INDUSTRY"].unique())
#print('df_stock_info',df_stock_info)

pd.to_pickle(df_stock_info, "./stock_info_bse.pkl")
