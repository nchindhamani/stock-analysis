from flask import render_template, redirect, Blueprint, url_for, request, session, flash
from flask_login import current_user,login_required
from Stocks_project.models import All_Stocks, Stock_Info, User_Wishlist, User_Portfolio
from Stocks_project.stocks.forms import Wish_button_Form, Add_to_Portfolio
from Stocks_project.core.forms import Industry_DD_Form
from Stocks_project.functions import f_stock_valuation
from Stocks_project import db

from datetime import datetime as dt
import pandas as pd
import requests
import os


core = Blueprint('core',__name__)

@core.route('/',methods=['GET','POST'])
def first():

    import exchange_calendars as ec
    from nsepy import get_history
    from datetime import date, datetime as dt
    from nsepy.history import get_price_list

    if 'curr_session_dt' not in session:
        str_curr_session_dt = date.today().isoformat()
        xbom = ec.get_calendar("XBOM")

        if not xbom.is_session(str_curr_session_dt):
            str_curr_session_dt = xbom.previous_close(str_curr_session_dt)
        print('str_curr_session_dt in homepage:', str_curr_session_dt)

        session['curr_session_dt'] = str_curr_session_dt


    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NIFTYBEES.BSE&outputsize=full&apikey={os.getenv('API_KEY')}"
    r = requests.get(url)
    json_niftybees = r.json()
    keys = reversed(json_niftybees["Time Series (Daily)"].keys())
    new_dict = {x:json_niftybees["Time Series (Daily)"][x]['4. close'] for x in keys}
    nifty_index_df = pd.DataFrame(list(new_dict.items()), columns=['date_of_record','close_price'])
    max_strf_date = nifty_index_df.iloc[-1][0]
    index_name = "NIFTYBEES"
    #print('nifty_index_df: ',nifty_index_df)
    return render_template('first.html',max_strf_date=max_strf_date, nifty_index_df = nifty_index_df, index_name=index_name)



@core.route('/AllNSEStocks',methods=['GET','POST'])
def index():
    df_stock_info = pd.read_pickle("./stock_info_bse.pkl")
    unique_industry_list = df_stock_info["INDUSTRY"].unique()
    new_unique_industry_list = []

    for industry in unique_industry_list:
        new_unique_industry_list.append((industry,industry))

    wish_button_form = Wish_button_Form()
    industry_dd_form = Industry_DD_Form()
    industry_dd_form.industry_dd.choices = new_unique_industry_list

    if industry_dd_form.validate_on_submit():
        print(f"Selected Industry is: {industry_dd_form.industry_dd.data}")

        df_stock_info = df_stock_info[df_stock_info["INDUSTRY"]==industry_dd_form.industry_dd.data]

    if 'curr_session_dt' in session:
        str_curr_session_dt = dt.strptime(session['curr_session_dt'],'%Y-%m-%d');

    from nsepy.history import get_price_list
    df_daily_bhav = get_price_list(dt=str_curr_session_dt)


    df_daily_bhav['Change %'] = (df_daily_bhav.CLOSE - df_daily_bhav.PREVCLOSE)/100
    #print('df_daily_bhav: ',df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
    df_daily_bhav = df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

    result = pd.merge(df_stock_info, df_daily_bhav, how='inner', on = 'ISIN')
    #print(result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
    latest_rec_df = result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

    max_strf_date = session['curr_session_dt']

    #print('max_strf_date: ',max_strf_date)
    #print('latest_rec_df: ',latest_rec_df)

    return render_template('home.html',max_strf_date=max_strf_date, latest_rec_df=latest_rec_df, wish_button_form = wish_button_form,industry_dd_form=industry_dd_form)


@core.route('/<string:symbol>/wishlist')
@login_required
def add_wishlist(symbol):
    print("In add_wishlist")
    #symbol = request.form.get("symbol")
    print(f"To add wishlist, symbol is {symbol}")
    print(f"Current user is {current_user.user_id}")
    #Code change done on 17-JUL-2022
    #To check if stock already exists in wishlist
    flag_already_exists = False
    user_stocks = User_Wishlist.query.filter_by(user_id=current_user.user_id)
    for stk in user_stocks:
        if symbol == stk.symbol:
            flag_already_exists = True
    print('flag_already_exists in add_wishlist',flag_already_exists)
    #if flag_already_exists:
    #    pass
    if not flag_already_exists:
        #Code change ends here


        user_wish = User_Wishlist(current_user.user_id,
                                  symbol)

        db.session.add(user_wish)
        db.session.commit()

    return redirect(url_for('core.show_wishlist'))

