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
import argparse

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
@app.route('/')
def hello():
    ''' Returns a simple greeting. '''
    return 'Hello, this is the Tsunami Year Count API.'

@app.route('/help')
def get_help():
    ''' Returns a simple help page. '''
    return flask.render_template('help.html')

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
        WHERE tsunamis_attribute.WAVE_ID = tsunamis_destruction.WAVE_ID 
        AND tsunamis_destruction.WAVE_ID = tsunamis_place_time.WAVE_ID 
        ORDER BY wave_YEAR DESC
        LIMIT 10'''
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
    return tsunamis

@app.route('/tsunamis/country_name', methods=['GET'])
def get_tsunamis_by_country():
    country_name = flask.request.args.get('country')
    tsunamis = []
    try:
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunamis_destruction.WAVE_ID 
        AND tsunamis_destruction.WAVE_ID = tsunamis_place_time.WAVE_ID 
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
        WHERE tsunamis_attribute.WAVE_ID = tsunamis_destruction.WAVE_ID
        AND tsunamis_destruction.WAVE_ID = tsunamis_place_time.WAVE_ID
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
        WHERE tsunamis_attribute.WAVE_ID = tsunamis_destruction.WAVE_ID 
        AND tsunamis_destruction.WAVE_ID = tsunamis_place_time.WAVE_ID 
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
    print(type(tsunamis))
    try:
        query = '''SELECT * FROM tsunamis_attribute, tsunamis_destruction, tsunamis_place_time
        WHERE tsunamis_attribute.WAVE_ID = tsunamis_destruction.WAVE_ID 
        AND tsunamis_destruction.WAVE_ID = tsunamis_place_time.WAVE_ID 
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
    #Example #1: get a list of tsunamis
    print('========== All tsunamis ==========')
    tsunamis = get_tsunamis()
    for tsunami in tsunamis:
        print(type(tsunami))
        print(f"{tsunami['wave year']} {tsunami['country']}")
    print()

    # Example #2: get a list of tsunamis by country
    country = 'Japan'
    print(f'========== All tsunamis in "{country}" ==========')
    tsunamis = get_tsunamis_by_country(country)
    
    for tsunami in tsunamis:

        print(f"{tsunami['wave year']} {tsunami['country']}")
    print()

    # Example #3: get a list of tsunamis by year range
    start_year = 1900
    end_year = 1999
    print(f'========== All tsunamis between "{start_year}" and "{end_year}" ==========')
    tsunamis = get_tsunamis_by_year_range(start_year, end_year)
    for tsunami in tsunamis:
        print(f"{tsunami['wave year']} {tsunami['country']}")
    print()

    # Example #4: get a list of tsunamis in a country by year range
    country = 'Japan'
    start_year = 1900
    end_year = 1999
    print(f'========== All tsunamis in "{country}" between "{start_year}" and "{end_year}" ==========')
    tsunamis = get_tsunamis_by_country_and_year_range(country, start_year, end_year)
    for tsunami in tsunamis:
        print(f"{tsunami['wave year']} {tsunami['country']}")
    print()

    # Example #5: get a list of tsunamis by wave id
    wave_id = 59
    print(f'========== All tsunamis with wave id "{wave_id}" ==========')
    tsunamis = get_tsunamis_by_wave_id(wave_id)
    for tsunami in tsunamis:
        print(f"{tsunamis}")
    print()



if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

