'''
    api.py
    Sean Lyons
    April, 21 2020

    This is an upgraded version of the tsunami_year_count.py script.
    I will be implementing a Flask API to serve the tsunami data.
    The API will have the following endpoints:
        - /: Returns a simple greeting.
        - /help: Returns a simple help page.
        - /tsunami_count/<years>: Returns the number of tsunamis in a given year.
    
'''

import argparse
import os
import sys
import csv
import argparse
import flask
import json

app = flask.Flask(__name__)

@app.route('/')
def hello():
    ''' Returns a simple greeting. '''
    return 'Hello, this is the Tsunami Year Count API.'

@app.route('/help')
def get_help():
    ''' Returns a simple help page. '''
    return flask.render_template('help.html')


@app.route('/tsunami_count/<years>')
def get_tsunami_count(years):
    counts = []
    with open('../data/sources.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        data = list(reader)
        for year in years.split(','):
            count = 0
            year = int(year)
            for row in data:
                try:
                    if int(row[1]) == year:
                        count += 1
                except (ValueError, IndexError):
                    continue
            counts.append({'Year': year, 'Number of Tsunamis': count})
    return json.dumps(counts, indent = 4)
                
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)