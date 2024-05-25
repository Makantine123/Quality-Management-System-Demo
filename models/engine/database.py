"""Database Module"""
from app import session
from ..investigations import Investigations

new_inv = Investigations(
    ir_number='IR3456',
    raised_by='John Doe',
    line_manager='Jane Smith',
    priority='High',
    team_leader='Sam Brown',
    description='Description of the investigation',
    root_cause_summary='Root cause analysis summary',
    ir_source='Internal',
    due_date=None,
)

session.add(new_inv)
session.commit()
print(new_inv.as_dict())
