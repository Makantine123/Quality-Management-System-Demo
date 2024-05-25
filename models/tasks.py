"""Tasks Module"""

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Tasks(BaseModel):
    """Task Class"""
    __tablename__ = 'tasks'

    investigationsdetail_id = Column(String(60),
                                     ForeignKey('investigations_details.id'),
                                     nullable=True)
    investigation_id = Column(String(60),
                              ForeignKey('investigations.id'),
                              nullable=False)
    assign_to = Column(String(20), nullable=False)
    description = Column(String(255), nullable=False)
    due_date = Column(DateTime, nullable=False)
    date_completed_on = Column(DateTime, nullable=False)

    investigations_details = relationship('InvestigationsDetails',
                                          backref='task_investigations_details')
    investigations = relationship('Investigations', backref='tasks')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
