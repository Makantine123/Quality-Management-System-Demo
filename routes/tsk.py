""" Investigations Routees """
from flask import Blueprint, render_template, flash, request, url_for, redirect
from models.investigations import Investigations
from models.investigations_details import InvestigationsDetails
from forms.investigations import InvestigationWithDetailsForm
from models.tasks import Tasks
from models.tasks_details import TaskDetails

tsk_views = Blueprint("tsk_views", __name__)


@tsk_views.route('/investigations/<id>/task/new')
def create_task_by_investiagtion_id(id):
    """ Show Investigation by id """
    task = {}
    task["investigation_id"] = id
    taskdetails = {}
    taskdetails["investigation_id"] = id
    return render_template(
        'dashboard/investigations/investigations_tasks.html',
        task=task, taskdetails=taskdetails)

@tsk_views.route('/investigation/<id>/task/goback')
def go_back_to_investigation_details(id):
    """ Return back to investigation details page """
    from app import Session
    db = Session()

    investigation = db.query(Investigations).filter_by(id=id).first()
    ir_number = investigation.ir_number

    return redirect(url_for(
        'inv_views.investigation_details', ir_number=ir_number))


@tsk_views.route('/investigation/task/save', methods=['POST', 'GET'])
def save_task():
    """ Save Task """
    form = request.form
    from app import Session
    db = Session()
    task_id = form.get('id')
    task = db.query(Tasks).filter_by(id=task_id).first()
    if task is None:
        task = Tasks(
            task_type=form.get('task_type'),
            status=form.get('status'),
            description=form.get('description'),
            assign_to=form.get('assign_to'),
            due_date=form.get('due_date'),
            investigation_id=form.get('investigation_id')
        )
        task.due_date = task.from_datetime_string(form.get('due_date'))
        db.add(task)
        details = TaskDetails()
        details.task_id = task.id
    else:
        task.task_type = form.get('task_type')
        task.status = form.get('status')
        task.description = form.get('description')
        task.assign_to = form.get('assign_to')
        task.investigation_id = form.get('investigation_id')
        task.due_date = task.from_datetime_string(form.get('due_date'))

    task_id = task.id
    db.commit()
    db.close()

    return redirect(url_for('tsk_views.task_by_id', id=task_id))


@tsk_views.route('/tasks/<id>')
def task_by_id(id):
    """ Show task by id """
    from app import Session
    db = Session()

    task = db.query(Tasks).filter_by(id=id).first()
    taskdetails = db.query(TaskDetails).filter_by(id=id).order_by(
        desc(TaskDetails.date_created_on)).first()
    return render_template(
        '/dashboard/investigations/investigations_tasks.html',
        task=task, taskdetails=taskdetails)





















