from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_remembered, login_required

dash_views = Blueprint('dash_views', __name__)


@dash_views.route('/dashboard')
@login_required
def dashboard():
    """ Dashboard """
    return render_template('dashboard/dashboard.html')


@dash_views.route('/dashboard/investigations')
@login_required
def click_investiagtions():
    """ Investigations """
    return redirect(url_for('inv_views.investigations_list'))
