from sqlalchemy import Column, Integer, String

from . import Base

__all__ = ['AgeBand', 'CasualtyClass', 'CasualtySeverity', 'JunctionControl', 'JunctionDetail', 'JunctionLocation',
           'PedestrianLocation', 'PedestrianMovement', 'Sex', 'TowingAndArticulation', 'VehicleLocation',
           'VehicleManoeuvre', 'VehicleType']


class ReferenceTable(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    label = Column(String)

    def to_json(self, verbose=False):
        return {
            'id': self.id,
            'label': self.label,
        }


class AgeBand(ReferenceTable):
    __tablename__ = 'age_band'

    gte = Column(Integer)
    lt = Column(Integer, nullable=True)


class CasualtyClass(ReferenceTable):
    __tablename__ = 'casualty_class'


class CasualtySeverity(ReferenceTable):
    __tablename__ = 'casualty_severity'

    comment = Column(String)
    injury_definition = Column(String)

    def to_json(self, verbose=False):
        data = super().to_json()
        if verbose:
            data.update({
                'comment': self.comment,
                'injury_definition': self.injury_definition,
            })
        return data


class JunctionControl(ReferenceTable):
    __tablename__ = 'junction_control'


class JunctionDetail(ReferenceTable):
    __tablename__ = 'junction_detail'


class JunctionLocation(ReferenceTable):
    __tablename__ = 'junction_location'


class PedestrianLocation(ReferenceTable):
    __tablename__ = 'pedestrian_location'


class PedestrianMovement(ReferenceTable):
    __tablename__ = 'pedestrian_movement'


class Sex(ReferenceTable):
    __tablename__ = 'sex'


class TowingAndArticulation(ReferenceTable):
    __tablename__ = 'towing_and_articulation'


class VehicleLocation(ReferenceTable):
    __tablename__ = 'vehicle_location'


class VehicleManoeuvre(ReferenceTable):
    __tablename__ = 'vehicle_manoeuvre'


class VehicleType(ReferenceTable):
    __tablename__ = 'vehicle_type'

    person_label = Column(String)
    font_awesome = Column(String, nullable=True)

    def to_json(self, verbose=False):
        data = super().to_json()
        data.update({
            'personLabel': self.person_label,
            'fontAwesome': self.font_awesome,
        })
        return data
