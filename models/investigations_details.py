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
    date_completed = Column(DateTime, nullable=False)

    investigations = relationship("Investigations",
                                  backref="investigations_details")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def as_dict(self):
        """Returns dictionary represetation of class"""
        return {
            "class": self.__class__.__name__,
            "id": self.id,
            "investigations_id": self.investigation_id,
            "date_created_on": self.date_created_on,
            "date_updated_on": self.date_updated_on,
            "status": self.status.value,
            "date_completed_on": self.date_created_on,
            "main_causes": self.main_causes,
            "steps_required": self.steps_required,
            "by_who": self.by_who,
            "due_date": self.due_date,
        }
