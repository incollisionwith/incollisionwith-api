import csv
import datetime

from astral import Astral
import pytz

from icw.db import Accident

def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value


def load_accident(app, f):
    reader = csv.DictReader(f)

    session = app['db-session']()
    timezone = pytz.timezone('Europe/London')
    astral = Astral()

    for i, row in enumerate(reader):
        date = datetime.datetime.strptime(row['Date'], '%d/%m/%Y').date()
        if row['Time']:
            date_and_time = datetime.datetime.strptime(row['Date'].strip() + ' ' + row['Time'].strip(),
                                                      '%d/%m/%Y %H:%M')
            date_and_time = timezone.localize(date_and_time)
        else:
            date_and_time = None

        try:
            longitude, latitude = float(row['Longitude']), float(row['Latitude'])
            location = 'SRID=4326;POINT({} {})'.format(longitude, latitude)
        except ValueError:
            location = None

        if location and date_and_time:
            solar_elevation = astral.solar_elevation(date_and_time, latitude, longitude)
        else:
            solar_elevation = None

        moon_phase = astral.moon_phase(date)

        try:
            accident = Accident(id=row['\ufeffAccident_Index'],
                                location=location,
                                police_force_id=row['Police_Force'],
                                severity_id=row['Accident_Severity'],
                                number_of_vehicles=int(row['Number_of_Vehicles']),
                                number_of_casualties=int(row['Number_of_Casualties']),
                                date=date,
                                date_and_time=date_and_time,
                                police_attended=row['Did_Police_Officer_Attend_Scene_of_Accident'] == '1',
                                junction_control_id=indexed(row, 'Junction_Control'),
                                junction_detail_id=indexed(row, 'Junction_Detail'),
                                moon_phase=moon_phase,
                                solar_elevation=solar_elevation)
            session.merge(accident)
        except:
            raise
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
