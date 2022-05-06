"""Test for plotting subaxes"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from plotting import plot_climatology, plot_cyclone_climatology
from reader import read_climatology
from filepath import climatology_filepath

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


def remove_labels(i, nrow=3):
    """Returns keyword to remove yaxis labels"""
    remove = {
        0: "right",
        1: "both",
        2: "left",
        }
    cindex = i % nrow
    return remove[cindex]


def keep_legend(i):
    """Helper function to return boolean for add_legend 
    keyword"""
    if i == 0:
        return True
    else:
        return False


def climatology_panel(gs, station, add_legend=True, axis_labels=None):
    """Generate a climatology panel"""
    fig = plt.gcf()
    subgs = gridspec.GridSpecFromSubplotSpec(4, 1, hspace=0., subplot_spec=gs)

    df = read_climatology(climatology_filepath(station))

    ax1 = fig.add_subplot(subgs[:-1, :])
    plot_climatology(df, ax=ax1, title=station, add_legend=add_legend,
                     axis_labels=axis_labels)
    ax1.set_xticklabels([])

    ax2 = fig.add_subplot(subgs[-1, :])
    plot_cyclone_climatology(df, ax=ax2)
    return subgs


def main():
    fig = plt.figure(figsize=(15, 20))

    nrow = 3
    ncol = 3
    gs0 = gridspec.GridSpec(nrow, ncol, figure=fig)

    gs_sub = []
    for i, (gs, station) in enumerate(zip(gs0, stations_list)):
        gs_sub.append(climatology_panel(gs, station,
                                        add_legend=keep_legend(i),
                                        axis_labels=remove_labels(i)))
    plt.tight_layout()

    fig.savefig('test_figure.png')


if __name__ == "__main__":
    main()
