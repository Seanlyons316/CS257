#!/usr/bin/env python3
'''
    Adapted by Sean Lyons and Matvei Keshkekian, May 2025
    May 2025, Software Design API implementation
    Original code by Jeff Ondich, 23 April 2016

    This is a flask web application that provides an API for the Tsunami database. 
    It makes use of the psycopg2 library to connect to a PostgreSQL database and retrieve data from it. 

    It provides the following endpoints:
    /tsunamis: Returns a list of all the tsunamis and all of their info.
    /tsunamis/all_ids: Returns a list of all the ids.
    /tsunamis/all_countries: Returns a list of all the countries that have tsunamis.
    /tsunamis/country_name: Returns a list of all the tsunamis that occured in a specific country and their related info.
    /tsunamis/id: Returns a list with just the tsunami matching that id and its related info.
    /tsunamis/years: Returns a list of all the tsuamis and all of their info between a start and end year.
    /tsunamis/country_years: Returns a list of all the tsuamis and all of their info between a start and end year in a specific country.
    /tsunamis/help: Returns a simple help page.
    /: Returns a simple greeting.
'''
import sys
import psycopg2
import flask
import json
import argparse

# We're going to import our postgres username, password,
# and database from a file named config.py, like so:
import config

app = flask.Blueprint('api', __name__)

def get_connection():
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/help')
def get_help():
    ''' Returns a simple help page. '''
    return flask.render_template('help.html')

