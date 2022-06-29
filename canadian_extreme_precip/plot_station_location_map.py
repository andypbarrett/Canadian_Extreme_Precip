"""Plots location of stations"""
from pathlib import Path

import matplotlib.pyplot as plt

from plotting import location_map

FIGURE_PATH = Path.home() / 'src' / 'Canadian_extreme_precip' / 'figures'


def plot_station_location_map(figsize=(10, 7)):
    """Plots station location map"""
    fig = plt.figure(figsize=figsize)
    ax = location_map(fig)
    fig.savefig(FIGURE_PATH / 'station_location_map.png')


if __name__ == "__main__":
    plot_station_location_map()
