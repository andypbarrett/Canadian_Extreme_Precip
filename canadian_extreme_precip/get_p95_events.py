"""Counts number of events above 95th percentile, e.g. to 5%"""

import pandas as pd

from canadian_extreme_precip.get_precipitation_quantiles import (load_precip_data,
                                                                 get_quantiles)

stations_list = [
    'clyde river',
    'cape dyer',
    'pond inlet',
    'resolute bay',
    'inuvik',
    'cambridge bay',
    'alert',
    'eureka',
    'hall beach',
    'sachs harbour',
    ]

year_start = '1960'
year_end = '1995'

def get_p95_events(station, threshold=0.):
    """Gets P95 event counts for a station"""
    df = load_precip_data(station)
    df = df[year_start: year_end]
    p95 = get_quantiles(df, threshold=threshold, quantiles=[0.95]).values[0]
    df95 = df[df > p95]
    return df95.groupby(df95.index.month).count()


def main():
    result = {}
    for station in stations_list:
        result[station] = get_p95_events(station, threshold=0.)
    df = pd.DataFrame(result)
    df = df.where(df.notna(), 0.)
    print(df.T)

    
if __name__ == "__main__":
    main()
