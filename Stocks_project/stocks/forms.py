from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class Wish_button_Form(FlaskForm):
    submit = SubmitField('AddToWishList')

class Add_to_Portfolio(FlaskForm):
    qty = IntegerField('Quantity', validators=[DataRequired()])
    buy_price = DecimalField('Buy Price', validators=[DataRequired()])
    submit_to_add = SubmitField('Add To Portfolio')
