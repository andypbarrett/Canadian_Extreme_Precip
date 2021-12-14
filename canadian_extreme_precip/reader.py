'''Readers for files'''

import pandas as pd


def read_station_file(station_file):
    '''Reads raw station file'''
    df = pd.read_csv(station_file, index_col='LOCAL_DATE', parse_dates=True)
    return df
