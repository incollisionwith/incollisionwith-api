from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Vehicle(Base):
    __tablename__ = 'vehicle'

    accident_id = Column(String(13), ForeignKey('accident.id'), index=True, primary_key=True)
    vehicle_ref = Column(Integer, primary_key=True)

    type_id = Column(Integer, ForeignKey('vehicle_type.id'))
    towing_and_articulation_id = Column(Integer, ForeignKey('towing_and_articulation.id'))
    location_id = Column(Integer, ForeignKey('vehicle_location.id'))
    manoeuvre_id = Column(Integer, ForeignKey('vehicle_manoeuvre.id'))
    junction_location_id = Column(Integer, ForeignKey('junction_location.id'))

    driver_sex_id = Column(Integer, ForeignKey('sex.id'), index=True)
    driver_age_band_id = Column(Integer, ForeignKey('age_band.id'), index=True)
    driver_age = Column(Integer, nullable=True, index=True)

    accident = relationship('Accident')
    type = relationship('VehicleType')
    towing_and_articulation = relationship('TowingAndArticulation')
    location = relationship('VehicleLocation')
    manoeuvre = relationship('VehicleManoeuvre')
    driver_sex = relationship('Sex')
    driver_age_band = relationship('AgeBand')
    junction_location = relationship('JunctionLocation')

    # dimensions = {
    #     'type': type_id,
    #     'towingAndArticulation': towing_and_articulation_id,
    #     'location': location_id,
    #     'manoeuvre': manoeuvre_id,
    #     'junctionLocation': junction_location_id,
    #     'driverAge': driver_age,
    # }

    def to_json(self, app):
        return {
            'vehicleRef': self.vehicle_ref,
            'type': app['reference-data']['VehicleType'].get(self.type_id),
            'casualties': [casualty.to_json(app) for casualty in self.casualties],
            'manoeuvre': app['reference-data']['VehicleManoeuvre'].get(self.manoeuvre_id),
            'location': app['reference-data']['VehicleLocation'].get(self.location_id),
            'junctionLocation': app['reference-data']['JunctionLocation'].get(self.junction_location_id),
            'towingAndArticulation': app['reference-data']['TowingAndArticulation'].get(self.towing_and_articulation_id),
            'driverSex': app['reference-data']['Sex'].get(self.driver_sex_id),
            'driverAgeBand': app['reference-data']['AgeBand'].get(self.driver_age_band_id),
            'driverAge': self.driver_age
        }