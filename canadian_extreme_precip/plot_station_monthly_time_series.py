"""Generates plots of monthly time series for stations in
   Canadian Extreme Precip paper"""

import matplotlib.pyplot as plt

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


def plot_station_monthly_time_series():
    for station, filepath in get_station_filelist().items():
        df = read_combined_file(filepath)
        df_mon = to_monthly(df)

        fig, ax = plt.subplots(3, 1, figsize=(15, 15))
        monthly_series(df_mon, ax)
        plt.show()

    return


if __name__ == "__main__":
    plot_station_monthly_time_series()

