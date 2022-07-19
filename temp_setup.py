from Stocks_project import db
from Stocks_project.models import All_Stocks, Stock_Info, User_Portfolio
from datetime import date, datetime
import matplotlib.pyplot as plt
import pandas as pd


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

print(df_stock_info[df_stock_info["INDUSTRY"]=="-"])
df_stock_info.loc[df_stock_info["INDUSTRY"]=="-","INDUSTRY"] = "Others"
print('df_stock_info industry null:: ',df_stock_info["INDUSTRY"].value_counts())
print('df_stock_info industry null:: ',df_stock_info["INDUSTRY"].unique())
print('df_stock_info',df_stock_info)

unique_industry_list = df_stock_info["INDUSTRY"].unique()
new_unique_industry_list = []

for industry in unique_industry_list:
    new_unique_industry_list.append((industry,industry))

print('new_unique_industry_list', new_unique_industry_list)
'''

'''
import exchange_calendars as ec
from nsepy import get_history
from datetime import date,  datetime as dt

str_curr_session_dt = date.today()
xbom = ec.get_calendar("XBOM")

if not xbom.is_session(str_curr_session_dt):
    str_curr_session_dt = dt.date(xbom.previous_close("2022-06-18"))
#print('str_curr_session_dt:', str_curr_session_dt)

from nsepy.history import get_price_list
df_daily_bhav = get_price_list(dt=str_curr_session_dt)
print(df_daily_bhav)


df_daily_bhav['Change %'] = (df_daily_bhav.CLOSE - df_daily_bhav.PREVCLOSE)/100
print('df_daily_bhav: ',df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
df_daily_bhav = df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

result = pd.merge(df_stock_info, df_daily_bhav, how='inner', on = 'ISIN')
print(result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])

# Fallout - joined on symbol - 4271     VENKEYS           NaN                                  NaN    NaN                         NaN     NaN  INE398A01010  1888.0  1888.00  1835.00  1853.55   -0.4140
# Fallout - joined on isin   - 1       AEGISLOG  INE208C01025                 Aegis Logistics Ltd.   1.00               Trading - Gas  Equity   AEGISCHEM   212.20   218.00   207.70   214.20    0.0065
# Fallout - joined on isin   - 4189         NaN  INE196Y01018                                  NaN    NaN                         NaN     NaN       WORTH    96.00    99.00    94.60    95.35   -0.0190


#The following worked
#stock_info_tcs = Stock_Info('TCS','Tata Consultancy Services','EQ',datetime(1980, 1, 1),1,1000,'ISIN0000',1,'IT','Y')
#db.session.add(stock_info_tcs)
#db.session.commit()


#The following worked
#tcs06MAY = All_Stocks('TCS',datetime(2022, 5, 6),3459, 3474.5,3424.5,3432.6,2010812)
#tcs05MAY = All_Stocks('TCS',datetime(2022, 5, 5),3512.1, 3533,3485.35,3513.4,1612000)
#tcs04MAY = All_Stocks('TCS',datetime(2022, 5, 4),3538.5, 3545.5,3465.3,3479.75,2306000)
#tcs02MAY = All_Stocks('TCS',datetime(2022, 5, 2),3519.5, 3547.9,3492.75,3542.4,1324000)
#db.session.add_all([tcs06MAY, tcs05MAY, tcs04MAY, tcs02MAY])
#db.session.commit()




#The following worked
#stock_info_nse = Stock_Info('NSENIFTY','NSE Nifty','EQ',datetime(1980, 1, 1),1,1000,'ISIN11111',1,'Index','Y')
#db.session.add(stock_info_nse)
#db.session.commit()


#The following worked
#nse06MAY = All_Stocks('NSENIFTY',datetime(2022, 5, 6),16415.55, 16484.2, 16340.9, 16411.25, 1000000)
#nse05MAY = All_Stocks('NSENIFTY',datetime(2022, 5, 5),16854.75, 16945.7, 16651.85, 16682.65,1000000)
#nse04MAY = All_Stocks('NSENIFTY',datetime(2022, 5, 4),17096.6, 17132.85, 16623.95, 16677.6,1000000)
#nse02MAY = All_Stocks('NSENIFTY',datetime(2022, 5, 2),16924.45, 17092.25, 16917.25, 17069.1,1000000)
#db.session.add_all([nse06MAY, nse05MAY, nse04MAY, nse02MAY])
#db.session.commit()




stock_info = Stock_Info.query.filter_by(symbol='TCS')
all_stock_info = stock_info.all()
print(all_stock_info)


#The following didn't work
#dt = datetime(2022, 5, 5)
#tcsMAY = All_Stocks.query.get('TCS',dt)   #will not work due to composite primary key. we get typeerror:2 positional args but 3 given


tcs = All_Stocks.query.filter_by(symbol ='TCS')
all_tcs_rec = tcs.all()
print(all_tcs_rec)


