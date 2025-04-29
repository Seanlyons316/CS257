#!/usr/bin/env python3
'''
    convert.py
    Sean Lyons Matvei Keshkekian , 29 April 2025
    Adapted from code by Jeff Ondich, 2025

    This program converts the waves.csv file into 4 separate more digestable files. Broken up by theme/topic.

    into separate CSV files with the formats:

        tsunamis_attribute.csv: Details not related to location and destruction. Size, period, etc.
        tsunamis_destruction.csv: Details related to destruction. Injuries, fatalities, damage, etc.
        tsunamis_place_time.csv: Details related to location and time. Region, country, state, etc.
        tsunamis_ids.csv: The source id and the wave id. This is used to identify which tsunamis came from the same earthquake source.

    Because everything about this is so specific, We've hard-coded quite a bit of information.
'''

import sys
import csv

def main():
    input_file_name = 'waves.csv'
    # Collect the data and assign ids to tsunamis and authors
    tsunamis_ids = []
    tsunamis_destruction = {}
    tsunamis_attribute = {}
    tsunamis_place_time = {}
    with open(input_file_name) as f:
        reader = csv.reader(f)
        next(f)  # Skip the header row
        for tsunami_row in reader:
            source_id = tsunami_row[0]
            wave_id = tsunami_row[1]
            year = tsunami_row[2]
            month = tsunami_row[3] if tsunami_row[3] else 'NULL'
            day = tsunami_row[4] if tsunami_row[4] else 'NULL'
            region_code = tsunami_row[5] 
            country = tsunami_row[6]
            state = tsunami_row[7] if tsunami_row[7] else 'NULL'
            location = tsunami_row[8] if tsunami_row[8] else 'NULL'
            latitude = tsunami_row[9] if tsunami_row[9] else 'NULL'
            longitude = tsunami_row[10] if tsunami_row[10] else 'NULL'
            distance_from_source = tsunami_row[11] if tsunami_row[11] else 'NULL'
            travel_time_hours = tsunami_row[12] if tsunami_row[12] else 'NULL'
            travel_time_minutes = tsunami_row[13] if tsunami_row[13] else 'NULL'
            validity = tsunami_row[14] if tsunami_row[14] else 'NULL'
            measurement_type = tsunami_row[15] if tsunami_row[15] else 'NULL'
            period = tsunami_row[16] if tsunami_row[16] else 'NULL'
            first_motion = tsunami_row[17] if tsunami_row[17] else 'NULL'
            maximum_height = tsunami_row[18] if tsunami_row[18] else 'NULL'
            horizontal_innundation = tsunami_row[19] if tsunami_row[19] else 'NULL'
            injuries = tsunami_row[20] if tsunami_row[20] else 'NULL'
            injuries_estimated = tsunami_row[21] if tsunami_row[21] else 'NULL'
            fatalities = tsunami_row[22] if tsunami_row[22] else 'NULL'
            fatalities_estimated = tsunami_row[23] if tsunami_row[23] else 'NULL'
            damage_millions_dollars = tsunami_row[24] if tsunami_row[24] else 'NULL'
            damage_estimated = tsunami_row[25] if tsunami_row[25] else 'NULL'
            houses_damaged = tsunami_row[26] if tsunami_row[26] else 'NULL'
            houses_damage_estimated = tsunami_row[27] if tsunami_row[27] else 'NULL'
            houses_destroyed = tsunami_row[28] if tsunami_row[28] else 'NULL'
            house_destruction_estimated = tsunami_row[29] if tsunami_row[29] else 'NULL'
            tsunami_attribute_key = f'{wave_id}+{year}+{month}+{day}'
            tsunami_destruction_key = f'{wave_id}+{year}+{month}+{day}'
            tsunami_place_time_key = f'{wave_id}+{year}+{month}+{day}'
            if tsunami_place_time_key not in tsunamis_destruction:
                tsunamis_place_time[tsunami_place_time_key] = {'id': wave_id,
                                                                'year': year,
                                                                'month': month,
                                                                'day': day,
                                                                'region_code': region_code,
                                                                'country': country,
                                                                'state': state,
                                                                'location': location,
                                                                'latitude': latitude,
                                                                'longitude': longitude}
            if tsunami_destruction_key not in tsunamis_destruction:
                tsunamis_destruction[tsunami_destruction_key] = {'id': wave_id,
                                                     'injuries': injuries,
                                                     'injuries_estimated': injuries_estimated,
                                                     'fatalities': fatalities,
                                                     'fatalities_estimated': fatalities_estimated,
                                                     'damage_millions_dollars': damage_millions_dollars,
                                                     'damage_estimated': damage_estimated,
                                                     'houses_damaged': houses_damaged,
                                                     'houses_damage_estimated': houses_damage_estimated,
                                                     'houses_destroyed': houses_destroyed,
                                                     'house_destruction_estimated': house_destruction_estimated}

            if tsunami_attribute_key not in tsunamis_attribute:
                tsunamis_attribute[tsunami_attribute_key] = {'id': wave_id,
                                    'source': source_id,
                                    'distance from source': distance_from_source,
                                    'travel time hours': travel_time_hours,
                                    'travel time minutes': travel_time_minutes,
                                    'validity': validity,
                                    'measurement type': measurement_type,
                                    'period': period,
                                    'first motion': first_motion,
                                    'maximum height': maximum_height,
                                    'horizontal inundation': horizontal_innundation}

            tsunamis_ids.append((source_id, wave_id))

    # Write to the table files
    with open('tsunamis_destruction.csv', 'w') as f:
        writer = csv.writer(f)
        for tsunami_destruction_key in tsunamis_destruction:
            tsunami_destruction = tsunamis_destruction[tsunami_destruction_key]
            row = (tsunami_destruction['id'], tsunami_destruction['injuries'],
                   tsunami_destruction['injuries_estimated'], tsunami_destruction['fatalities'],
                   tsunami_destruction['fatalities_estimated'], tsunami_destruction['damage_millions_dollars'],
                   tsunami_destruction['damage_estimated'], tsunami_destruction['houses_damaged'],
                   tsunami_destruction['houses_damage_estimated'], tsunami_destruction['houses_destroyed'],
                   tsunami_destruction['house_destruction_estimated'])
            writer.writerow(row)

    with open('tsunamis_attribute.csv', 'w') as f:
        writer = csv.writer(f)
        for tsunami_attribute_key in tsunamis_attribute:
            tsunami = tsunamis_attribute[tsunami_attribute_key]
            row = (tsunami['id'], tsunami['source'], tsunami['distance from source'],
                   tsunami['travel time hours'], tsunami['travel time minutes'], tsunami['validity'],
                   tsunami['measurement type'], tsunami['period'], tsunami['first motion'],
                   tsunami['maximum height'], tsunami['horizontal inundation'])
            writer.writerow(row)

    with open('tsunamis_place_time.csv', 'w') as f:
        writer = csv.writer(f)
        for tsunami_place_time_key in tsunamis_place_time:
            tsunami = tsunamis_place_time[tsunami_place_time_key]
            row = (tsunami['id'], tsunami['region_code'], tsunami['country'],
                   tsunami['state'], tsunami['location'], tsunami['latitude'], tsunami['longitude'])
            writer.writerow(row)

    with open('tsunamis_ids.csv', 'w') as f:
        writer = csv.writer(f)
        for wave_id, source_id in tsunamis_ids:
            writer.writerow((source_id, wave_id))

main()
