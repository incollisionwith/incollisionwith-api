import datetime
from functools import partial

from astral import Astral
import pytz

from icw.api.data_import.common import load_table_main, indexed
from ..db import Accident


def get_accident_dict(timezone, astral, row):
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

    return dict(
        id=row['\ufeffAccident_Index'],
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
        solar_elevation=solar_elevation,
        light_conditions_id=indexed(row, 'Light_Conditions'),
        pedestrian_crossing_human_id=indexed(row, 'Pedestrian_Crossing-Human_Control'),
        pedestrian_crossing_physical_id=indexed(row, 'Pedestrian_Crossing-Physical_Facilities'),
        weather_id=indexed(row, 'Weather_Conditions'),
        road_surface_id=indexed(row, 'Road_Surface_Conditions'),
        road_type_id=indexed(row, 'Road_Type'),
        special_conditions_id=indexed(row, 'Special_Conditions_at_Site'),
        carriageway_hazards_id=indexed(row, 'Carriageway_Hazards'),
        urban_rural_id=indexed(row, 'Urban_or_Rural_Area'),
        road_1_class=indexed(row, '1st_Road_Class'),
        road_2_class=indexed(row, '2nd_Road_Class'),
        road_1_number=indexed(row, '1st_Road_Number'),
        road_2_number=indexed(row, '2nd_Road_Number'),
        speed_limit=indexed(row, 'Speed_limit'),
        )

if __name__ == '__main__':
    timezone = pytz.timezone('Europe/London')
    astral = Astral()
    row_parser = partial(get_accident_dict, timezone, astral)
    load_table_main(Accident, row_parser)
