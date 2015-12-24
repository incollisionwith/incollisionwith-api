import csv

from icw.db import Vehicle

def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value

def sex_indexed(row, name):
    value = int(row[name])
    if value in (1, 2):
        return value

def load_accident(app, f):
    reader = csv.DictReader(f)

    engine = app['db-engine']

    vehicles = []
    engine.execute(Vehicle.__table__.delete())

    for i, row in enumerate(reader):
        vehicle = {'accident_id': row['\ufeffAccident_Index'],
                   'vehicle_ref': row['Vehicle_Reference'],
                   'type_id': indexed(row, 'Vehicle_Type'),
                   'driver_sex_id': sex_indexed(row, 'Sex_of_Driver'),
                   'driver_age': indexed(row, 'Age_of_Driver'),
                   'driver_age_band_id': indexed(row, 'Age_Band_of_Driver'),
                   'manoeuvre_id': indexed(row, 'Vehicle_Manoeuvre'),
                   'location_id': indexed(row, 'Vehicle_Location-Restricted_Lane'),
                   'towing_and_articulation_id': indexed(row, 'Towing_and_Articulation'),
                   'junction_location_id': indexed(row, 'Junction_Location')}
        vehicles.append(vehicle)

        if i % 10000 == 0:
            engine.execute(Vehicle.__table__.insert(), vehicles)
            vehicles[:] = []
            print(i)

    engine.execute(Vehicle.__table__.insert(), vehicles)

if __name__ == '__main__':
    import sys
    from ..app import get_app
    app = get_app()

    with open(sys.argv[1]) as f:
        load_accident(app, f)