dt = date(2022, 5, 5)
tcs_1 = All_Stocks.query.filter(All_Stocks.symbol =='TCS').filter(All_Stocks.date_of_record == dt)
tcs_1_all = tcs_1.all()
print(dt)
print('tcs_1: ',tcs_1)
print('tcs_1_all: ',tcs_1_all)



#All_Stocks.query.filter_by(symbol ='TCS').delete()     #This worked    #https://stackoverflow.com/questions/27158573/how-to-delete-a-record-by-id-in-flask-sqlalchemy
#db.session.commit()



user_port = User_Portfolio.query.all()
print(user_port)


print('-------------------------------------------------------------------')
user_portf_stocks = User_Portfolio.query.filter_by(user_id=1)
list_user_symbol = []
for stk in user_portf_stocks:
    list_user_symbol.append(stk.symbol)
print('list_user_symbol in Show Portfolio: ',list_user_symbol)
max_date = db.session.query(db.func.max(All_Stocks.date_of_record)).scalar()
print(max_date)
max_strf_date = max_date.strftime("%d-%b-%y").upper()
print(max_strf_date)
all_user_stocks = All_Stocks.query.filter(All_Stocks.symbol.in_(list_user_symbol)).filter(All_Stocks.date_of_record==max_date).all()
print('all_user_stocks in Show Portfolio: ',all_user_stocks)






import yfinance as yf
yf_tcs = yf.Ticker("TCS.NS")
#d_tcs = yf_tcs.info
#print(d_tcs.keys())
#hist = msft.history(period="max")
df_hist = yf_tcs.history(start = '2022-05-01', end = '2022-05-09')
print('df_hist:',df_hist)
#df_hist['Close'].plot()
tcs_infy_few_data = yf.download("TCS.NS INFY.NS", start = '2022-05-01', end = '2022-05-09')
print('tcs_infy_few_data: ',tcs_infy_few_data)

tcs_infy_max_data = yf.download("TCS.NS INFY.NS", period="max")
print('tcs_infy_max_data:',tcs_infy_max_data)



from nsepy import get_history
from datetime import date
data_sbin = get_history(symbol="SBIN", start=date(2022,5,1), end=date(2022,5,9))
print(data_sbin)

nifty_next50 = get_history(symbol="NIFTY NEXT 50",
                            start=date(2022,5,1),
                            end=date(2022,5,9),
                            index=True)
print(nifty_next50)

nifty_50 = get_history(symbol="NIFTY 50",
                            start=date(2022,5,1),
                            end=date(2022,5,9),
                            index=True)
print(nifty_50)


from nsepy.history import get_price_list
prices = get_price_list(dt=date(2022,5,9))
print('prices: ',prices)

nifty_50_full = get_history(symbol="NIFTY 50",
                            start = date(2022,5,9),
                            end=date(2022,5,9),
                            index=True)
print('nifty_50_full: ', nifty_50_full)


nifty_50_holi = get_history(symbol="NIFTY 50",
                            start = date(2022,6,12),
                            end=date(2022,6,12),
                            index=True)
print('nifty_50_holi: ', nifty_50_holi)






#-------------------------------------------------------------------------------------------------------------------------


import requests
import pandas as pd
import json

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NIFTYBEES.BSE&outputsize=full&apikey=YVP6WADWLX8P06MH'
r = requests.get(url)
json_niftybees = r.json()
print(json_niftybees)
#print(json_niftybees["Time Series (Daily)"]['2022-06-13']['4. close'])
#print(json_niftybees["Time Series (Daily)"].keys())
keys = reversed(json_niftybees["Time Series (Daily)"].keys())
new_dict = {x:json_niftybees["Time Series (Daily)"][x]['4. close'] for x in keys}
#print('new_dict: ', new_dict)
#new_df = pd.DataFrame(list(new_dict.items()))
#new_df = new_df.loc[::-1].reset_index(drop=True).head()
#for col in new_df.columns:
#    print(col)
#new_df.columns = ['date_of_record', 'close_price']
new_df = pd.DataFrame(list(new_dict.items()), columns=['date_of_record','close_price'])
print('new_df: ', new_df)
print(new_df.iloc[-1][0])



#print(json_niftybees["Time Series (Daily)"])
#df_niftybees = pd.json_normalize(json_niftybees["Time Series (Daily)"], max_level = 0)
#print(df_niftybees['2022-05-13'])







import exchange_calendars as ec
from datetime import date,  datetime as dt

today = date.today()
print('today:', today)

xbom = ec.get_calendar("XBOM")
print(xbom)
print(xbom.is_session(today))

print(xbom.previous_session(today))

#str_curr_session_dt = dt.date(xbom.previous_close(str_curr_session_dt))
str_valid_session_dt = dt.date(xbom.previous_session(today)).isoformat()
print('str_valid_session_dt:',str_valid_session_dt)

from nsepy.history import get_price_list
df_daily_bhav = get_price_list(dt=today)
df_daily_bhav['Change %'] = (df_daily_bhav.CLOSE - df_daily_bhav.PREVCLOSE)/100
print('df_daily_bhav: ',df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
'''
