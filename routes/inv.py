""" Investigations Routees """
from operator import inv
from flask import Blueprint, render_template, flash, request, url_for, redirect
from sqlalchemy import desc
from sqlalchemy.util import duck_type_collection, unbound_method_to_callable
from models.investigations import Investigations
from models.investigations_details import InvestigationsDetails
from models.tasks import Tasks
from forms.investigations import InvestigationWithDetailsForm

inv_views = Blueprint("inv_views", __name__)


@inv_views.route('/investigations')
def investigations_list():
    """ Render Investigations Lists Template """
    from app import Session
    db = Session()
    investigations = db.query(Investigations).filter(Investigations.status!="Rejected").all()
    print(investigations)
    return render_template('dashboard/investigations/investigations.html',
                           investigations=investigations)


@inv_views.route('/investigations/<ir_number>', methods=['POST', 'GET'])
def investigation_details(ir_number):
    """ Render Template With Investigation and its details """
    from app import Session
    db = Session()
    investigation = db.query(Investigations).filter_by(
        ir_number=ir_number).first()
    details = db.query(InvestigationsDetails).filter_by(
        investigation_id=investigation.id).order_by(
        desc(InvestigationsDetails.date_created_on)).first()
    detailslist = db.query(InvestigationsDetails).filter_by(
        investigation_id=investigation.id).all()
    tasklist = db.query(Tasks).filter_by(
        investigation_id=investigation.id).all()
    db.close()
    if details is None:
        details = {}
        details['investigation_id'] = investigation.id
    return render_template(
            'dashboard/investigations/investigations_details.html',
            investigations=investigation, details=details,
            detailslist=detailslist, taskslist=tasklist)


@inv_views.route('/investigations/<ir_number>/delete', methods=['POST', 'GET'])
def delete_investigation(ir_number):
    """ Soft Deletes Investigation by ir_number """
    from app import Session
    db = Session()
    investigation = db.query(Investigations).filter_by(
        ir_number=ir_number).first()
    if investigation:
        investigation.status = "Rejected"
        db.commit()
    return redirect(url_for('inv_views.investigations_list'))


@inv_views.route('/investigations/save_new', methods=['GET', 'POST'])
def new_investigation():
    """ Save new investigation """
    form = request.form
    from app import Session
    db = Session()
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
        investigation.due_date = investigation.from_datetime_string(form.get('due_date'))

    ir_number = investigation.ir_number
    db.commit()

    db.close()
    return redirect(url_for('inv_views.investigation_details',
                            ir_number=ir_number))


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
        details.due_date = details.from_datetime_string(form.get('due_date'))
        db.add(details)
    else:
        details.steps_required = form.get('steps_required')
        details.by_who = form.get('by_who')
        details.main_causes = form.get('main_causes')
        details.investigation_id = form.get('investigation_id')
        details.status = form.get('status')
        details.due_date = details.from_datetime_string(form.get('due_date'))

    db.commit()

    inv_id = details.investigation_id
    investigation = db.query(Investigations).filter_by(
        id=inv_id).first()
    ir_number = investigation.ir_number
    db.close()

    return redirect(url_for('inv_views.investigation_details',
                            ir_number=ir_number))


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
    detailslist = db.query(InvestigationsDetails).filter_by(
        investigation_id=inv_id).all()
    tasklist = db.query(Tasks).filter_by(
        investigation_id=inv_id).all()
    db.close()
    if details is None:
        details = {}
        details['investigation_id'] = investigation.id
    return render_template(
            'dashboard/investigations/investigations_details.html',
            investigations=investigation, details=details,
            detailslist=detailslist, taskslist=tasklist)


@inv_views.route('/investigation/details/<id>', methods=['POST', 'GET'])
def investigation_details_by_id(id):
    """ Fetch investigation details by id """
    from app import Session
    db = Session()
    details = db.query(InvestigationsDetails).filter_by(id=id).first()
    investigation_id = details.investigation_id
    investigation = db.query(Investigations).filter_by(id=investigation_id).first()
    detailslist = db.query(InvestigationsDetails).filter_by(investigation_id=investigation_id).all()
    tasklist = db.query(Tasks).filter_by(investigation_id=investigation_id).all()

    return render_template(
            'dashboard/investigations/investigations_details.html',
            investigations=investigation, details=details,
            detailslist=detailslist, taskslist=tasklist)

