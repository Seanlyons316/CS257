#!/usr/bin/env python3
'''
    psycopg2-sample.py
    Jeff Ondich, 23 April 2016

    A very short, demo of how to use psycopg2 to connect to
    and query a PostgreSQL database. This demo assumes a "books"
    database like the one I've used in CS257 for the past few years,
    including an authors table with fields

        (id, given_name, surname, birth_year, death_year)

    You might also want to consult the official psycopg2 tutorial
    at https://wiki.postgresql.org/wiki/Psycopg2_Tutorial.

    Also, SEE THE NOTE BELOW ABOUT config.py. It's important.
'''
import sys
import psycopg2
import flask
import json

app = flask.Flask(__name__)

# We're going to import our postgres username, password,
# and database from a file named config.py, like so:
import config


def get_connection():
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/tsunamis')
def get_tsunamis():
    ''' Returns a list of all the tsunamis and all of their info". '''
    tsunamis = []
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the query
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunami_destruction.WAVE_ID 
        AND tsunami_destruction.WAVE_ID = tsunami_place_time.WAVE_ID 
        ORDER BY wave_YEAR DESC'''
        cursor.execute(query)

        # Iterate over the query results to produce the list of author names.
        for row in cursor:
            tsunamis.append({'source id': row[0],
                            'wave id': row[1],
                            'distance from source': row[2],
                            'travel time_hours': row[3],
                            'validity': row[4],
                            'measurement type': row[5],
                            'wave period': row[6],
                            'first motion': row[7],
                            'max_height': row[8],
                            'horizontal innundation': row[9],
                            'injuries': row[10],
                            'injury estimate': row[11],
                            'deaths': row[12],
                            'death estimate': row[13],
                            'houses damaged': row[14],
                            'houses damaged estimate': row[15],
                            'houses destroyed': row[16],
                            'houses destroyed estimate': row[17],
                            'region code': row[18],
                            'country': row[19],
                            'wave year': row[20],
                            'wave month': row[21],
                            'wave day': row[22],
                            'state': row[23],
                            'location': row[24],
                            'latitude': row[25],
                            'longitude': row[26]
                            })

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return json.dumps(tsunamis)

@app.route('/tsunamis/country_name', methods=['GET'])
def get_tsunamis_by_country():
    country_name = flask.request.args.get('country')
    tsunamis = []
    try:
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunami_destruction.WAVE_ID 
        AND tsunami_destruction.WAVE_ID = tsunami_place_time.WAVE_ID 
        AND tsunamis_place_time.country = %s
        ORDER BY wave_YEAR DESC'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (country_name,))
        for row in cursor:
            tsunamis.append({'source id': row[0],
                            'wave id': row[1],
                            'distance from source': row[2],
                            'travel time_hours': row[3],
                            'validity': row[4],
                            'measurement type': row[5],
                            'wave period': row[6],
                            'first motion': row[7],
                            'max_height': row[8],
                            'horizontal innundation': row[9],
                            'injuries': row[10],
                            'injury estimate': row[11],
                            'deaths': row[12],
                            'death estimate': row[13],
                            'houses damaged': row[14],
                            'houses damaged estimate': row[15],
                            'houses destroyed': row[16],
                            'houses destroyed estimate': row[17],
                            'region code': row[18],
                            'country': row[19],
                            'wave year': row[20],
                            'wave month': row[21],
                            'wave day': row[22],
                            'state': row[23],
                            'location': row[24],
                            'latitude': row[25],
                            'longitude': row[26]
                            })
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return tsunamis


@app.route('/tsunamis/id', methods=['GET'])
def get_tsunamis_by_wave_id():

    id = flask.request.args.get('id', type=int)
    tsunamis = []
    try:
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunami_destruction.WAVE_ID
        AND tsunami_destruction.WAVE_ID = tsunami_place_time.WAVE_ID
        AND tsunamis_attribute.WAVE_ID = %d'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        for row in cursor:
            tsunamis.append({'source id': row[0],
                            'wave id': row[1],
                            'distance from source': row[2],
                            'travel time_hours': row[3],
                            'validity': row[4],
                            'measurement type': row[5],
                            'wave period': row[6],
                            'first motion': row[7],
                            'max_height': row[8],
                            'horizontal innundation': row[9],
                            'injuries': row[10],
                            'injury estimate': row[11],
                            'deaths': row[12],
                            'death estimate': row[13],
                            'houses damaged': row[14],
                            'houses damaged estimate': row[15],
                            'houses destroyed': row[16],
                            'houses destroyed estimate': row[17],
                            'region code': row[18],
                            'country': row[19],
                            'wave year': row[20],
                            'wave month': row[21],
                            'wave day': row[22],
                            'state': row[23],
                            'location': row[24],
                            'latitude': row[25],
                            'longitude': row[26]
                            })

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return tsunamis



@app.route('/tsunamis/years', methods=['GET'])
def get_tsunamis_by_year_range():
    before = flask.request.args.get('start_year', type=float)
    after = flask.request.args.get('end_year', type=float)

    tsunamis = []
    try:
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunami_destruction.WAVE_ID 
        AND tsunami_destruction.WAVE_ID = tsunami_place_time.WAVE_ID 
        AND wave_year BETWEEN %f AND %f
        ORDER BY wave_YEAR DESC'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (after, before))
        for row in cursor:
            tsunamis.append({'source id': row[0],
                            'wave id': row[1],
                            'distance from source': row[2],
                            'travel time_hours': row[3],
                            'validity': row[4],
                            'measurement type': row[5],
                            'wave period': row[6],
                            'first motion': row[7],
                            'max_height': row[8],
                            'horizontal innundation': row[9],
                            'injuries': row[10],
                            'injury estimate': row[11],
                            'deaths': row[12],
                            'death estimate': row[13],
                            'houses damaged': row[14],
                            'houses damaged estimate': row[15],
                            'houses destroyed': row[16],
                            'houses destroyed estimate': row[17],
                            'region code': row[18],
                            'country': row[19],
                            'wave year': row[20],
                            'wave month': row[21],
                            'wave day': row[22],
                            'state': row[23],
                            'location': row[24],
                            'latitude': row[25],
                            'longitude': row[26]
                            })

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return tsunamis

def get_tsunamis_by_country_and_year_range():
    country = flask.request.args.get('country', type=str)
    start_year = flask.request.args.get('start_year', type=float)
    end_year = flask.request.args.get('end_year', type=float)
    tsunamis = []
    try:
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunami_destruction.WAVE_ID 
        AND tsunami_destruction.WAVE_ID = tsunami_place_time.WAVE_ID 
        AND wave_year BETWEEN %f AND %f
        AND country = %s
        ORDER BY wave_YEAR DESC'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (start_year, end_year, country))
        for row in cursor:
            tsunamis.append({'source id': row[0],
                            'wave id': row[1],
                            'distance from source': row[2],
                            'travel time_hours': row[3],
                            'validity': row[4],
                            'measurement type': row[5],
                            'wave period': row[6],
                            'first motion': row[7],
                            'max_height': row[8],
                            'horizontal innundation': row[9],
                            'injuries': row[10],
                            'injury estimate': row[11],
                            'deaths': row[12],
                            'death estimate': row[13],
                            'houses damaged': row[14],
                            'houses damaged estimate': row[15],
                            'houses destroyed': row[16],
                            'houses destroyed estimate': row[17],
                            'region code': row[18],
                            'country': row[19],
                            'wave year': row[20],
                            'wave month': row[21],
                            'wave day': row[22],
                            'state': row[23],
                            'location': row[24],
                            'latitude': row[25],
                            'longitude': row[26]
                            })

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return tsunamis


def main():
    # Example #1: get a list of author names
    print('========== All authors ==========')
    authors = get_authors()
    for author in authors:
        print(f"{author['given_name']} {author['surname']}")
    print()

    # Example #2: get a list of authors whose surnames equal a search string
    surname = 'Brontë'
    print(f'========== All authors with surname "{surname}" ==========')
    authors = get_authors_by_surname(surname)
    for author in authors:
        print(f"{author['given_name']} {author['surname']}")
    print()

    # Example #3: get a list of authors whose surnames contain a search string
    search_text = 'is'
    print(f'========== All authors whose surnames contain "{search_text}" ==========')
    authors = get_matching_authors(search_text)
    for author in authors:
        print(f"{author['given_name']} {author['surname']}")
    print()


if __name__ == '__main__':
    main()

