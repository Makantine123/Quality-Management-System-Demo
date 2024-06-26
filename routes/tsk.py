""" Investigations Routees """
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required
from sqlalchemy import desc
from sqlalchemy.sql.functions import rollup
from models.investigations import Investigations
from models.tasks import Tasks
from models.tasks_details import TaskDetails

tsk_views = Blueprint("tsk_views", __name__)


@tsk_views.route('/investigations/<id>/task/new')
@login_required
def create_task_by_investiagtion_id(id):
    """ Show Investigation by id """
    from app import Session
    db = Session()
    try:
        task = {}
        task["investigation_id"] = id
        taskslist = db.query(Tasks).filter(Tasks.investigation_id == id,
                                           Tasks.status != "Rejected").all()
        taskdetails = {}
        taskdetails["investigation_id"] = id
        taskdetailslist = db.query(TaskDetails).filter(
            TaskDetails.investigation_id == id,
            TaskDetails.status != "Rejected").all()
        return render_template(
            'dashboard/investigations/investigations_tasks.html',
            task=task, taskdetails=taskdetails, taskslist=taskslist,
            taskdetailslist=taskdetailslist)
    except Exception as e:
        raise e
    finally:
        db.close()


@tsk_views.route('/investigation/<id>/task/goback')
@login_required
def go_back_to_investigation_details(id):
    """ Return back to investigation details page """
    from app import Session
    db = Session()
    try:
        investigation = db.query(Investigations).filter_by(id=id).first()
        ir_number = investigation.ir_number

        return redirect(url_for(
            'inv_views.investigation_details', ir_number=ir_number))
    except Exception as e:
        raise e
    finally:
        db.close()


@tsk_views.route('/investigation/task/save', methods=['POST', 'GET'])
@login_required
def save_task():
    """ Save Task """
    form = request.form
    from app import Session
    db = Session()
    try:
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

        db.commit()
        task_id = task.id
        return redirect(url_for('tsk_views.task_by_id', id=task_id))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@tsk_views.route('/tasks/<id>')
@login_required
def task_by_id(id):
    """ Show task by id """
    from app import Session
    db = Session()
    try:
        task = db.query(Tasks).filter_by(id=id).first()
        inv_id = task.investigation_id
        taskslist = db.query(Tasks).filter(Tasks.investigation_id == inv_id,
                                           Tasks.status != "Rejected").all()
        taskdetails = db.query(TaskDetails).filter(
            TaskDetails.task_id == id, Tasks.status != "Rejected").order_by(
            desc(TaskDetails.date_created_on)).first()
        taskdetailslist = db.query(TaskDetails).filter(
            TaskDetails.task_id == id,
            TaskDetails.status != "Rejected").order_by(
            desc(TaskDetails.date_created_on)).all()
        if taskdetails is None:
            taskdetails = {}
            taskdetails['task_id'] = task.id
            taskdetails['investigation_id'] = task.investigation_id
        return render_template(
            '/dashboard/investigations/investigations_tasks.html',
            task=task, taskdetails=taskdetails,
            taskdetailslist=taskdetailslist,
            taskslist=taskslist)
    except Exception as e:
        raise e
    finally:
        db.close()


@tsk_views.route('/investigation_task/detail/save', methods=['POST', 'GET'])
@login_required
def save_investigation_task_detail():
    """ Save Investigation Task Detail """
    form = request.form
    file = request.files.get('attachment_name')
    from app import Session
    db = Session()
    try:
        tsk_detail_id = form.get('id')
        details = db.query(TaskDetails).filter_by(id=tsk_detail_id).first()
        if details is None:
            details = TaskDetails(
                task_id=form.get('task_id'),
                investigation_id=form.get('investigation_id'),
                status=form.get('status'),
                attachment_comments=form.get('attachment_comments'),
                feedback=form.get('feedback'),
            )
            if file:
                details.attachment_name = file

            if form.get('date_completed_on') is not None:
                details.date_completed_on = details.from_datetime_string(
                    form.get('date_completed_on'))
            db.add(details)
        else:
            details.task_id = form.get('task_id')
            details.investigation_id = form.get('investigation_id')
            details.status = form.get('status')
            details.date_completed_on = form.get('date_completed_on')
            if file:
                details.attachment_name = file
            details.attachment_comments = form.get('attachment_comments')
            details.feedback = form.get('feedback')
            if form.get('date_completed_on') is not None:
                details.date_completed_on = details.from_datetime_string(
                    form.get('date_completed_on'))

        db.commit()

        tsk_id = details.task_id

        return redirect(url_for('tsk_views.task_by_id', id=tsk_id))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@tsk_views.route('/task/details/<id>')
@login_required
def task_details_by_id(id):
    """ Fetch Task deatils by id """
    from app import Session
    db = Session()
    try:
        taskdetails = db.query(TaskDetails).filter_by(id=id).first()
        taskdetailslist = db.query(TaskDetails).filter(
            TaskDetails.id == id, TaskDetails.status != "Rejected").all()
        task_id = taskdetails.task_id
        inv_id = taskdetails.investigation_id
        task = db.query(Tasks).filter_by(id=task_id).first()
        taskslist = db.query(Tasks).filter(
            Tasks.investigation_id == inv_id, Tasks.status != "Rejected").all()

        return render_template(
            '/dashboard/investigations/investigations_tasks.html',
            task=task, taskdetails=taskdetails,
            taskdetailslist=taskdetailslist,
            taskslist=taskslist)
    except Exception as e:
        raise e
    finally:
        db.close()


@tsk_views.route('/task/details/<id>/delete', methods=['POST', 'GET'])
@login_required
def delete_task_details(id):
    """ Soft Deletes Task details by id """
    from app import Session
    db = Session()
    try:
        taskdetails = db.query(TaskDetails).filter_by(
            id=id).first()
        task_id = taskdetails.task_id
        if taskdetails:
            taskdetails.status = "Rejected"
            db.commit()
        return redirect(url_for('tsk_views.task_by_id', id=task_id))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
