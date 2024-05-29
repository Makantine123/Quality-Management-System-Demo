""" Investigations Routees """
from flask import Blueprint, render_template, flash, url_for, redirect
from models.investigations import Investigations
from models.investigations_details import InvestigationsDetails
from forms.investigations import InvestigationWithDetailsForm

tsk_views = Blueprint("tsk_views", __name__)


@tsk_views.route('/investigations/<id>/task/new')
def create_task_by_investiagtion_id(id):
    """ Show Investigation by id """
    return render_template('')
