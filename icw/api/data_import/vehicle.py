import csv

from icw.api.data_import.common import indexed, load_table_main
from ..db import Vehicle


def sex_indexed(row, name):
    value = int(row[name])
    if value in (1, 2):
        return value


def row_parser(row):
    return {
        'accident_id': row['\ufeffAccident_Index'],
        'vehicle_ref': int(row['Vehicle_Reference']),
        'type_id': indexed(row, 'Vehicle_Type'),
        'driver_sex_id': sex_indexed(row, 'Sex_of_Driver'),
        'driver_age': indexed(row, 'Age_of_Driver'),
        'driver_age_band_id': indexed(row, 'Age_Band_of_Driver'),
        'manoeuvre_id': indexed(row, 'Vehicle_Manoeuvre'),
        'location_id': indexed(row, 'Vehicle_Location-Restricted_Lane'),
        'towing_and_articulation_id': indexed(row, 'Towing_and_Articulation'),
        'junction_location_id': indexed(row, 'Junction_Location'),
        'skidding_and_overturning_id': indexed(row, 'Skidding_and_Overturning'),
        'hit_object_in_carriageway_id': indexed(row, 'Hit_Object_in_Carriageway'),
        'hit_object_off_carriageway_id': indexed(row, 'Hit_Object_off_Carriageway'),
        'first_point_of_impact_id': indexed(row, '1st_Point_of_Impact'),
        'leaving_carriageway_id': indexed(row, 'Vehicle_Leaving_Carriageway'),
    }


if __name__ == '__main__':
    load_table_main(Vehicle, row_parser)
