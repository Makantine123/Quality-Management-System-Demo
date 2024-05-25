from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SelectField, HiddenField, FieldList, FormField
from wtforms.validators import DataRequired, Optional


class InvestigationForm(FlaskForm):
    id = HiddenField()
    ir_number = StringField('IR Number', validators=[DataRequired()])
    raised_by = StringField('Raised By', validators=[DataRequired()])
    line_manager = StringField('Line Manager', validators=[DataRequired()])
    priority = StringField('Priority', validators=[DataRequired()])
    team_leader = StringField('Team Leader', validators=[Optional()])
    description = TextAreaField('Description', validators=[DataRequired()])
    root_cause_summary = TextAreaField('Root Cause Summary', validators=[DataRequired()])
    ir_source = StringField('IR Source', validators=[DataRequired()])
    due_date = DateTimeField('Due Date', validators=[Optional()])


class InvestigationDetailForm(FlaskForm):
    id = HiddenField()
    investigation_id = HiddenField()
    main_causes = StringField('Main Causes', validators=[DataRequired()])
    steps_required = TextAreaField('Steps Required', validators=[Optional()])
    by_who = StringField('By Who', validators=[DataRequired()])
    due_date = DateTimeField('Due Date', validators=[DataRequired()])
    date_completed = DateTimeField('Date Completed', validators=[DataRequired()])


class InvestigationWithDetailsForm(FlaskForm):
    investigation = FormField(InvestigationForm)
    details = FieldList(FormField(InvestigationDetailForm), min_entries=1)
