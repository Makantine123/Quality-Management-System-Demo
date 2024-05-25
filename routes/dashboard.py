from flask import Blueprint, redirect, render_template, url_for

dash_views = Blueprint('dash_views', __name__)


@dash_views.route('/dashboard')
def dashboard():
    """ Dashboard """
    return render_template('dashboard/dashboard.html')


@dash_views.route('/dashboard/investigations')
def click_investiagtions():
    """ Investigations """
    #return render_template('index.html')
    return redirect(url_for('inv_views.investigations_list'))
