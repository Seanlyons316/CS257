'''
    cli.py
    Sean Lyons
    April, 21 2020

    Example of how to use the standard argparse module to learn about a csv files. When the user inputs a year the number of tsunamis that occured that year will be returned.

    Try a few ways of using the arguments:

        python3 cli.py <year>
    Notes:
'''

import argparse
import csv
import os
import sys

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Report on the number tsunamis in a given year')
    parser.add_argument('year', metavar='year', nargs='+', help='one or more years in which you want to know the number of tsunamis')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def get_tsunami_count(year):
    ''' Returns the number of tsunamis in a given year. '''
    count = 0
    with open('../data/tsunamis.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            try:
                if int(row[1]) == year:
                    count += 1
            except (ValueError, IndexError):
                continue  # Skip malformed rows
    return count


def main():
    parsed_arguments = get_parsed_arguments()
    years = parsed_arguments.year
    for year in years:
        try:
            year = int(year)
            count = get_tsunami_count(year)
            print(f'There were {count} tsunamis in {year}.')
        except ValueError:
            print(f'Invalid year: {year}. Please enter a valid year.')

if __name__ == '__main__':
    main()
