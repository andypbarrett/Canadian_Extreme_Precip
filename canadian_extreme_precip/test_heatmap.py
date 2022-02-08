import numpy as np
import matplotlib.pyplot as plt

from canadian_extreme_precip.plotting import station_heatmap
from canadian_extreme_precip.reader import read_combined_file
from canadian_extreme_precip.filepath import COMBINED_PATH

VARIABLES = [
    'MEAN_TEMPERATURE',
    'MIN_TEMPERATURE',
    'MAX_TEMPERATURE',
    'TOTAL_PRECIPITATION',
    'TOTAL_RAIN',
    'TOTAL_SNOW',
    'SNOW_ON_GROUND',
    ]


def main():
    filelist = list(COMBINED_PATH.glob('*.csv'))

    df = read_combined_file(filelist[0])
    df_obs = df[VARIABLES].apply(np.isfinite).resample('M').sum()
    df_obs = df_obs.divide(df_obs.index.daysinmonth, axis='rows')
    
    fig, ax = plt.subplots(figsize=(20,7))
    station_heatmap(df_obs.iloc[:36,:])

    plt.show()


if __name__ == "__main__":
    main()
