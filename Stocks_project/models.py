from Stocks_project import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'site_users'

    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    src_id = db.Column(db.Integer, default = 1)

    user_wishes = db.relationship('User_Wishlist', backref='uw_uid', lazy='dynamic')
    user_stocks = db.relationship('User_Portfolio', backref='up_uid', lazy='dynamic')


    def __init__(self, user_id, user_name, password):
        self.user_id = user_id
        self.user_name = user_name
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.user_name}"

    def get_id(self):
           return (self.user_id)

class Stock_Info(db.Model):
    __tablename__ = 'nse_stock_info_1'

    symbol = db.Column(db.String(30), primary_key = True)
    name_of_company = db.Column(db.String(1000))
    series = db.Column(db.String(2))
    date_of_listing = db.Column(db.Date)
    paid_up_value = db.Column(db.Integer)
    market_lot = db.Column(db.Integer)
    isin_number = db.Column(db.String(12))
    face_value = db.Column(db.Integer)
    industry = db.Column(db.String(100))
    nifty_500_ind = db.Column(db.String(1))

    daily_price = db.relationship('All_Stocks', backref='s_info', lazy='dynamic')
    stock_wishes = db.relationship('User_Wishlist', backref='uw_sym', lazy='dynamic')
    user_portf = db.relationship('User_Portfolio', backref='up_sym', lazy='dynamic')

    def __init__(self, symbol, name_of_company, series, date_of_listing,
                paid_up_value, market_lot, isin_number, face_value, industry, nifty_500_ind):
            self.symbol = symbol
            self.name_of_company = name_of_company
            self.series = series
            self.date_of_listing = date_of_listing
            self.paid_up_value = paid_up_value
            self.market_lot = market_lot
            self.isin_number = isin_number
            self.face_value = face_value
            self.industry = industry
            self.nifty_500_ind = nifty_500_ind

    def __repr__(self):
            return f"Stock - {self.symbol} - {self.name_of_company} opened on {self.date_of_listing} with FV Rs. {self.face_value}"


class All_Stocks(db.Model):

    __tablename__ = 'stocks_nse_daily'

    symbol = db.Column(db.String(30), db.ForeignKey('nse_stock_info_1.symbol'), primary_key = True, index=True)
    date_of_record = db.Column(db.Date, primary_key = True, index=True)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    day_volume = db.Column(db.Integer)

    def __init__(self, symbol, date_of_record, open_price, high_price,
                low_price, close_price, day_volume):
            self.symbol = symbol
            self.date_of_record = date_of_record
            self.open_price = open_price
            self.high_price = high_price
            self.low_price = low_price
            self.close_price = close_price
            self.day_volume = day_volume

    def __repr__(self):
        return f"On {self.date_of_record} {self.symbol} closed at {self.close_price}"
        #return f"{self.close_price}"


class User_Wishlist(db.Model):
    __tablename__ = 'user_wishlist'

    user_id = db.Column(db.Integer, db.ForeignKey('site_users.user_id'), primary_key = True, index=True)
    symbol = db.Column(db.String(30), db.ForeignKey('nse_stock_info_1.symbol'), primary_key = True, index=True)

    def __init__(self, user_id, symbol):
        self.user_id = user_id
        self.symbol = symbol

    def __repr__(self):
        return f"User {self.user_id} wishes to track {self.symbol}"


class User_Portfolio(db.Model):
    __tablename__ = 'user_portfolio'

    user_id = db.Column(db.Integer, db.ForeignKey('site_users.user_id'), primary_key = True, index=True)
    symbol = db.Column(db.String(30), db.ForeignKey('nse_stock_info_1.symbol'), primary_key = True, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, symbol, quantity, buy_price):
        self.user_id = user_id
        self.symbol = symbol
        self.quantity = quantity
        self.buy_price = buy_price


    def __repr__(self):
        return f"User {self.user_id} holds {self.quantity} of {self.symbol} at Rs.{self.buy_price}/share"
