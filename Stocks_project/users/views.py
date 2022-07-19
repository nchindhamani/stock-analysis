from flask import render_template, redirect, session, url_for, Blueprint, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from Stocks_project import db
from werkzeug.security import generate_password_hash,check_password_hash
from Stocks_project.models import User
from Stocks_project.users.forms import RegistrationForm, LoginForm


users_blueprint = Blueprint('users',__name__)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        #User.query.order_by(User.username).all() - example
        #user_max =
        all_user_id = db.session.query(User.user_id).all()
        if all_user_id == []:
            new_user_id = 1
        else:
            new_user_id = max(all_user_id)[0]+1
        user = User(new_user_id,
                    user_name=form.user_name.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(user_name=form.user_name.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)


            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.show_portfolio')

            return redirect(next)
        else:
            flash("Incorrect UserName/Password")
    return render_template('login.html', form=form)




@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.first'))



#THere is no link to show account profile as I dont have anything else to show
#other than user_name. If we add First Name, Last Name, etc, then we need to add that.
