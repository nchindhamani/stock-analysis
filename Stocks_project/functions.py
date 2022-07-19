from Stocks_project.models import All_Stocks
from Stocks_project import db
from datetime import date, datetime
import pandas as pd


def f_stock_valuation(req_stocks):
    latest_rec_tuple = ()
    latest_rec_list = []

    if(req_stocks == []):
        print('Empty req_stocks')
        latest_rec_df = pd.DataFrame(columns=['symbol','date_of_record','name_of_company','open_price','high_price','low_price','close_price','date_of_listing'])
        max_date = db.session.query(db.func.max(All_Stocks.date_of_record)).scalar()
        max_strf_date = max_date.strftime("%d-%b-%y").upper()

    else:
        for company in req_stocks:
            latest_rec_tuple = (company.symbol, company.date_of_record, company.s_info.name_of_company, company.open_price, company.high_price, company.low_price, company.close_price, company.s_info.date_of_listing)
            latest_rec_list.append(latest_rec_tuple)

            latest_rec_df = pd.DataFrame(latest_rec_list, columns=['symbol','date_of_record','name_of_company','open_price','high_price','low_price','close_price','date_of_listing'])
            latest_rec_df['listing_year'] = pd.DatetimeIndex(latest_rec_df['date_of_listing']).year
            max_date = latest_rec_df['date_of_record'].max()
            max_strf_date = max_date.strftime("%d-%b-%y").upper()

            latest_rec_df['min_price'] = latest_rec_df.groupby('symbol')['close_price'].transform('min')
            latest_rec_df['max_price'] = latest_rec_df.groupby('symbol')['close_price'].transform('max')
            latest_rec_df['up_pot'] = (latest_rec_df['max_price'] - latest_rec_df['close_price'])*100 / latest_rec_df['close_price']
            latest_rec_df['up_pot'] = latest_rec_df['up_pot'].round(0)
            latest_rec_df['dec_pct'] = (latest_rec_df['max_price'] - latest_rec_df['close_price'])*100 / latest_rec_df['max_price']
            latest_rec_df['dec_pct'] = latest_rec_df['dec_pct'].round(0)
            latest_rec_df = latest_rec_df.sort_values(by=['listing_year','up_pot'],ascending=[True,False])

            latest_rec_df = latest_rec_df[latest_rec_df['date_of_record']==max_date]
            latest_rec_df = latest_rec_df.drop(['date_of_record','date_of_listing'],axis=1)
            #return_values = [latest_rec_df, max_strf_date]
            
    return latest_rec_df, max_strf_date
