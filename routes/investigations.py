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
    investiagtions = db.query(Investigations).all()
    return render_template('dashboard/investigations/investigations.html',
                           investiagtions=investiagtions)


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
