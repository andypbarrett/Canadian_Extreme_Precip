'''Plotting routines for Extreme Precip Paper'''
import warnings
import datetime as dt
import calendar
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib as mpl


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

    #nrow = z.shape[0]
    #for idx in np.arange(nrow):
    #    z[idx,:] = (idx + 1) / nrow
    #print(z[:,0])
    
    x = mdates.date2num(df.index)
    y = df.columns
    #z = np.broadcast_to(np.arange(len(y)), (z.shape[1],z.shape[0])).T / len(y)
        
    # Get extent of heatmap array
    x0 = df.index[0]
    xlim = mdates.date2num([dt.datetime(x0.year, x0.month, 1), df.index[-1]])
    ylim = [len(y)-0.5, -0.5]

    img = ax.imshow(z, aspect='auto', cmap=cmap,
                    interpolation='none', 
                    extent=[xlim[0], xlim[-1], ylim[0], ylim[1]])

    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(y)
    
    for yy in (np.arange(len(y)) - 0.5)[1:]:
        ax.axhline(yy, color='0.7')
    
    return img


def new_ylim(ylim):
    """Returns new ylim"""
    yrng = ylim[1] - ylim[0]
    return ylim[0]-(0.1*yrng), ylim[1]


def plot_climatology(df, ax=None, title=None):
    """Creates a climatology panel"""
    
    if ax is None:
        ax = plt.gca()
    
    month_labels = [m[0] for m in calendar.month_name if m != '']
    
    # Create and plot temperature axes
    if 'MEAN_TEMPERATURE' in df:
        ax.plot(df.index, df.MEAN_TEMPERATURE, c='k', linestyle='-', lw=2)
    else:
        warnings.warn("MEAN_TEMPERATURE not in df, skipping...")
    if "MIN_TEMPERATURE" in df:
        ax.plot(df.index, df.MIN_TEMPERATURE, c='k', linestyle='--', lw=2)
    else:
        warnings.warn("MIN_TEMPERATURE not in df, skipping...")
    if "MAX_TEMPERATURE" in df:
        ax.plot(df.index, df.MAX_TEMPERATURE, c='k', linestyle='--', lw=2)
    else:
        warnings.warn("MAX_TEMPERATURE not in df, skipping...")
    
    ax.axhline(0., color='0.5')

    ax.set_xlim(0.5, 12.5)
    ax.set_xticks(np.arange(1,13));
    ax.set_xticklabels(month_labels)
    ax.set_ylabel('Temperature ($^{\circ}C$)', fontsize=20)
    ax.tick_params(labelsize=15)
    
    # Create and plot precipitation axes
    ax2 = ax.twinx()
    if "TOTAL_PRECIPITATION" in df:
        ax2.bar(df.index, df.TOTAL_PRECIPITATION, label='Rain')
    else:
        warnings.warn("TOTAL_PRECIPITATION not in df, skipping...")
    if "TOTAL_SNOW" in df:
        ax2.bar(df.index, df.TOTAL_SNOW, color='0.5', label='Snow')
    else:
        warnings.warn("TOTAL_SNOW not in df, skipping...")
    ax2.set_ylabel('Precipitation (mm)', fontsize=20)
    ax2.tick_params(labelsize=15)
    
    # Add space to show days of snow cover
    ax.set_ylim( new_ylim(ax.get_ylim()) )
    ax2.set_ylim( new_ylim(ax2.get_ylim()) )
    ax2.axhline(0., c='k')

    # Add snow on ground frequency as patches
    if "SNOW_ON_GROUND" in df:
        y = -10.  #ax2.get_xlim()[0]
        patches = []
        colors = []
        for index, value in df.SNOW_ON_GROUND.items():
            patches.append(Rectangle((index-0.5, y), 1., (-1.*y)))
            colors.append(value)
        cmap = mpl.cm.Greens_r
        collection = PatchCollection(patches, cmap=cmap, alpha=1.)
        collection.set_array(np.array(colors))
        ax2.add_collection(collection)
    else:
        warnings.warn("SNOW_ON_GROUND not in df, skipping...")
    
    # Make sure temperature curves plot in front of precip
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.set_frame_on(False)

    ax.set_title(title.title(), fontsize=20)

    ax2.legend(loc='upper left')
    
    # Add some space
    #fig.subplots_adjust(bottom=0.2)
    #ax_cb = fig.add_subplot()
    #cb1 = mpl.colorbar.ColorbarBase(ax_cb, cmap=cmap,
    #                                orientation='horizontal')
    #cb1.set_label('% month')
    
    return ax
