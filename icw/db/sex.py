from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Sex(Base):
    __tablename__ = 'sex'

    id = Column(Integer, primary_key=True)
    label = Column(String)

    def to_json(self, verbose=False):
        return {
            'id': self.id,
            'label': self.label,
        }
