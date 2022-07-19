from flask import render_template, redirect, session, url_for, Blueprint, request
from Stocks_project import db
from Stocks_project.models import Stock_Info, All_Stocks
from Stocks_project.stocks.forms import Wish_button_Form

import pandas as pd
import requests
import os


stocks = Blueprint("stocks",__name__)

@stocks.route('/<string:stock_symbol>')
def stock_info(stock_symbol):
    print('stock_symbol: ',stock_symbol)
    name_of_company = 'XXXXXXXX'
    print('name_of_company: ',name_of_company)
    wish_button_form = Wish_button_Form()

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}.BSE&outputsize=full&apikey={os.getenv('API_KEY')}"
    r = requests.get(url)
    json_indv_stock_price = r.json()
    keys = reversed(json_indv_stock_price["Time Series (Daily)"].keys())
    new_dict = {x:json_indv_stock_price["Time Series (Daily)"][x]['4. close'] for x in keys}
    indv_stock_price_df = pd.DataFrame(list(new_dict.items()), columns=['date_of_record','close_price'])
    #max_strf_date = indv_stock_price_df.iloc[-1][0]
    print('indv_stock_price_df: ', indv_stock_price_df)



    #indv_stock = Stock_Info.query.get(stock_symbol)

    indv_stock_price = All_Stocks.query.filter_by(symbol = stock_symbol)
    indv_stock_price_tuple = ()
    indv_stock_price_list = []
    for company in indv_stock_price:
        indv_stock_price_tuple = (company.date_of_record,company.close_price)
        indv_stock_price_list.append(indv_stock_price_tuple)
    indv_stock_price_list.sort(key = lambda tup: tup[0])    #added on 07-MAY-2022 #To sort on date so that the graph comes out properly.
    #indv_stock_price_df = pd.DataFrame(indv_stock_price_list, columns=['date_of_record','close_price'])

    #return render_template("indv_stock.html",wish_button_form=wish_button_form,indv_stock=indv_stock,indv_stock_price_df=indv_stock_price_df)
    return render_template("indv_stock.html",wish_button_form=wish_button_form,stock_symbol=stock_symbol,name_of_company=name_of_company,indv_stock_price_df=indv_stock_price_df)
