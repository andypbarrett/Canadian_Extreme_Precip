"""Plots temperature and precipitation climatologies for selected stations
for Canadian Extreme Precip paper"""

import matplotlib.pyplot as plt

from plotting import plot_number_of_monthly_obs
from reader import read_combined_file
from filepath import FIGURE_PATH, combined_station_filelist


def plot_station_climatologies():
    """Main function for plotting climatologies"""

    for station, filepath in combined_station_filelist().items():
        print(station)


if __name__ == "__main__":
    plot_station_climatologies()
