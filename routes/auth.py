#!/usr/bin/python3
"""Login and Signin routes"""
from flask import Blueprint, flash, request, render_template, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from config import Config
from models.users import Users

auth_views = Blueprint('auth_views', __name__)

github_blueprint = make_github_blueprint(client_id=Config.GITHUB_CLIENT_ID,
                                         client_secret=Config.GITHUB_SECRET,
                                         authorized_url='/github/callback')
google_blueprint = make_google_blueprint(client_id=Config.GOOGLE_CLIENT_ID,
                                         client_secret=Config.GOOGLE_SECRET,
                                         redirect_to='google.login',
                                         authorized_url='/google/callback')


@auth_views.route('/login', methods=['GET', 'POST'])
def standard_login():
    """Login method"""
    loginform = request.form
    email = loginform.get('email')
    password = loginform.get('password')

    from app import Session
    db = Session()
    user = db.query(Users).filter_by(email=email).first()

    if not user:
        flash('Oops! User does not exist!', 'error')
        return

    if user.check_password(user.password_hsh, password):
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dash_views.dashboard'))

    flash('Oops! Email and Password do not match!', 'error')
    return redirect(url_for('home'))

    return render_template('dashboard/dashboard.html')


@auth_views.route('/github_login')
def github_login():
    """ Login Using GitHub """
    if not github.authorized:
        return redirect(url_for('github.login'))


@auth_views.route('/google_login')
def google_login():
    """ Login Using Google """
    if not google.authorized:
        return redirect(url_for('google.login'))


@auth_views.route('/github_signup')
def gethub_signup():
    """ User signup using GitHub """


@auth_views.route('/google_signup')
def google_signup():
    """ User signup using Google """


@auth_views.route('/signup', methods=['POST'])
def standard_signup():
    """ User signup using standard method """
    if request.method == 'POST':
        signupform = request.form
        if signupform:
            name = signupform.get('name')
            surname = signupform.get('surname')
            email = signupform.get('email')
            password = signupform.get('password')

            from app import Session
            # Create Instance of Factory Session
            db = Session()
            # Check if user already exists
            users = db.query(Users).filter_by(email=email).first()
            if users:
                flash('Users already exits, please sign in')
                return redirect(url_for('home'))

            newUser = Users()
            newUser.name = name
            newUser.surname = surname
            newUser.email = email
            newUser.password_hsh = password
            newUser.standard_signup = 'Y'

            try:
                db.add(newUser)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
            print(newUser.as_dict())
            flash('Successfuly Registerd!! Please login')
            return redirect(url_for('home'))
    return render_template('home')


@auth_views.route('/google/callback')
def google_authorization():
    """ Google Authorization Callback """
    pass


@auth_views.route('/github/callback')
def github_authorization():
    """ GitHub Authorization Callback """
    pass
