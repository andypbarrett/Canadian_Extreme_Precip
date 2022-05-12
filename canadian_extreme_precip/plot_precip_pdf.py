"""Plots PDF for station precipitation.  Only plots nonzero precip"""

import numpy as np
import matplotlib.pyplot as plt

from reader import read_combined_file
from filepath import combined_station_filepath, FIGURE_PATH


MIN_PRECIPITATION = 1.  # Threshold precipitation for PDF

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


def load_precip_data(station):
    df = read_combined_file(combined_station_filepath(station))
    return df['TOTAL_PRECIPITATION']


def plot_pdf(df, title="", ax=None, bin_width=1.):
    if not ax:
        ax = plt.gca()

    df_t = df[df > MIN_PRECIPITATION]
    pmin = MIN_PRECIPITATION
    pmax = np.ceil(df_t.max()) + bin_width

    bins = np.arange(pmin, pmax, bin_width)

    q95, q99, qmax = df_t.quantile([0.95, 0.99, 1.], interpolation='nearest')

    df_t.hist(bins=bins, ax=ax, density=True, color='0.5')
    ax.axvline(q95, c='k', lw=2)
    ax.axvline(q99, c='b', lw=2)
    ax.axvline(qmax, c='r', lw=2)
    ax.set_title(title)
    ax.set_xlim(0., 100.)
    ax.text(0.6, 0.8, f"P95 = {q95:.1f}",
            color='k', transform=ax.transAxes)
    ax.text(0.6, 0.7, f"P99 = {q99:.1f}",
            color='b', transform=ax.transAxes)
    ax.text(0.6, 0.6, f"Pmax = {qmax:.1f}",
            color='r', transform=ax.transAxes)
    ax.text(0.6, 0.5, f"N = {df_t.size}", transform=ax.transAxes)
    
    return ax


def plot_precip_pdf(verbose=True):
    """Plots PDF for all stations"""

    fig = plt.figure(figsize=(10,10))

    axes = []
    for i, station in enumerate(stations_list, start=1):
        print(station)
        ax = fig.add_subplot(4, 3, i)
        df = load_precip_data(station)
        ax = plot_pdf(df, ax=ax, title=station.title())

    fig.tight_layout()
    fig.savefig(FIGURE_PATH / 'canadian_extreme_precip.precip_pdf.png')


if __name__ == "__main__":
    plot_precip_pdf()
