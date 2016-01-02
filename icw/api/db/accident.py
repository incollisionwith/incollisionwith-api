from geoalchemy2 import Geometry
import shapely.wkb
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Boolean, Float, Date
from sqlalchemy.orm import relationship

from . import Base


class Accident(Base):
    __tablename__ = 'accident'

    id = Column(String(13), primary_key=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    police_force_id = Column(Integer, ForeignKey('police_force.id'))
    severity_id = Column(Integer, ForeignKey('casualty_severity.id'))
    junction_control_id = Column(Integer, ForeignKey('junction_control.id'), nullable=True)
    junction_detail_id = Column(Integer, ForeignKey('junction_detail.id'), nullable=True)

    number_of_vehicles = Column(Integer)
    number_of_casualties = Column(Integer)
    date = Column(Date)
    date_and_time = Column(DateTime(timezone=True))
    police_attended = Column(Boolean)

    solar_elevation = Column(Float, nullable=True)
    moon_phase = Column(Integer, nullable=True)

    police_force = relationship('PoliceForce')
    severity = relationship('CasualtySeverity')
    junction_detail = relationship('JunctionDetail')
    junction_control = relationship('JunctionControl')

    vehicles = relationship('Vehicle', order_by='Vehicle.vehicle_ref')
    casualties = relationship('Casualty', order_by='Casualty.casualty_ref')
    citations = relationship('CitationAccident', back_populates='accident') #, order_by='Citation.published')

    dimensions = {
        'numberOfVehicles': number_of_vehicles,
        'numberOfCasualties': number_of_casualties,
        'location': location,
    }

    def to_json(self):
        if self.location is not None:
            location = shapely.wkb.loads(bytes(self.location.data))
            location = {'lat': location.y, 'lon': location.x}
        else:
            location = None
        return {
            'id': self.id,
            'location': location,
            'police_force': self.police_force.to_json(),
            'severity': self.severity.to_json(),
            'numberOfVehicles': self.number_of_vehicles,
            'numberOfCasualties': self.number_of_casualties,
            'vehicles': [vehicle.to_json() for vehicle in self.vehicles],
            'date': self.date.isoformat(),
            'dateTime': self.date_and_time.isoformat() if self.date_and_time else None,
            'policeAttended': self.police_attended,
            'solarElevation': self.solar_elevation,
            'moonPhase': self.moon_phase,
            'junctionControl': self.junction_control.to_json() if self.junction_control else None,
            'junctionDetail': self.junction_detail.to_json() if self.junction_detail else None,
            'citations': [dict(certainty=assoc.certainty.to_json(),
                               ** assoc.citation.to_json())
                          for assoc in self.citations],
        }