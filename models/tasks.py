"""Tasks Module"""

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Tasks(BaseModel):
    """Task Class"""
    __tablename__ = 'tasks'

    task_type = Column(String(20), nullable=False)
    investigation_id = Column(String(60),
                              ForeignKey('investigations.id'),
                              nullable=False)
    assign_to = Column(String(20), nullable=False)
    description = Column(String(255), nullable=False)
    due_date = Column(DateTime, nullable=False)
    date_completed_on = Column(DateTime, nullable=True)

    investigations = relationship('Investigations', backref='tasks')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
