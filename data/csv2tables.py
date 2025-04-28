#!/usr/bin/env python3
'''
    csv2tables.py
    Jeff Ondich, 24 April 2025

    This program converts a CSV file with the format

        title,publication-year,author-surname,author-given-name,author-birth-year,author-death-year

    into separate CSV files with the formats:

        authors.csv: id,surname,given-name,birth-year,death-year
        tsunamis.csv: id,title,publication-year
        tsunamis_authors.csv: tsunami_id,author_id

    Because everything about this is so specific, I've hard-coded quite a bit of information.
'''

import sys
import csv

def main(input_file_name):
    # Collect the data and assign ids to tsunamis and authors
    tsunamis_destruction = {}
    tsunamis_attribute = {}
    with open(input_file_name) as f:
        reader = csv.reader(f)
        reader(next)
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
            if tsunami_key not in tsunamis:
                tsunamis[tsunami_key] = {'id': len(tsunamis),
                                   'title': title,
                                   'publication_year': publication_year}

            if author_key not in authors:
                authors[author_key] = {'id': wave_id,
                                       'surname': surname,
                                       'given_name': given_name,
                                       'birth_year': birth_year,
                                       'death_year': death_year}

            tsunamis_authors.append((authors[author_key]['id'], tsunamis[tsunami_key]['id']))

    # Write to the table files
    with open('authors.csv', 'w') as f:
        writer = csv.writer(f)
        for author_key in authors:
            author = authors[author_key]
            row = (author['id'], author['surname'], author['given_name'], author['birth_year'], author['death_year'])
            writer.writerow(row)

    with open('tsunamis.csv', 'w') as f:
        writer = csv.writer(f)
        for tsunami_key in tsunamis:
            tsunami = tsunamis[tsunami_key]
            row = (tsunami['id'], tsunami['title'], tsunami['publication_year'])
            writer.writerow(row)

    with open('tsunamis_authors.csv', 'w') as f:
        writer = csv.writer(f)
        for tsunami_id, author_id in tsunamis_authors:
            writer.writerow((tsunami_id, author_id))

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} original_csv_file', file=sys.stderr)
    exit()

main(sys.argv[1])
