from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from . import Base


class Casualty(Base):
    __tablename__ = 'casualty'

    accident_id = Column(String(13), ForeignKey('accident.id'), index=True, primary_key=True)
    vehicle_ref = Column(Integer, primary_key=True)
    casualty_ref = Column(Integer, primary_key=True)

    class_id = Column(Integer, ForeignKey('casualty_class.id'), index=True)
    sex_id = Column(Integer, ForeignKey('sex.id'), index=True)
    severity_id = Column(Integer, ForeignKey('casualty_severity.id'), index=True)
    age_band_id = Column(Integer, ForeignKey('age_band.id'), index=True)
    type_id = Column(Integer, ForeignKey('vehicle_type.id'), index=True)
    age = Column(Integer, nullable=True, index=True)

    pedestrian_location_id = Column(Integer, ForeignKey('pedestrian_location.id'), nullable=True)
    pedestrian_movement_id = Column(Integer, ForeignKey('pedestrian_movement.id'), nullable=True)

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

    def to_json(self):
        return {
            'casualtyRef': self.casualty_ref,
            'class': self.class_.to_json(),
            'sex': self.sex.to_json() if self.sex else None,
            'severity': self.severity.to_json(),
            'ageBand': self.age_band.to_json() if self.age_band else None,
            'age': self.age,
            'type': self.type.to_json(),
            'pedestrianLocation': self.pedestrian_location.to_json() if self.pedestrian_location else None,
            'pedestrianMovement': self.pedestrian_movement.to_json() if self.pedestrian_movement else None,

        }