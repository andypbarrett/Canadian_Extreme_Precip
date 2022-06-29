"""Estimates quantiles for Total Precipitation""" 

import numpy as np
import pandas as pd

from canadian_extreme_precip.reader import read_combined_file
from canadian_extreme_precip.filepath import (combined_station_filepath,
                                              FIGURE_PATH,
                                              STATS_FILEPATH)


MIN_PRECIPITATION = 0.001  # Threshold precipitation for PDF

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
    'pond inlet',
    ]

QUANTILES = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.90, 0.95, 0.99, 1.]


def load_precip_data(station):
    df = read_combined_file(combined_station_filepath(station))
    return df['TOTAL_PRECIPITATION']


def get_quantiles(df, threshold=0., quantiles=QUANTILES):
    """Calculates quantiles"""
    df_t = df[df > threshold]
    return df_t.quantile(quantiles, interpolation='lower')


def get_precipitation_quantiles():

    stats = {}
    
    print(f"{' '*15}, {', '.join([f'{v*100.:>3.0f}%' for v in QUANTILES])}")
    for station in stations_list:
        df = load_precip_data(station)
        q = get_quantiles(df, threshold=0.01)
        stats[station] = q
        print(f"{station:15s}, {', '.join([f'{v:>4.1f}' for v in q])}")

        q = get_quantiles(df, threshold=1.)
        print(f"{'threshold=1.':>15s}, {', '.join([f'{v:>4.1f}' for v in q])}")
        q = get_quantiles(df['1960':'1995'], threshold=1.)
        print(f"{'1965-1960':>15s}, {', '.join([f'{v:>4.1f}' for v in q])}")

    stats_df = pd.DataFrame(stats).T
    stats_df.columns = [f"p{int(c*100):02d}" for c in stats_df.columns]
    stats_df.to_csv(STATS_FILEPATH)

if __name__ == "__main__":
    get_precipitation_quantiles()
