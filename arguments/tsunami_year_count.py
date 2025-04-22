'''
    tsunami_year_count.py
    Sean Lyons
    April, 21 2020

    Example of how to use the standard argparse module to learn about a csv files. When the user inputs a year the number of tsunamis that occured that year will be returned.

    Try a few ways of using the arguments:

        python3 tsunami_year_count.py <year>
    Notes:
'''

import argparse
import pandas as pd
import os
import sys

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Report on the number tsunamis in a given year')
    parser.add_argument('year', metavar='year', nargs='+', help='one or more years in which you want to know the number of tsunamis')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def get_tsunami_count(year):
    tsunamis = pd.read_csv(r'C:\Users\seanl\CS257\data\tsunamis.csv')
    if year < -2000 or year > 2017:
        print(f'Year {year} is out of range. Please enter a year between -2000 and 2017.')
        return 0
    if year in tsunamis['YEAR'].values:
        count = tsunamis[tsunamis['YEAR'] == year].shape[0]
        return count
    else:
        return 0

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
