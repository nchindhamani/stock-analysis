from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired

class Industry_DD_Form(FlaskForm):
    industry_dd = SelectField(u'Choose Industry:',
                          coerce=str, validators=[InputRequired()])
    submit = SubmitField('Get Stocks')
