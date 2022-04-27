"""Test for plotting subaxes"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def climatology_panel(gs):
    """Generate a climatology panel"""
    subgs = gs.subgridspec(4, 1, hspace=0.)
    ax1 = fig.add_subplot(subgs[:-1, :])
    ax2 = fig.add_subplot(subgs[-1, :])
    return subgs


def main():
    fig = plt.figure(figsize=(15, 20))

    gs0 = gridspec.GridSpec(1, 2, figure=fig)

    gs00 = gs0[0].subgridspec(4, 1, hspace=0.)
    ax1 = fig.add_subplot(gs00[:-1, :])
    ax2 = fig.add_subplot(gs00[-1, :])

    gs01 = gs0[1].subgridspec(4, 1, hspace=0.)
    ax3 = fig.add_subplot(gs01[:-1, :])
    ax4 = fig.add_subplot(gs01[-1, :])

    plt.show()
    

if __name__ == "__main__":
    main()
