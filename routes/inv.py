""" Investigations Routees """
from flask import Blueprint, render_template, flash, url_for, redirect
from models.investigations import Investigations
from models.investigations_details import InvestigationsDetails
from forms.investigations import InvestigationWithDetailsForm

inv_views = Blueprint("inv_views", __name__)


@inv_views.route('/investigations')
def investigations_list():
    """ Render Investigations Lists Template """
    from app import Session
    db = Session()
    investigations = db.query(Investigations).all()
    print(investigations)
    return render_template('dashboard/investigations/investigations.html',
                           investigations=investigations)


@inv_views.route('/investigations/<ir_number>', methods=['POST', 'GET'])
def investigation_details(ir_number):
    """ Render Template With Investigation and its details """
    from app import Session
    db = Session()
    if ir_number:
        details = db.query(InvestigationsDetails).all()
        investigation = db.query(Investigations).first()
        return render_template(
            'dashboard/investigations/investigations_details.html',
            investigations=investigation, details=details)

    return redirect(url_for('investigations_list'))


@inv_views.route('/investigations/new', methods=['GET', 'POST'])
def new_investigation():
    """ Save new investigation """
    form = InvestigationWithDetailsForm()

    if form.validate_on_submit():
        from app import Session
        db = Session()

        # Create Investigation
        investigation_data = form.investigation.data
        investigation = Investigations(**investigation_data)
        db.add(investigation)
        db.commit()

        # Create Investigation Details
        details_data = form.details.data
        for detail in details_data:
            detail['investigation_id'] = investigation.id
            investigation_detail = InvestigationsDetails(**detail)
            db.add(investigation_detail)

        db.commit()
        flash('Investigation created successfully!', 'success')
        return redirect(url_for('inv_views.investigations_list'))

    return render_template(
        'dashboard/investigations/create_investigations.html', form=form)


@inv_views.route('/investigations/create', methods=['GET', 'POST'])
def create_investigation():
    """ Create a new Investigation """
    form = InvestigationWithDetailsForm()
    return render_template('dashboard/investigations/new_investigations.html', form=form)
