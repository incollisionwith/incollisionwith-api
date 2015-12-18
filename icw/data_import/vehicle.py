import csv

from icw.db import Vehicle

def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value

def load_accident(app, f):
    reader = csv.DictReader(f)

    session = app['db-session']()

    for i, row in enumerate(reader):
        try:
            vehicle = Vehicle(accident_id=row['\ufeffAccident_Index'],
                              vehicle_ref=row['Vehicle_Reference'],
                              vehicle_type_id=indexed(row, 'Vehicle_Type'),
                              towing_and_articulation_id=indexed(row, 'Towing_and_Articulation'))
            session.merge(vehicle)
        except:
            print(row)

        if i % 1000 == 0:
            session.commit()
            print(i)

        session.commit()

if __name__ == '__main__':
    import sys
    from ..app import get_app
    app = get_app()

    with open(sys.argv[1]) as f:
        load_accident(app, f)
