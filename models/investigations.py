"""Investigations Model Class"""
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, event
from .base_model import BaseModel


class Investigations(BaseModel):
    """Investigations Class"""
    __tablename__ = "investigations"

    ir_number = Column(String(10), nullable=False, unique=True)
    raised_by = Column(String(20), nullable=False)
    line_manager = Column(String(20), nullable=False)
    priority = Column(String(10), nullable=False)
    team_leader = Column(String(20), nullable=True)
    description = Column(String(255), nullable=False)
    root_cause_summary = Column(String(100), nullable=False)
    ir_source = Column(String(30), nullable=False)
    due_date = Column(DateTime, nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        """Initialise investigations Class"""
        super().__init__(*args, **kwargs)

    def generate_ir_no(self):
        """Generate new ir number"""
        current_year = func.extract('year', func.now()).scalar()

        from app import Session
        db = Session()

        count = db.query(
            Investigations.ir_number).filter(
            Investigations.ir_number.like(f"{current_year}")).count()

        if count:
            increment = count + 1
            ir_number = f"{current_year}-{increment:03d}"
        else:
            ir_number = f"{current_year}-001"

        return ir_number
