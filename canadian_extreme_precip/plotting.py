'''Plotting routines for Extreme Precip Paper'''
import datetime as dt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def station_heatmap(df, ax=None, cmap=None):
    '''Generates a heatmap showing daily observations in each month

    :df: pandas dataframe - expects a monthly timestep
    :ax: matplotlib axis instance

    :returns: an axis instance
    '''

    if not ax:
        ax = plt.gca()

    z = df.values.T
    z = np.where(z > 0., z, np.nan)
    
    x = mdates.date2num(df.index)
    y = df.columns
    #z = np.broadcast_to(np.arange(len(y)), (z.shape[1],z.shape[0])).T / len(y)
        
    # Get extent of heatmap array
    x0 = df.index[0]
    xlim = mdates.date2num([dt.datetime(x0.year, x0.month, 1), df.index[-1]])
    ylim = [len(y)-0.5, -0.5]

    img = ax.imshow(z, aspect='auto', cmap=cmap,
                    extent=[xlim[0], xlim[-1], ylim[0], ylim[1]])

    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(y)
    
    for yy in (np.arange(len(y)) - 0.5)[1:]:
        ax.axhline(yy, color='k')
    
    plt.colorbar(img, ax=ax)

    return ax
