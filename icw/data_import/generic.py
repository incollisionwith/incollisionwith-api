import csv
import pkgutil

import yaml

from icw.db import AccidentSeverity, VehicleType, TowingAndArticulation


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

    load_generic(app, 'data/accident_severity.yaml', AccidentSeverity)
    load_generic(app, 'data/vehicle_type.yaml', VehicleType)
    load_generic(app, 'data/towing_and_articulation.yaml', TowingAndArticulation)
