from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Boolean, Float, Date
from sqlalchemy.orm import relationship

from . import Base


class Vehicle(Base):
    __tablename__ = 'vehicle'

    accident_id = Column(String(13), ForeignKey('accident.id'), index=True, primary_key=True)
    vehicle_ref = Column(Integer, primary_key=True)

    vehicle_type_id = Column(Integer, ForeignKey('vehicle_type.id'))
    towing_and_articulation_id = Column(Integer, ForeignKey('towing_and_articulation.id'))

    accident = relationship('Accident')
    vehicle_type = relationship('VehicleType')
    towing_and_articulation = relationship('TowingAndArticulation')
