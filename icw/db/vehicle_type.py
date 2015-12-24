from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class VehicleType(Base):
    __tablename__ = 'vehicle_type'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    person_label = Column(String)
    font_awesome = Column(String, nullable=True)


    def to_json(self, verbose=False):
        data = {
            'id': self.id,
            'label': self.label,
            'personLabel': self.person_label,
            'fontAwesome': self.font_awesome,
        }
        return data