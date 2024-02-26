from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


# User login. 
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user_email = data["email"]
        user_password = data["password"]
        
        user = User.query.filter_by(email=user_email).first()
        if user:
            # user exists and password is correct
            if check_password_hash(user.password, user_password):
                flash('Logged in successfuly!')
                login_user(user, remember=True)
                return redirect(url_for("views.userhome"))
            else:
                flash('Password is incorrect!', category='error')
                # password is wrong
        else:
            # email does not exist
            flash('Email does not exist! Enter a correct email or create an account.', category='error')

    return render_template('login.html', user=current_user)


## User create a new account.
@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        user_email = data["email"]
        user_name = data['name']
        user_password = data["password"]

        # email, name, or password is too short
        if len(user_email) < 1 or len(user_name) < 1 or len(user_password) < 1:
            flash('Enter valid details.', category='error')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(email=user_email).first()
        # email already exists
        if (user):
            flash('Email already exists! Sign up with a new email or login with your existing email.', category='error')
            return redirect(url_for('auth.signup'))
        else:
            new_user = User(email=user_email, name=user_name, password=generate_password_hash(user_password, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            flash('Created account successfuly! You are now logged in.', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for("views.userhome"))
        
    return render_template('signup.html', user=current_user)


# User logout.
@auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfuly!', category='success')
    return redirect(url_for('auth.login'))
