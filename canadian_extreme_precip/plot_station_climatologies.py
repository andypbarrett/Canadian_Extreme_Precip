"""Plots temperature and precipitation climatologies for selected stations
for Canadian Extreme Precip paper"""

import matplotlib.pyplot as plt

from plotting import plot_climatology
from reader import read_combined_file
from filepath import FIGURE_PATH, combined_station_filepath
from utils import to_monthly, to_climatology


# Excludes Pond Inlet
stations_list = [
    'cape dyer',
    'resolute bay',
    'eureka',
    'alert',
    'clyde river',
    'cambridge bay',
    'hall beach',
    'sachs harbour',
    'inuvik',
    ]


def load_climatology(station):
    """Loads station data and calculates climatology
    and loads cyclone frequency"""
    df = read_combined_file(combined_station_filepath(station))
    df_mon = to_monthly(df)
    df_clm = to_climatology(df_mon.loc['1960':'1995', :])
    return df_clm

    
def plot_station_climatologies(verbose=False):
    """Main function for plotting climatologies"""

    fig, axes = plt.subplots(3, 3, figsize=(15, 20))

    for ax, station in zip(axes.flatten(), stations_list):
        if verbose: print(f"Reading data for {station.title()}")
        df = load_climatology(station)
        plot_climatology(df, ax=ax, title=station)

    fig.tight_layout()
    fig.savefig(FIGURE_PATH / 'station_climatologies_for_paper.png')


if __name__ == "__main__":
    verbose=True
    plot_station_climatologies(verbose=verbose)
