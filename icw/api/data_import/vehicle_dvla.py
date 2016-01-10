import csv
import io

from ..db import Vehicle


def load_vehicle(app, f):
    reader = csv.DictReader(f)

    session = app['db-session']()

    vehicles = []

    for i, row in enumerate(reader):
        vehicle = {'accident_id': row['Acc_Index'],
                   'vehicle_ref': row['Vehicle_Reference'],
                   'make': row['make'].strip() or None,
                   'model': row['model'].strip() or None,
                   'age_of_vehicle': int(row['Age_of_Vehicle']) if row['Age_of_Vehicle'] != '-1' else None,
                   'engine_capacity': int(row['Engine_Capacity_(CC)']) if row['Engine_Capacity_(CC)'] != '-1' else None,
                   }

        vehicles.append(vehicle)

        if i % 10000 == 0:
            session.bulk_update_mappings(Vehicle, vehicles)
            session.flush()
            session.commit()
            vehicles[:] = []
            print(i)

    if vehicles:
        session.bulk_update_mappings(Vehicle, vehicles)
        session.flush()
        session.commit()

if __name__ == '__main__':
    import sys
    from ..app import get_app
    app = get_app()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            load_vehicle(app, f)
    else:
        load_vehicle(app, io.TextIOWrapper(sys.stdin.buffer, encoding='latin1'))
