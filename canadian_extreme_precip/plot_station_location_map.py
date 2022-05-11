"""Plots location of stations"""

import matplotlib.pyplot as plt

from plotting import location_map


def plot_station_location_map(figsize=(10, 7)):
    """Plots station location map"""
    fig = plt.figure(figsize=figsize)
    ax = location_map(fig)
    plt.show()


if __name__ == "__main__":
    plot_station_location_map()
