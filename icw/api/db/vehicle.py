from sqlalchemy import String, Column, ForeignKey, SmallInteger, Integer
from sqlalchemy.orm import relationship

from . import Base


class Vehicle(Base):
    __tablename__ = 'vehicle'

    accident_id = Column(String(13), ForeignKey('accident.id'), index=True, primary_key=True)
    vehicle_ref = Column(SmallInteger, primary_key=True)

    type_id = Column(SmallInteger, ForeignKey('vehicle_type.id'))
    towing_and_articulation_id = Column(SmallInteger, ForeignKey('towing_and_articulation.id'))
    location_id = Column(SmallInteger, ForeignKey('vehicle_location.id'))
    manoeuvre_id = Column(SmallInteger, ForeignKey('vehicle_manoeuvre.id'))
    junction_location_id = Column(SmallInteger, ForeignKey('junction_location.id'))

    hit_object_in_carriageway_id = Column(SmallInteger, ForeignKey('hit_object_in_carriageway.id'))
    hit_object_off_carriageway_id = Column(SmallInteger, ForeignKey('hit_object_off_carriageway.id'))
    first_point_of_impact_id = Column(SmallInteger, ForeignKey('first_point_of_impact.id'))
    skidding_and_overturning_id = Column(SmallInteger, ForeignKey('skidding_and_overturning.id'))
    leaving_carriageway_id = Column(SmallInteger, ForeignKey('vehicle_leaving_carriageway.id'))

    driver_sex_id = Column(SmallInteger, ForeignKey('sex.id'), index=True)
    driver_age_band_id = Column(SmallInteger, ForeignKey('age_band.id'), index=True)
    driver_age = Column(SmallInteger, nullable=True, index=True)

    age_of_vehicle = Column(SmallInteger, nullable=True)
    engine_capacity = Column(Integer, nullable=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)

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
            'skiddingAndOverturning': app['reference-data']['SkiddingAndOverturning'].get(self.skidding_and_overturning_id),
            'leavingCarriageway': app['reference-data']['VehicleLeavingCarriageway'].get(self.leaving_carriageway_id),
            'hitObjectInCarriageway': app['reference-data']['HitObjectInCarriageway'].get(self.hit_object_in_carriageway_id),
            'hitObjectOffCarriageway': app['reference-data']['HitObjectOffCarriageway'].get(self.hit_object_off_carriageway_id),
            'firstPointOfImpact': app['reference-data']['FirstPointOfImpact'].get(self.first_point_of_impact_id),
            'driverSex': app['reference-data']['Sex'].get(self.driver_sex_id),
            'driverAgeBand': app['reference-data']['AgeBand'].get(self.driver_age_band_id),
            'driverAge': self.driver_age,
            'make': self.make,
            'model': self.model,
        }