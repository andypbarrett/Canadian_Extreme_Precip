"""Generates plots of monthly time series for stations in Canadian Extreme Precip paper"""

from reader import read_combined_file
from filepath import COMBINED_PATH
from plotting import plot_climatology, monthly_series
from utils import to_monthly, to_climatology


def get_station_filelist():
    """Return list of station files"""
    station_files = {}
    for f in COMBINED_PATH.glob('*combined.csv'):
        station_name = ' '.join(f.stem.split('.')[0].split('_'))
        station_files[station_name] = f
    return station_files


if __name__ == "__main__":
    plotstation_monthly_time_series()

