from sqlalchemy import Column, String, SmallInteger
from . import Base

__all__ = ['ReferenceTable',
           'AgeBand', 'CarriagewayHazards', 'CasualtyClass', 'CasualtySeverity', 'CitationCertainty',
           'FirstPointOfImpact', 'HighwayAuthority', 'HitObjectInCarriageway', 'HitObjectOffCarriageway',
           'JunctionControl', 'JunctionDetail', 'JunctionLocation', 'LightConditions', 'PedestrianCrossingHuman',
           'PedestrianCrossingPhysical', 'PedestrianLocation', 'PedestrianMovement', 'RoadClass', 'RoadSurface',
           'RoadType', 'Sex', 'SkiddingAndOverturning', 'SpecialConditions', 'TowingAndArticulation', 'UrbanRural',
           'VehicleLeavingCarriageway', 'VehicleLocation', 'VehicleManoeuvre', 'VehicleType', 'Weather']


class ReferenceTable(Base):
    __abstract__ = True

    id = Column(SmallInteger, primary_key=True)
    label = Column(String)

    def to_json(self, verbose=False):
        return {
            'id': self.id,
            'label': self.label,
        }


class AgeBand(ReferenceTable):
    __tablename__ = 'age_band'

    gte = Column(SmallInteger)
    lt = Column(SmallInteger, nullable=True)


class CarriagewayHazards(ReferenceTable):
    __tablename__ = 'carriageway_hazards'


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


class CitationCertainty(ReferenceTable):
    __tablename__ = 'citation_certainty'


class FirstPointOfImpact(ReferenceTable):
    __tablename__ = 'first_point_of_impact'


class HighwayAuthority(ReferenceTable):
    __tablename__ = 'highway_authority'

    id = Column(String, primary_key=True)


class HitObjectInCarriageway(ReferenceTable):
    __tablename__ = 'hit_object_in_carriageway'

    sentence_part = Column(String)


class HitObjectOffCarriageway(ReferenceTable):
    __tablename__ = 'hit_object_off_carriageway'


class JunctionControl(ReferenceTable):
    __tablename__ = 'junction_control'


class JunctionDetail(ReferenceTable):
    __tablename__ = 'junction_detail'


class JunctionLocation(ReferenceTable):
    __tablename__ = 'junction_location'


class LightConditions(ReferenceTable):
    __tablename__ = 'light_conditions'


class PedestrianCrossingHuman(ReferenceTable):
    __tablename__ = 'pedestrian_crossing_human'


class PedestrianCrossingPhysical(ReferenceTable):
    __tablename__ = 'pedestrian_crossing_physical'


class PedestrianLocation(ReferenceTable):
    __tablename__ = 'pedestrian_location'


class PedestrianMovement(ReferenceTable):
    __tablename__ = 'pedestrian_movement'


class RoadClass(ReferenceTable):
    __tablename__ = 'road_class'

    pattern = Column(String)


class RoadSurface(ReferenceTable):
    __tablename__ = 'road_surface'


class RoadType(ReferenceTable):
    __tablename__ = 'road_type'


class Sex(ReferenceTable):
    __tablename__ = 'sex'


class SkiddingAndOverturning(ReferenceTable):
    __tablename__ = 'skidding_and_overturning'


class SpecialConditions(ReferenceTable):
    __tablename__ = 'special_conditions'


class TowingAndArticulation(ReferenceTable):
    __tablename__ = 'towing_and_articulation'


class UrbanRural(ReferenceTable):
    __tablename__ = 'urban_rural'


class VehicleLeavingCarriageway(ReferenceTable):
    __tablename__ = 'vehicle_leaving_carriageway'


class VehicleLocation(ReferenceTable):
    __tablename__ = 'vehicle_location'


class VehicleManoeuvre(ReferenceTable):
    __tablename__ = 'vehicle_manoeuvre'


class VehicleType(ReferenceTable):
    __tablename__ = 'vehicle_type'

    font_awesome = Column(String, nullable=True)
    class_driver = Column(String, nullable=True)
    class_passenger = Column(String, nullable=True)

    def to_json(self, verbose=False):
        data = super().to_json()
        data.update({
            'driverLabel': self.class_driver or (self.label + ' driver'),
            'passengerLabel': self.class_passenger or (self.label + ' passenger'),
            'fontAwesome': self.font_awesome,
        })
        return data


class Weather(ReferenceTable):
    __tablename__ = 'weather'
