'''Readers for files'''

import pandas as pd


column_dtype = {
    'MEAN_TEMPERATURE_FLAG': str,
    'MIN_TEMPERATURE_FLAG': str,
    'MAX_TEMPERATURE_FLAG': str,
    'TOTAL_PRECIPITATION_FLAG': str,
    'TOTAL_RAIN_FLAG': str,
    'TOTAL_SNOW_FLAG': str,
    'SNOW_ON_GROUND_FLAG': str,
    'DIRECTION_MAX_GUST_FLAG': str,
    'SPEED_MAX_GUST_FLAG': str,
    'COOLING_DEGREE_DAYS_FLAG': str,
    'HEATING_DEGREE_DAYS_FLAG': str,
    'MIN_REL_HUMIDITY_FLAG': str,
    'MAX_REL_HUMIDITY_FLAG': str,
    }


def read_station_file(station_file):
    '''Reads raw station file
    A description of Flags is here
    https://climate.weather.gc.ca/doc/Technical_Documentation.pdf'''
    df = pd.read_csv(station_file, index_col='LOCAL_DATE',
                     dtype=column_dtype, parse_dates=True)
    return df