@core.route('/<string:stock_symbol>/DeleteWishlist',methods=['GET','POST'])
@login_required
def del_wish_stocks(stock_symbol):
    del_wish_stk = User_Wishlist.query.get((current_user.user_id,stock_symbol))
    #print (del_portf_stk)
    db.session.delete(del_wish_stk)
    db.session.commit()
    return redirect(url_for('core.show_wishlist'))


@core.route('/ShowWishlist')
@login_required
def show_wishlist():

    df_stock_info = pd.read_pickle("./stock_info_bse.pkl")
    user_stocks = User_Wishlist.query.filter_by(user_id=current_user.user_id)
    #print('user_stocks (show_wishlist) : ',user_stocks)
    list_user_symbol = []
    for stk in user_stocks:
        list_user_symbol.append(stk.symbol)
    print(list_user_symbol)

    if 'curr_session_dt' in session:
        str_curr_session_dt = dt.strptime(session['curr_session_dt'],'%Y-%m-%d');

    from nsepy.history import get_price_list
    df_daily_bhav = get_price_list(dt=str_curr_session_dt)


    df_daily_bhav['Change %'] = (df_daily_bhav.CLOSE - df_daily_bhav.PREVCLOSE)/100
    #print('df_daily_bhav: ',df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
    df_daily_bhav = df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

    result = pd.merge(df_stock_info, df_daily_bhav, how='inner', on = 'ISIN')
    #print(result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
    latest_rec_df = result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

    max_strf_date = session['curr_session_dt']
    print('max_strf_date in show_wishlist:',max_strf_date)
    print('latest_rec_df in show_wishlist:',latest_rec_df)

    df_user_stock = pd.DataFrame(columns=['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %'])
    for item in list_user_symbol:
        df_user_stock = pd.concat([df_user_stock,latest_rec_df[latest_rec_df['SYMBOL_x']==item][['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]],ignore_index=True)

    print('df_user_stock in show_wishlist \n',df_user_stock)
    latest_rec_df = df_user_stock

    #all_user_stocks = All_Stocks.query.filter(All_Stocks.symbol.in_(list_user_symbol)).all()
    #latest_rec_df,max_strf_date = f_stock_valuation (all_user_stocks)

    return render_template("wishlist.html",latest_rec_df=latest_rec_df,max_strf_date=max_strf_date )


@core.route('/<string:stock_symbol>/AddToPortfolio',methods=['GET','POST'])
@login_required
def add_portfolio(stock_symbol):
    portfolio_form = Add_to_Portfolio()
    flag_already_exists = False
    if portfolio_form.validate_on_submit():

        #Code change on 07-MAY-2022
        #To check if the stock already exists in the portfolio
        user_portf_stocks = User_Portfolio.query.filter_by(user_id=current_user.user_id)
        for stk in user_portf_stocks:
            if stock_symbol == stk.symbol:
                flag_already_exists = True
        print('flag_already_exists in add_portfolio',flag_already_exists)
        if flag_already_exists:
            flash("Stock already exists in Portfolio")
        else:
        #Code change ends here

            add_stock = User_Portfolio(user_id=current_user.user_id,
                         symbol=stock_symbol,
                         quantity=portfolio_form.qty.data,
                         buy_price=portfolio_form.buy_price.data,
                         )
            db.session.add(add_stock)
            db.session.commit()
            return redirect(url_for('core.show_portfolio'))

    return render_template("add_to_portfolio.html",portfolio_form=portfolio_form,stock_symbol=stock_symbol)

@core.route('/<string:stock_symbol>/UpdatePortfolio',methods=['GET','POST'])
@login_required
def upd_portf_stocks(stock_symbol):
    upd_portf_stk = User_Portfolio.query.get((current_user.user_id,stock_symbol))
    db.session.delete(upd_portf_stk)
    db.session.commit()
    return redirect(url_for('core.add_portfolio',stock_symbol=stock_symbol))

@core.route('/<string:stock_symbol>/DeletePortfolio',methods=['GET','POST'])
@login_required
def del_portf_stocks(stock_symbol):
    del_portf_stk = User_Portfolio.query.get((current_user.user_id,stock_symbol))
    #print (del_portf_stk)
    db.session.delete(del_portf_stk)
    db.session.commit()
    return redirect(url_for('core.show_portfolio'))

@core.route('/ShowPortfolio')
@login_required
def show_portfolio():
    user_portf_stocks = User_Portfolio.query.filter_by(user_id=current_user.user_id)
    list_user_symbol = []
    for stk in user_portf_stocks:
        list_user_symbol.append(stk.symbol)
    print('list_user_symbol in Show Portfolio: ',list_user_symbol)

    if 'curr_session_dt' in session:
        max_strf_date = session['curr_session_dt']
        str_curr_session_dt = dt.strptime(session['curr_session_dt'],'%Y-%m-%d');


    from nsepy.history import get_price_list
    df_daily_bhav = get_price_list(dt=str_curr_session_dt)
    print('df_daily_bhav in show_portfolio', df_daily_bhav)

    df_user_stock = pd.DataFrame(columns=['SYMBOL','CLOSE'])
    for item in list_user_symbol:
        df_user_stock = pd.concat([df_user_stock,df_daily_bhav[df_daily_bhav['SYMBOL']==item][['SYMBOL','CLOSE']]],ignore_index=True)
    df_user_stock.columns=['symbol','close_price']
    print('df_user_stock \n',df_user_stock)

    rec_tuple = ()
    rec_list = []
    for company in user_portf_stocks:
        #rec_tuple = (company.symbol,company.up_sym.name_of_company, company.quantity, company.buy_price)
        rec_tuple = (company.symbol,company.symbol, company.quantity, company.buy_price)
        rec_list.append(rec_tuple)
    rec_df = pd.DataFrame(rec_list, columns=['symbol','name_of_company','quantity','buy_price'])
    portf_df = pd.merge(rec_df,df_user_stock, on='symbol', how='left')
    portf_df['buy_value'] = portf_df['buy_price'] * portf_df['quantity']
    portf_df['close_value'] = portf_df['close_price'] * portf_df['quantity']
    portf_df['profit'] = portf_df['close_value']  - portf_df['buy_value']
    portf_df['profit_pct'] = (portf_df['profit'] * 100 ) / portf_df['buy_value']
    #portf_df['profit_pct'] = portf_df['profit_pct'].round(decimals = 2)


    return render_template("portfolio.html",portf_df=portf_df,max_strf_date=max_strf_date)


@core.route('/api/<industry_name>/')
def api(industry_name):
    df_stock_info = pd.read_pickle("./stock_info_bse.pkl")
    df_stock_info = df_stock_info[df_stock_info["INDUSTRY"]==industry_name]

    if 'curr_session_dt' in session:
        str_curr_session_dt = dt.strptime(session['curr_session_dt'],'%Y-%m-%d');

    from nsepy.history import get_price_list
    df_daily_bhav = get_price_list(dt=str_curr_session_dt)


    df_daily_bhav['Change %'] = (df_daily_bhav.CLOSE - df_daily_bhav.PREVCLOSE)/100
    #print('df_daily_bhav: ',df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
    df_daily_bhav = df_daily_bhav[['SYMBOL', 'ISIN', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

    result = pd.merge(df_stock_info, df_daily_bhav, how='inner', on = 'ISIN')
    #print(result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']])
    latest_rec_df = result[['SYMBOL_x','NAME_OF_COMPANY', 'OPEN', 'HIGH', 'LOW','CLOSE', 'Change %']]

    max_strf_date = session['curr_session_dt']

    #print('max_strf_date: ',max_strf_date)
    #print('latest_rec_df: ',latest_rec_df)


    #latest_rec_df_2 = latest_rec_df.set_index('SYMBOL_x')
    #latest_rec_dict = latest_rec_df_2.to_dict(orient = 'index')
    latest_rec_dict = latest_rec_df.set_index('SYMBOL_x').to_dict(orient = 'index')
    #print('latest_rec_dict: ', latest_rec_dict)

    return latest_rec_dict
