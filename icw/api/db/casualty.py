from sqlalchemy import String, Column, ForeignKey, ForeignKeyConstraint, SmallInteger
from sqlalchemy.orm import relationship

from . import Base


class Casualty(Base):
    __tablename__ = 'casualty'

    accident_id = Column(String(13), ForeignKey('accident.id'), index=True, primary_key=True)
    vehicle_ref = Column(SmallInteger, primary_key=True)
    casualty_ref = Column(SmallInteger, primary_key=True)

    class_id = Column(SmallInteger, ForeignKey('casualty_class.id'), index=True)
    sex_id = Column(SmallInteger, ForeignKey('sex.id'), index=True)
    severity_id = Column(SmallInteger, ForeignKey('casualty_severity.id'), index=True)
    age_band_id = Column(SmallInteger, ForeignKey('age_band.id'), index=True)
    type_id = Column(SmallInteger, ForeignKey('vehicle_type.id'), index=True)
    age = Column(SmallInteger, nullable=True, index=True)

    pedestrian_location_id = Column(SmallInteger, ForeignKey('pedestrian_location.id'), nullable=True)
    pedestrian_movement_id = Column(SmallInteger, ForeignKey('pedestrian_movement.id'), nullable=True)

    accident = relationship('Accident', viewonly=True)
    vehicle = relationship('Vehicle', foreign_keys=[accident_id, vehicle_ref], backref='casualties')
    age_band = relationship('AgeBand')
    class_ = relationship('CasualtyClass')
    sex = relationship('Sex')
    severity = relationship('CasualtySeverity')
    type = relationship('VehicleType')
    pedestrian_location = relationship('PedestrianLocation')
    pedestrian_movement = relationship('PedestrianMovement')

    __table_args__ = (
        ForeignKeyConstraint(
            ['accident_id', 'vehicle_ref'],
            ['vehicle.accident_id', 'vehicle.vehicle_ref'],
        ),
    )

    def to_json(self, app):
        return {
            'casualtyRef': self.casualty_ref,
            'class': app['reference-data']['CasualtyClass'].get(self.class_id),
            'sex': app['reference-data']['Sex'].get(self.sex_id),
            'severity': app['reference-data']['CasualtySeverity'].get(self.severity_id),
            'ageBand': app['reference-data']['AgeBand'].get(self.age_band_id),
            'age': self.age,
            'type': app['reference-data']['VehicleType'].get(self.type_id),
            'pedestrianLocation': app['reference-data']['PedestrianLocation'].get(self.pedestrian_location_id),
            'pedestrianMovement': app['reference-data']['PedestrianMovement'].get(self.pedestrian_movement_id),

        }