from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Revisions(BaseModel):
    """Revisions Class"""
    __tablename__ = "revisions"

    investigation_id = Column(String(60), ForeignKey('investigations.id'))
    requested_by = Column(String(60), nullable=False)
    reason_for_revision = Column(String(255), nullable=False)
    revison_type = Column(String(20), nullable=False)
    approved_by = Column(String(60), nullable=False)

    investigations = relationship('Investigations', backref='investigations')

    def __init__(self, *args, **kwargs) -> None:
        """Initialisation of class"""
        super().__init__(*args, **kwargs)

    def as_dict(self):
        """Return dictionary represetation"""
        return {
            "class": self.__class__.__name__,
            "id": self.id,
            "date_created_on": self.date_created_on,
            "date_updated_on": self.date_updated_on,
            "satus": self.status.value,
            "investigation_id": self.investigation_id,
            "requested_by": self.requested_by,
            "reason_for_revision": self.reason_for_revision,
            "revison_type": self.revison_type,
            "approved_by": self.approved_by,
        }
