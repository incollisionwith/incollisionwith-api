from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Boolean, Float, Date
from sqlalchemy.orm import relationship

from . import Base


class Accident(Base):
    __tablename__ = 'accident'

    id = Column(String(13), primary_key=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    police_force_id = Column(Integer, ForeignKey('police_force.id'))
    accident_severity_id = Column(Integer, ForeignKey('accident_severity.id'))
    number_of_vehicles = Column(Integer)
    number_of_casualties = Column(Integer)
    date = Column(Date)
    date_and_time = Column(DateTime(timezone=True))
    police_attended = Column(Boolean)

    solar_elevation = Column(Float, nullable=True)
    moon_phase = Column(Integer, nullable=True)

    police_force = relationship('PoliceForce')
    accident_severity = relationship('AccidentSeverity')
