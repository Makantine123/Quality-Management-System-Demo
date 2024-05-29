"""Investingations Details Module"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class InvestigationsDetails(BaseModel):
    """Investigations Details Class"""
    __tablename__ = "investigations_details"

    investigation_id = Column(String(60), ForeignKey('investigations.id'))
    main_causes = Column(String(60), nullable=False)
    steps_required = Column(String(255))
    by_who = Column(String(60), nullable=False)
    due_date = Column(DateTime, nullable=False)
    date_completed = Column(DateTime, nullable=True)

    investigations = relationship("Investigations",
                                  backref="investigations_details")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
