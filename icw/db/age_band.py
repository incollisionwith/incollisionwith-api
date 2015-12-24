from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class AgeBand(Base):
    __tablename__ = 'age_band'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    gte = Column(Integer)
    lt = Column(Integer, nullable=True)

    def to_json(self, verbose=False):
        return {
            'id': self.id,
            'label': self.label,
        }
