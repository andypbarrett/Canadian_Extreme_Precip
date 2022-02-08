'''Plotting routines for Extreme Precip Paper'''
import datetime as dt

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
    x = mdates.date2num(df.index)
    y = df.columns
    
    # Get extent of heatmap array
    x0 = df.index[0]
    xlim = mdates.date2num([dt.datetime(x0.year, x0.month, 1), df.index[-1]])
    ylim = [-0.5, len(y)-0.5]

    img = ax.imshow(z, aspect='auto', cmap=cmap,
                    extent=[xlim[0], xlim[-1], ylim[0], ylim[1]])

    # Set xaxis to be datetime
    xticks = mdates.date2num(df.index[df.index.month == 12].shift(1,'D'))
    ax.xaxis_date()
    ax.set_xticks(xticks)
    date_format = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_formatter(date_format)
    
    #ax.set_yticklabels(y)
    
    plt.colorbar(img, ax=ax)

    return ax
