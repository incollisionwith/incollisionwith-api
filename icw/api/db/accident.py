from geoalchemy2 import Geometry
import shapely.wkb
from sqlalchemy import String, Column, ForeignKey, DateTime, Boolean, Float, Date, SmallInteger
from sqlalchemy.orm import relationship

from . import Base


class Accident(Base):
    __tablename__ = 'accident'

    id = Column(String(13), primary_key=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    police_force_id = Column(SmallInteger, ForeignKey('police_force.id'))
    severity_id = Column(SmallInteger, ForeignKey('casualty_severity.id'))
    junction_control_id = Column(SmallInteger, ForeignKey('junction_control.id'), nullable=True)
    junction_detail_id = Column(SmallInteger, ForeignKey('junction_detail.id'), nullable=True)

    number_of_vehicles = Column(SmallInteger)
    number_of_casualties = Column(SmallInteger)
    date = Column(Date)
    date_and_time = Column(DateTime(timezone=True))
    police_attended = Column(Boolean)

    speed_limit = Column(SmallInteger, nullable=True)
    road_type = Column(SmallInteger, ForeignKey('road_type.id'))
    road_1_class = Column(SmallInteger, ForeignKey('road_class.id'))
    road_1_number = Column(SmallInteger, nullable=True)
    road_1 = Column(String, nullable=True)
    road_2_class = Column(SmallInteger, ForeignKey('road_class.id'), nullable=True)
    road_2_number = Column(SmallInteger, nullable=True)
    road_2 = Column(String, nullable=True)

    pedestrian_crossing_human_id = Column(SmallInteger, ForeignKey('pedestrian_crossing_human.id'))
    pedestrian_crossing_physical_id = Column(SmallInteger, ForeignKey('pedestrian_crossing_physical.id'))

    light_conditions_id = Column(SmallInteger, ForeignKey('light_conditions.id'))
    weather_id = Column(SmallInteger, ForeignKey('weather.id'))
    road_surface_id = Column(SmallInteger, ForeignKey('road_surface.id'))
    road_type_id = Column(SmallInteger, ForeignKey('road_type.id'))
    special_conditions_id = Column(SmallInteger, ForeignKey('special_conditions.id'))
    carriageway_hazards_id = Column(SmallInteger, ForeignKey('carriageway_hazards.id'))
    urban_rural_id = Column(SmallInteger, ForeignKey('urban_rural.id'))

    solar_elevation = Column(Float, nullable=True)
    moon_phase = Column(SmallInteger, nullable=True)

    police_force = relationship('PoliceForce')
    severity = relationship('CasualtySeverity')
    junction_detail = relationship('JunctionDetail')
    junction_control = relationship('JunctionControl')

    vehicles = relationship('Vehicle', order_by='Vehicle.vehicle_ref', viewonly=True)
    casualties = relationship('Casualty', order_by='Casualty.casualty_ref', viewonly=True)
    citations = relationship('CitationAccident', back_populates='accident') #, order_by='Citation.published')

    dimensions = {
        'numberOfVehicles': number_of_vehicles,
        'numberOfCasualties': number_of_casualties,
        'location': location,
    }

    def to_json(self, app):
        if self.location is not None:
            location = shapely.wkb.loads(bytes(self.location.data))
            location = {'lat': location.y, 'lon': location.x}
        else:
            location = None
        return {
            'id': self.id,
            'location': location,
            'police_force': app['reference-data']['PoliceForce'][self.police_force_id],
            'severity': app['reference-data']['CasualtySeverity'][self.severity_id],
            'numberOfVehicles': self.number_of_vehicles,
            'numberOfCasualties': self.number_of_casualties,
            'vehicles': [vehicle.to_json(app) for vehicle in self.vehicles],
            'date': self.date.isoformat(),
            'dateTime': self.date_and_time.isoformat() if self.date_and_time else None,
            'policeAttended': self.police_attended,
            'solarElevation': self.solar_elevation,
            'moonPhase': self.moon_phase,
            'speedLimit': self.speed_limit,
            'specialConditions': app['reference-data']['SpecialConditions'].get(self.special_conditions_id),
            'carriagewayHazards': app['reference-data']['CarriagewayHazards'].get(self.carriageway_hazards_id),
            'junctionControl': app['reference-data']['JunctionControl'].get(self.junction_control_id),
            'junctionDetail': app['reference-data']['JunctionDetail'].get(self.junction_detail_id),
            'roadType': app['reference-data']['RoadType'].get(self.road_type_id),
            'lightConditions': app['reference-data']['LightConditions'].get(self.light_conditions_id),
            'pedestrianCrossingHuman': app['reference-data']['PedestrianCrossingHuman'].get(self.pedestrian_crossing_human_id),
            'pedestrianCrossingPhysical': app['reference-data']['PedestrianCrossingPhysical'].get(self.pedestrian_crossing_physical_id),
            'weather': app['reference-data']['Weather'].get(self.weather_id),
            'citations': [dict(certainty=assoc.certainty.to_json(),
                               ** assoc.citation.to_json())
                          for assoc in self.citations],
        }