from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class VehicleType(Base):
    __tablename__ = 'vehicle_type'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    font_awesome = Column(String, nullable=True)
