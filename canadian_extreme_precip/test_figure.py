"""Test for plotting subaxes"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def dummy_plot1(ax):
    x = np.arange(1, 13)
    y = np.sin((x-1) * np.pi / 11) + np.random.randn(12)
    ax.plot(x, y)
    ax.axhline(0.)
    ax.set_ylabel('Temperature', fontsize=15)
    return ax
    
    
def dummy_plot2(ax):
    x = np.arange(1, 13)
    y = np.sin((x-1) * np.pi / 11) + np.random.randn(12)
    ax.fill_between(x, y, step='mid')
    ax.axhline(0.)
    ax.set_ylabel('Cyclones', fontsize=15)
    return ax
    
    
def climatology_panel(gs):
    """Generate a climatology panel"""
    fig = plt.gcf()
    subgs = gridspec.GridSpecFromSubplotSpec(4, 1, hspace=0., subplot_spec=gs)
    ax1 = fig.add_subplot(subgs[:-1, :])
    dummy_plot1(ax1)
    ax2 = fig.add_subplot(subgs[-1, :])
    dummy_plot2(ax2)
    return subgs


def main():
    fig = plt.figure(figsize=(15, 20))

    gs0 = gridspec.GridSpec(3, 3, figure=fig)

    gs_sub = []
    for gs in gs0:
        gs_sub.append(climatology_panel(gs))
    plt.tight_layout()
    
    plt.show()
    

if __name__ == "__main__":
    main()
