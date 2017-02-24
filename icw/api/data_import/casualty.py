import csv

from ..db import Casualty

def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value

def load_accident(app, f):
    reader = csv.DictReader(f)

    engine = app['db-engine']

    engine.execute(Casualty.__table__.delete())

    casualties = []
    for i, row in enumerate(reader):
        casualty = {'accident_id': row.get('Accident_Index') or row['\ufeffAccident_Index'],
                    'vehicle_ref': row['Vehicle_Reference'],
                    'casualty_ref': row['Casualty_Reference'],
                    'class_id': indexed(row, 'Casualty_Class'),
                    'sex_id': indexed(row, 'Sex_of_Casualty'),
                    'age': indexed(row, 'Age_of_Casualty'),
                    'age_band_id': indexed(row, 'Age_Band_of_Casualty'),
                    'severity_id': indexed(row, 'Casualty_Severity'),
                    'type_id': indexed(row, 'Casualty_Type'),
                    'pedestrian_location_id': indexed(row, 'Pedestrian_Location'),
                    'pedestrian_movement_id': indexed(row, 'Pedestrian_Movement')}
        casualties.append(casualty)

        if i % 10000 == 0:
            engine.execute(Casualty.__table__.insert(), casualties)
            casualties[:] = []
            print(i)

    engine.execute(Casualty.__table__.insert(), casualties)

if __name__ == '__main__':
    import sys
    from icw.api.app import get_app
    app = get_app()

    with open(sys.argv[1]) as f:
        load_accident(app, f)
