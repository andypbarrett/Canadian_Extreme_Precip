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

    ax2.legend(loc='upper left', fontsize=15)
    
    # Add some space
    #fig.subplots_adjust(bottom=0.2)
    #ax_cb = fig.add_subplot()
    #cb1 = mpl.colorbar.ColorbarBase(ax_cb, cmap=cmap,
    #                                orientation='horizontal')
    #cb1.set_label('% month')
    
    return ax


def monthly_series(df, fig):
    
    time_begin = dt.datetime(df.index[0].year, 1, 1)
    time_end = dt.datetime(df.index[-1].year, 12, 31)

    ax1 = fig.add_subplot(311)
    ax1.plot(df.index, df['MEAN_TEMPERATURE'], color='k')
    ax1.fill_between(df.index, df['MIN_TEMPERATURE'].values, df['MAX_TEMPERATURE'].values,
                       color='0.6')
    ax1.set_xlim(time_begin, time_end)
    ax1.axhline(0., c='0.7', zorder=0)
    ticks = ax1.get_xticks()
    ax1.set_xticks([])
    ax1.set_ylabel("Temperature ($^{\circ}C$)", fontsize=20)
    
    ax2 = fig.add_subplot(312, sharex=ax1)
    ax2.fill_between(df.index, df["TOTAL_PRECIPITATION"], step='mid')
    ax2.fill_between(df.index, df["TOTAL_SNOW"], step='mid', color='0.4')
    ax2.set_xlim(time_begin, time_end)
    ax2.set_ylim(0., ax2.get_ylim()[1])
    ax2.set_ylabel("Precipitation (mm)", fontsize=20)

    ax3 = fig.add_subplot(313, sharex=ax1)
    ax3.fill_between(df.index, df["SNOW_ON_GROUND"], step='mid', color='k')
    ax3.set_xlim(time_begin, time_end)
    ax3.set_ylim(0., 1.)
    ax3.set_ylabel("Snow on Ground", fontsize=20)

    plt.setp([ax1.get_xticklabels(), ax2.get_xticklabels()], visible=False)

    return [ax1, ax2, ax3]
