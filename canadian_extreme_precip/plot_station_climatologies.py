"""Plots temperature and precipitation climatologies for selected stations
for Canadian Extreme Precip paper"""

import matplotlib.pyplot as plt

from plotting import plot_climatology
from reader import read_climatology
from filepath import FIGURE_PATH, climatology_filepath


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


def plot_station_climatologies(verbose=False):
    """Main function for plotting climatologies"""

    fig, axes = plt.subplots(3, 3, figsize=(15, 20))

    for ax, station in zip(axes.flatten(), stations_list):
        if verbose: print(f"Reading data for {station.title()}")
        df = read_climatology(climatology_filepath(station))
        plot_climatology(df, ax=ax, title=station)

    fig.tight_layout()
    fig.savefig(FIGURE_PATH / 'station_climatologies_for_paper.png')


if __name__ == "__main__":
    verbose = True
    plot_station_climatologies(verbose=verbose)
