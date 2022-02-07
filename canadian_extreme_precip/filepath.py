'''Contains filepaths for data etc'''

from pathlib import Path

HOME = Path.home()

DATAPATH = HOME / 'Data' / 'Rain_on_snow'

RAW_STATION_PATH = DATAPATH / 'Canada_extreme_precip' / 'Raw_station_files'
COMBINED_PATH = DATAPATH / 'Canada_extreme_precip' / 'Combined_files'


def raw_station_filepath(climate_identifier):
    '''Returns filepath for station file

    :climate_identifier: numeric station id

    :returns: filepath pathlib Path object'''
    return RAW_STATION_PATH / f'{climate_identifier}_climate_daily.csv'
