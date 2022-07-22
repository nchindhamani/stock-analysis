__author__ = 'Chindhamani'

import os        #Code Change on 06-MAY-2022
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate     #Code Change on 06-MAY-2022

app = Flask(__name__)

#Commenting on 06-MAY-2022
#app.config['SECRET_KEY'] = 'mysecretkey'
#app.config['SQLALCHEMY_DATABASE_URI'] = "oracle://stock_proj:tata123@127.0.0.1:1521/xe"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

#Commenting on 06-MAY-2022 ends
#Code Change on 06-MAY-2022 starts
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = f"{os.getenv('SECRET_KEY')}"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

#Code Change on 06-MAY-2022 ends



#######################
#### LOGIN CONFIGS ####
#######################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"

###########################
#### BLUEPRINT CONFIGS ####
###########################
from Stocks_project.core.views import core
from Stocks_project.users.views import users_blueprint
from Stocks_project.stocks.views import stocks


app.register_blueprint(core)
app.register_blueprint(users_blueprint)
app.register_blueprint(stocks)