@app.route('/tsunamis/', methods=['GET'])
def get_combined_tsunamis():
    ''' Returns a list of tsunamis with optional filtering by country and year range. '''
    country = flask.request.args.get('country', type=str)
    start_year = flask.request.args.get('start_year', type=float)
    end_year = flask.request.args.get('end_year', type=float)
    tsunamis = []
    parameters = []
    if country is not None and start_year is not None and end_year is not None and start_year == end_year:
        country = str.upper(country)
        parameters.append(country)
        parameters.append(start_year)
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.country LIKE %s 
            AND tp.wave_year = %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
                                'location' : row[24],
                                'latitude': row[25],
                                'longitude': row[26]
                                })
        except Exception as e:
            print(e, file=sys.stderr)
    elif country is None and start_year is not None and end_year is not None and start_year == end_year:
        parameters.append(start_year)
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.wave_year = %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
                                'location' : row[24],
                                'latitude': row[25],
                                'longitude': row[26]
                                })
        except Exception as e:
            print(e, file=sys.stderr)
    elif country is not None and start_year is not None and end_year is not None:
        country = str.upper(country)
        parameters.append(country)
        parameters.append(start_year)
        parameters.append(end_year)
        try:
            query = '''
            SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
                ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
                ta.maximum_height, ta.horizonrtal_innundation,
                td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
                td.houses_damaged, td.house_damage_estimate,
                td.houses_destroyed, td.house_destruction_estimate,
                tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
                tp.wave_state, tp.wave_location, tp.latitude, tp.longitude
                FROM tsunamis_attribute AS ta
                JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
                JOIN tsunamis_place_time AS tp ON ta.WAVE_ID = tp.WAVE_ID
                WHERE tp.country LIKE %s
                AND tp.wave_year BETWEEN %s AND %s
                ORDER BY tp.wave_year DESC;
            '''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
    elif (start_year is not None and country is not None):
        country = str.upper(country)
        parameters.append(country)
        parameters.append(start_year)
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time  AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.country LIKE %s
            AND tp.wave_year = %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
    elif (end_year is not None and country is not None):
        country = str.upper(country)
        parameters.append(country)
        parameters.append(end_year)
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time  AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.country LIKE %s
            AND tp.wave_year = %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
                                'location' : row[24],
                                'latitude': row[25],
                                'longitude': row[26]
                                })
        except Exception as e:
            print(e, file=sys.stderr)
    elif country is not None:
        country = str.upper(country)
        parameters.append(country)
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time  AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.country LIKE %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
    elif start_year is not None and end_year is not None:
        parameters.append(start_year)
        parameters.append(end_year)
        if start_year > end_year:
            return 'Please provide a start year that is less than the end year.'
        if start_year == end_year:
            return 'Please provide a start year that is not equal to the end year.'
        if start_year < -2000 or end_year > 2023:
            return 'Please provide a start year that is greater than -2000 and an end year that is less than 2023.'
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time  AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.wave_year BETWEEN %s AND %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
    elif start_year is not None:
        parameters.append(start_year)
        try:
            query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
            ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
            ta.maximum_height, ta.horizonrtal_innundation,
            td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
            td.houses_damaged, td.house_damage_estimate,
            td.houses_destroyed, td.house_destruction_estimate,
            tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
            tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time  AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.wave_year = %s
            ORDER BY tp.wave_year DESC;'''
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
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
                                'horizonrtal innundation': row[9],
                                'injuries': row[10],
                                'injury estimate': row[11],
                                'fatalities': row[12],
                                'fatality estimate': row[13],
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
    elif end_year is not None:
        parameters.append(end_year)
        try:
            query = '''
            SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
                ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
                ta.maximum_height, ta.horizonrtal_innundation,
                td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
                td.houses_damaged, td.house_damage_estimate,
                td.houses_destroyed, td.house_destruction_estimate,
                tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
                tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
            FROM tsunamis_attribute AS ta
            JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
            JOIN tsunamis_place_time AS tp ON ta.WAVE_ID = tp.WAVE_ID
            WHERE tp.wave_year = %s
            ORDER BY tp.wave_year DESC;'''
            
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, parameters)
            tsunamis = []  # Reset explicitly here
            for row in cursor:
                tsunamis.append({
                    'source id': row[0],
                    'wave id': row[1],
                    'distance from source': row[2],
                    'travel time_hours': row[3],
                    'validity': row[4],
                    'measurement type': row[5],
                    'wave period': row[6],
                    'first motion': row[7],
                    'max_height': row[8],
                    'horizonrtal innundation': row[9],
                    'injuries': row[10],
                    'injury estimate': row[11],
                    'fatalities': row[12],
                    'fatality estimate': row[13],
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
    else:
        return 'Please provide a country, start year, or end year.'
        

    connection.close()
    print(tsunamis)
    return json.dumps(tsunamis, indent=4)

@app.route('/tsunami/id', methods=['GET'])
def get_tsunamis_by_wave_id():
    ''' Returns a list of all the tsunamis and all of their info by wave id. '''
    id = flask.request.args.get('id', type=int)
    print(id)
    tsunamis = []
    parameters = []
    if id is not None:
        parameters.append(id)
    else:
        return 'Please provide a wave id.'
    try:
        query = '''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
        ta.validity, ta.measurement_type, ta.wave_period, ta.first_motion,
        ta.maximum_height, ta.horizonrtal_innundation,
        td.injuries, td.injury_estimate, td.fatalities, td.fatality_estimate,
        td.houses_damaged, td.house_damage_estimate,
        td.houses_destroyed, td.house_destruction_estimate,
        tp.region_code, tp.country, tp.wave_year, tp.wave_month, tp.wave_day,
        tp.wave_state, tp.wave_location, tp.latitude, tp.longitude 
        FROM tsunamis_attribute AS ta, tsunamis_destruction AS td, tsunamis_place_time AS tp
        WHERE ta.WAVE_ID = td.WAVE_ID AND ta.WAVE_ID = tp.WAVE_ID
        AND ta.WAVE_ID = %s
        ORDER BY tp.wave_year DESC;'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
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
                            'horizonrtal innundation': row[9],
                            'injuries': row[10],
                            'injury estimate': row[11],
                            'fatalities': row[12],
                            'fatality estimate': row[13],
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
    print(tsunamis)
    return json.dumps(tsunamis, indent = 4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
