"""Generates plots of monthly time series for stations in
   Canadian Extreme Precip paper"""

import matplotlib.pyplot as plt

from reader import read_combined_file
from filepath import COMBINED_PATH, FIGURE_PATH
from plotting import plot_climatology, monthly_series
from utils import to_monthly, to_climatology


def get_station_filelist():
    """Return list of station files"""
    station_files = {}
    for f in COMBINED_PATH.glob('*combined.csv'):
        station_name = ' '.join(f.stem.split('.')[0].split('_'))
        station_files[station_name] = f
    return station_files


def plot_station_monthly_time_series(verbose=False):
    """Plot monthly time series of Arctic stations"""
    for station, filepath in get_station_filelist().items():
        if verbose: print(f"Generating monthly plot for {station.title()}")
        df = read_combined_file(filepath)
        df_mon = to_monthly(df)

        fig = plt.figure(figsize=(15, 15))
        ax = monthly_series(df_mon, fig)
        fig.suptitle(station.title(), fontsize=20)
        fig.subplots_adjust(left=0.075, right=0.95, top=0.95, hspace=0.05)

        pngfile = FIGURE_PATH / f"{'_'.join(station.split())}.monthly.time_series.png"
        fig.savefig(pngfile)

    return


if __name__ == "__main__":
    plot_station_monthly_time_series(verbose=True)

