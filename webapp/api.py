#!/usr/bin/env python3
'''
    Adapted by Sean Lyons and Matvei Keshkekian, May 2025
    May 2025, Software Design API implementation
    Original code by Jeff Ondich, 23 April 2016

    This is a flask web application that provides an API for the Tsunami database. 
    It makes use of the psycopg2 library to connect to a PostgreSQL database and retrieve data from it. 

    It provides the following endpoints:
    /tsunamis/:    Returns a list of tsunamis with optional filtering by country and year range with pages. 
    /tsunami/id:  Returns a single tsunami by its wave id.
    /help: Returns a simple help page.
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


# After much trial and error, I decided to use a function to generate the query separately from the execution.
# This allows us to reuse the query generation logic for both the main query and the count query.
def query_func(conditions, params, page, page_size, sort_column, sort_order):
    query = f'''SELECT ta.source_id, ta.WAVE_ID, ta.distance_from_source, ta.travel_time_hours,
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
    WHERE {conditions}
    ORDER BY {sort_column} {sort_order}
    LIMIT %s OFFSET %s;
    '''

    count_query = f'''SELECT COUNT(*) FROM tsunamis_attribute AS ta
    JOIN tsunamis_destruction AS td ON ta.WAVE_ID = td.WAVE_ID
    JOIN tsunamis_place_time AS tp ON ta.WAVE_ID = tp.WAVE_ID
    WHERE {conditions}'''

    offset = (page - 1) * page_size
    return query, count_query, params + [page_size, offset], params

#This is the workhorse of the search list functionality.
@app.route('/tsunamis/', methods=['GET'])
def get_pages_combined_tsunamis():
    ''' Returns a list of tsunamis with optional filtering by country and year range with pages. Additionally, it allows sorting by various fields. '''

    country = flask.request.args.get('country', type=str)
    start_year = flask.request.args.get('start_year', type=float)
    end_year = flask.request.args.get('end_year', type=float)
    page_size = flask.request.args.get('page_size', default=25, type=int)
    page = flask.request.args.get('page', default=1, type=int)
    sort_field = flask.request.args.get('sort_field', default='wave year', type=str).lower()
    sort_order = flask.request.args.get('sort_order', default='desc', type=str).lower()
    #To prevet SQL injection,using a dictionary to map sort fields to their SQL equivalents.
    valid_sort_fields = {
    "distance from source": "ta.distance_from_source",
    "travel time_hours": "ta.travel_time_hours",
    "validity": "ta.validity",
    "wave period": "ta.wave_period",
    "max_height": "ta.maximum_height",
    "horizontal inundation": "ta.horizonrtal_innundation",
    "injuries": "td.injuries",
    "fatalities": "td.fatalities",
    "houses damaged": "td.houses_damaged",
    "houses destroyed": "td.houses_destroyed",
    "wave year": "tp.wave_year",
    "wave month": "tp.wave_month"
    }
    # Default sort field if one is not provided or invalid.
    sort_column = valid_sort_fields.get(sort_field, 'tp.wave_year')
    sort_order = 'DESC' if sort_order == 'desc' else 'ASC'
    tsunamis = []
    parameters = []
    conditions = []
    total_count = 0
    # If the sort order is not valid, default to ascending order.
    sort_order = "DESC" if sort_order == "desc" else "ASC"

    # Build the conditions based on the provided parameters.
    if country is not None:
        #All country names are stored in uppercase in the database, so we convert the input to uppercase.
        country = str.upper(country)
        conditions.append('tp.country LIKE %s')
        parameters.append(country)
    # If both start_year and end_year are provided, then check if they are equal, different, or if one is missing and then buld the conditions accordingly.
    if start_year is not None and end_year is not None:
        if start_year > end_year:
            return 'Please provide a start year that is less than the end year.'
        if start_year == end_year:
            conditions.append('tp.wave_year = %s')
            parameters.append(start_year)
        else:
            conditions.append('tp.wave_year BETWEEN %s AND %s')
            parameters.extend([start_year, end_year])
    elif start_year is not None:
        conditions.append('tp.wave_year = %s')
        parameters.append(start_year)
    elif end_year is not None:
        conditions = ['tp.wave_year = %s']
        parameters.append(end_year)
    # If no conditions are provided, return an error message.
    if not conditions:
        return flask.jsonify({'error': 'Please provide at least one filter parameter.'}), 400
    # Join the conditions with 'AND' to form the WHERE clause.
    # This is to prevent SQL injection attacks.
    conditions = ' AND '.join(conditions)
    try: 
        # Get the query and country query using the query function
        query, count_query, query_params, count_params = query_func(conditions, parameters, page, page_size, sort_column, sort_order)
        connection = get_connection()
        cursor = connection.cursor()
        # Execute the count query to get the total number of results and ensure pages are calculated correctly.
        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()[0]
        # Execute the main query to get the results.
        cursor.execute(query, query_params)
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
        connection.close()
        # Return the results from both the main query and the count query.
        return flask.jsonify({
            'tsunamis': tsunamis,
            'total_count': total_count,
            'page_size': page_size,
            'page': page
        })
    except Exception as e:
        print(e, file=sys.stderr)
        return flask.jsonify({'error': str(e)}), 500

#This is what is used to grab an individual tsunami by its id.
#Which is used on the tsunami info page.
@app.route('/tsunami/id', methods=['GET'])
def get_tsunamis_by_wave_id():
    ''' Returns a list of all the tsunamis and all of their info by wave id. '''
    id = flask.request.args.get('id', type=int)
    tsunamis = []
    parameters = []
    if id is not None:
        parameters.append(id)
    else:
        return 'Please provide a wave id.'
    try:
        #We dont use the query function here because it is a single result and thus no need for pages and sorting.
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
    return json.dumps(tsunamis, indent = 4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
