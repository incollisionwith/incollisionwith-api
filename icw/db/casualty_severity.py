from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class CasualtySeverity(Base):
    __tablename__ = 'casualty_severity'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    comment = Column(String)
    injury_definition = Column(String)

    def to_json(self, verbose=False):
        data = {
            'id': self.id,
            'label': self.label,
        }
        if verbose:
            data.update({
                'comment': self.comment,
                'injury_definition': self.injury_definition,
            })
        return data