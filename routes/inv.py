""" Investigations Routees """
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required
from sqlalchemy import desc
from models.investigations import Investigations
from models.investigations_details import InvestigationsDetails
from models.tasks import Tasks

inv_views = Blueprint("inv_views", __name__)


@inv_views.route('/investigations')
@login_required
def investigations_list():
    """ Render Investigations Lists Template """
    from app import Session
    db = Session()
    try:
        investigations = db.query(Investigations).filter(
            Investigations.status != "Rejected").all()
        return render_template('dashboard/investigations/investigations.html',
                               investigations=investigations)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@inv_views.route('/investigations/<ir_number>', methods=['POST', 'GET'])
@login_required
def investigation_details(ir_number):
    """ Render Template With Investigation and its details """
    from app import Session
    db = Session()
    try:
        investigation = db.query(Investigations).filter_by(
            ir_number=ir_number).first()
        if not investigation:
            return render_template('404.html'), 404
        details = db.query(InvestigationsDetails).filter_by(
            investigation_id=investigation.id).order_by(
            desc(InvestigationsDetails.date_created_on)).first()
        detailslist = db.query(InvestigationsDetails).filter(
            InvestigationsDetails.investigation_id == investigation.id,
            InvestigationsDetails.status != "Rejected").all()
        tasklist = db.query(Tasks).filter(
            Tasks.investigation_id == investigation.id,
            Tasks.status != "Rejected").all()
        if details is None:
            details = {}
            details['investigation_id'] = investigation.id
        return render_template(
                'dashboard/investigations/investigations_details.html',
                investigations=investigation, details=details,
                detailslist=detailslist, taskslist=tasklist)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@inv_views.route('/investigations/<ir_number>/delete', methods=['POST', 'GET'])
@login_required
def delete_investigation(ir_number):
    """ Soft Deletes Investigation by ir_number """
    from app import Session
    db = Session()
    try:
        investigation = db.query(Investigations).filter_by(
            ir_number=ir_number).first()
        if investigation:
            investigation.status = "Rejected"
            db.commit()
        return redirect(url_for('inv_views.investigations_list'))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@inv_views.route('/investigations/save_new', methods=['GET', 'POST'])
def new_investigation():
    """ Save new investigation """
    form = request.form
    from app import Session
    db = Session()
    try:
        inv_id = form.get('id')
        investigation = db.query(Investigations).filter_by(id=inv_id).first()
        if investigation is None:
            investigation = Investigations(
                raised_by=form.get('raised_by'),
                status=form.get('status'),
                priority=form.get('priority'),
                ir_source=form.get('ir_source'),
                line_manager=form.get('line_manager'),
                description=form.get('description'),
                root_cause_summary=form.get('root_cause_summary'),
                team_leader=form.get('team_leader'),
                due_date=form.get('due_date'),
            )
            investigation.ir_number = investigation.generate_ir_no()
            investigation.due_date = investigation.from_datetime_string(
                form.get('due_date'))
            db.add(investigation)
            details = InvestigationsDetails()
            details.investigation_id = investigation.id
        else:
            investigation.raised_by = form.get('raised_by')
            investigation.status = form.get('status')
            investigation.priority = form.get('priority')
            investigation.ir_source = form.get('ir_source')
            investigation.line_manager = form.get('line_manager')
            investigation.description = form.get('description')
            investigation.root_cause_summary = form.get('root_cause_summary')
            investigation.team_leader = form.get('team_leader')
            investigation.due_date = investigation.from_datetime_string(
                form.get('due_date'))

        ir_number = investigation.ir_number
        db.commit()
        return redirect(url_for('inv_views.investigation_details',
                                ir_number=ir_number))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@inv_views.route('/investigations/create', methods=['GET', 'POST'])
def create_investigation():
    """ Create a new Investigation """
    investigations = []
    details = InvestigationsDetails()
    return render_template(
        'dashboard/investigations/investigations_details.html',
        investigations=investigations, details=details)


@inv_views.route('/investigation_detail/save', methods=['POST', 'GET'])
def save_investigation_detail():
    """ Save investigation detail """
    form = request.form
    from app import Session
    db = Session()
    try:
        inv_detail_id = form.get('id')
        details = db.query(InvestigationsDetails).filter_by(
            id=inv_detail_id).first()
        if details is None:
            details = InvestigationsDetails(
                steps_required=form.get('steps_required'),
                by_who=form.get('by_who'),
                main_causes=form.get('main_causes'),
                investigation_id=form.get('investigation_id'),
                status=form.get('status'),
            )
            details.due_date = details.from_datetime_string(
                form.get('due_date'))
            db.add(details)
        else:
            details.steps_required = form.get('steps_required')
            details.by_who = form.get('by_who')
            details.main_causes = form.get('main_causes')
            details.investigation_id = form.get('investigation_id')
            details.status = form.get('status')
            details.due_date = details.from_datetime_string(
                form.get('due_date'))

        db.commit()

        inv_id = details.investigation_id
        investigation = db.query(Investigations).filter_by(
            id=inv_id).first()
        ir_number = investigation.ir_number

        return redirect(url_for('inv_views.investigation_details',
                                ir_number=ir_number))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@inv_views.route('/investigations/<id>/task')
def add_investigation_task(id):
    """ Add Task to Investigation """
    return redirect(url_for('tsk_views.create_task_by_investiagtion_id',
                            id=id))


@inv_views.route('/task/<id>/delete', methods=['POST', 'GET'])
def delete_task(id):
    """ Soft delete Task by id """
    from app import Session
    db = Session()
    try:
        task = db.query(Tasks).filter_by(id=id).first()
        if task:
            task.status = "Rejected"
            db.commit()

        inv_id = task.investigation_id

        investigation = db.query(Investigations).filter_by(
            id=inv_id).first()
        details = db.query(InvestigationsDetails).filter_by(
            investigation_id=inv_id).order_by(
            desc(InvestigationsDetails.date_created_on)).first()
        detailslist = db.query(InvestigationsDetails).filter(
            InvestigationsDetails.investigation_id == inv_id,
            InvestigationsDetails.status != "Rejected").all()
        tasklist = db.query(Tasks).filter(
            Tasks.investigation_id == inv_id, Tasks.status != "Rejected").all()
        if details is None:
            details = {}
            details['investigation_id'] = investigation.id
        return render_template(
                'dashboard/investigations/investigations_details.html',
                investigations=investigation, details=details,
                detailslist=detailslist, taskslist=tasklist)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@inv_views.route('/investigation/details/<id>', methods=['POST', 'GET'])
def investigation_details_by_id(id):
    """ Fetch investigation details by id """
    from app import Session
    db = Session()
    try:
        details = db.query(InvestigationsDetails).filter_by(id=id).first()
        investigation_id = details.investigation_id
        investigation = db.query(Investigations).filter_by(
            id=investigation_id).first()
        detailslist = db.query(InvestigationsDetails).filter(
            InvestigationsDetails.investigation_id == investigation_id,
            InvestigationsDetails.status != "Rejected").all()
        tasklist = db.query(Tasks).filter(
            Tasks.investigation_id == investigation_id,
            Tasks.status != "Rejected").all()

        return render_template(
                'dashboard/investigations/investigations_details.html',
                investigations=investigation, details=details,
                detailslist=detailslist, taskslist=tasklist)
    except Exception as e:
        raise e
    finally:
        db.close()
