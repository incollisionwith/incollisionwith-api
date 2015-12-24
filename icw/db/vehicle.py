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

    accident = relationship('Accident', backref='vehicles')
    type = relationship('VehicleType')
    towing_and_articulation = relationship('TowingAndArticulation')
    location = relationship('VehicleLocation')
    manoeuvre = relationship('VehicleManoeuvre')
    driver_sex = relationship('Sex')
    driver_age_band = relationship('AgeBand')
    junction_location = relationship('JunctionLocation')

    def to_json(self):
        return {
            'vehicleRef': self.vehicle_ref,
            'type': self.type.to_json(),
            'casualties': [casualty.to_json() for casualty in self.casualties],
            'manoeuvre': self.manoeuvre.to_json() if self.manoeuvre else None,
            'location': self.location.to_json() if self.location else None,
            'junctionLocation': self.junction_location.to_json() if self.junction_location else None,
            'driverSex': self.driver_sex.to_json() if self.driver_sex else None,
            'driverAgeBand': self.driver_age_band.to_json() if self.driver_age_band else None,
            'driverAge': self.driver_age
        }