"""Plots charts of number monthly observations for each variable by station"""
import matplotlib.pyplot as plt

from plotting import plot_number_of_monthly_obs
from reader import read_combined_file
from filepath import FIGURE_PATH, combined_station_filelist


def observations_per_month(x):
    return x.count() / x.index[0].daysinmonth


def to_observations(df):
    return df.resample('M').apply({
        'MEAN_TEMPERATURE': observations_per_month,
        'MIN_TEMPERATURE': observations_per_month,
        'MAX_TEMPERATURE': observations_per_month,
        'TOTAL_PRECIPITATION': observations_per_month,
        'TOTAL_SNOW': observations_per_month,
        'TOTAL_RAIN': observations_per_month,
        'SNOW_ON_GROUND': observations_per_month,
        })


def main():

    for station, filepath in combined_station_filelist().items():
        df = read_combined_file(filepath)
        df_count = to_observations(df)
        fig = plot_number_of_monthly_obs(df_count)
        fig.suptitle(station.title(), fontsize=20)
        fig.tight_layout()

        pngfile = FIGURE_PATH / f"{'_'.join(station.split())}.observation_frequency.png"
        print(f"Saving figure to {pngfile}")
        fig.savefig(pngfile)


if __name__ == "__main__":
    main()
