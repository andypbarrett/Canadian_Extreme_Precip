'''Contains filepaths for data etc'''

from pathlib import Path

HOME = Path.home()

DATAPATH = HOME / 'Data' / 'Rain_on_snow' / 'Canada_extreme_precip'

RAW_STATION_PATH = DATAPATH / 'Raw_station_files'
COMBINED_PATH = DATAPATH / 'Combined_files'
FIGURE_PATH = DATAPATH / 'Figures'


def raw_station_filepath(climate_identifier):
    '''Returns filepath for station file

    :climate_identifier: numeric station id

    :returns: filepath pathlib Path object'''
    return RAW_STATION_PATH / f'{climate_identifier}_climate_daily.csv'


def combined_station_filelist():
    """Return list of station files"""
    station_files = {}
    for f in COMBINED_PATH.glob('*combined.csv'):
        station_name = ' '.join(f.stem.split('.')[0].split('_'))
        station_files[station_name] = f
    return station_files
