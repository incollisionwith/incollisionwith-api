import csv
import pkgutil

import yaml

from icw.db import CasualtySeverity, VehicleType, TowingAndArticulation, CasualtyClass, Sex, AgeBand, JunctionDetail, \
    JunctionControl, VehicleManoeuvre, VehicleLocation, PedestrianLocation, PedestrianMovement, JunctionLocation


def load_generic(app, filename, model):
    session = app['db-session']()

    data = yaml.load(pkgutil.get_data('icw', filename))
    for datum in data:
        accident_severity = model(**datum)
        session.merge(accident_severity)

    session.commit()


if __name__ == '__main__':
    import sys
    from ..app import get_app
    app = get_app()

    load_generic(app, 'data/age_band.yaml', AgeBand)
    load_generic(app, 'data/casualty_class.yaml', CasualtyClass)
    load_generic(app, 'data/casualty_severity.yaml', CasualtySeverity)
    load_generic(app, 'data/junction_control.yaml', JunctionControl)
    load_generic(app, 'data/junction_detail.yaml', JunctionDetail)
    load_generic(app, 'data/junction_location.yaml', JunctionLocation)
    load_generic(app, 'data/towing_and_articulation.yaml', TowingAndArticulation)
    load_generic(app, 'data/sex.yaml', Sex)
    load_generic(app, 'data/vehicle_location.yaml', VehicleLocation)
    load_generic(app, 'data/vehicle_manoeuvre.yaml', VehicleManoeuvre)
    load_generic(app, 'data/vehicle_type.yaml', VehicleType)
    load_generic(app, 'data/pedestrian_location.yaml', PedestrianLocation)
    load_generic(app, 'data/pedestrian_movement.yaml', PedestrianMovement)
