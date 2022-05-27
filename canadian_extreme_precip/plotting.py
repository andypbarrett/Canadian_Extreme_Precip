'''Plotting routines for Extreme Precip Paper'''
import warnings
import datetime as dt
import calendar
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib as mpl
from matplotlib import ticker

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from filepath import STATION_FILEPATH, STATS_FILEPATH


def load_stations_and_stats():
    """Loads station locations and precipitation statistics
       for location map
    """
    station_df = pd.read_csv(STATION_FILEPATH, index_col=0, header=0)
    stats_df = pd.read_csv(STATS_FILEPATH, index_col=0, header=0)
    station_df = station_df.join(stats_df)
    station_df = station_df.drop('pond inlet')  # Not included in paper
    return station_df


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


def plot_climatology(df, ax=None, title=None, add_legend=True,
                     axis_labels=None, temperature_limit=(-45., 20.),
                     precipitation_limit=(0., 100.)):
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
    ax.set_ylim(temperature_limit)
    ax.set_yticks([-40., -30., -20., -10., 0., 10., 20.])  # Hard coded

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
    ax2.set_ylim(precipitation_limit)

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

    if add_legend:
        ax2.legend(loc='upper left', fontsize=15)

    if axis_labels == "both":
        ax.set_ylabel('')
        ax2.set_ylabel('')
    elif axis_labels == "left":
        ax.set_ylabel('')
    elif axis_labels == "right":
        ax2.set_ylabel('')

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


def plot_number_of_monthly_obs(df):
    """Plots the fraction of observations per month"""

    tbeg = dt.datetime(1920, 1, 1)
    tend = dt.datetime(2022, 12, 31)
    
    nvar = len(df.columns)
    
    fig, axes = plt.subplots(nvar, 1, figsize=(15, 10))

    for ax, (name, values) in zip(axes.flatten(), df.items()):
        ax.fill_between(df.index, df[name], step='mid')
        ax.text(0.01, 0.85, name, transform=ax.transAxes)
        ax.set_ylim(0., 1.)
        ax.set_xlim(tbeg, tend)
    return fig


def plot_cyclone_climatology(df, ax=None, title=None, axis_labels=None,
                             ylimit=(0, 8)):
    """Plots climatology of cyclone tracks"""
    if not ax:
        ax = plt.gca()

    month_labels = [m[0] for m in calendar.month_name if m != '']

    if "CYCLONE_TRACKS" in df:
        ax.bar(df.index, df.CYCLONE_TRACKS, color='0.5')

    ax.set_xlim(0.5, 12.5)
    ax.set_xticks(np.arange(1,13))
    ax.set_xticklabels(month_labels)
    ax.tick_params(labelsize=15)
    ax.set_ylim(ylimit)
    ax.set_yticks([0, 2, 4, 6, 8])
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))

    if axis_labels == "right":
        ax.set_ylabel('Cyclones', fontsize=20)

    return ax


def location_map(fig=None):
    """Plots locations of stations"""
    map_extent = [
        -2045000., 2000000.,
        -3000000., -300000.,
    ]
    proj = ccrs.Stereographic(central_latitude=90.,
                              central_longitude=270.,
                              true_scale_latitude=70.)

    stations = load_stations_and_stats()

    if not fig:
        fig = plt.gcf()

    ax = fig.add_subplot(projection=proj)
    ax.set_extent(map_extent, proj)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND)

    ax.text(-37.5, 74., 'Greenland',
            va='center', ha='center',
            fontsize=20, color='0.4',
            transform=ccrs.PlateCarree())
    ax.text(-112.9, 63.8, 'Canada',
            va='center', ha='center',
            fontsize=20, color='0.4',
            transform=ccrs.PlateCarree())
    
    gl = ax.gridlines(color='0.6', zorder=1, draw_labels=True)
    gl.top_labels = False

    for station, data in stations.iterrows():
        x, y = proj.transform_point(data['lon'], data['lat'],
                                    ccrs.PlateCarree())
        ax.scatter(x, y, 50, c='k',
                   transform=proj, zorder=3)
        ax.text(x+40000, y-10000, station.title(),
                transform=proj,
                va='top',
                ha='left',
                fontsize=12)
        ax.text(x+4000, y+10000, data['p100'].round(1),
                transform=proj,
                va='bottom',
                ha='left',
                fontsize=13)
        ax.text(x-40000, y+10000, data['p99'].round(1),
                transform=proj,
                va='bottom',
                ha='right',
                fontsize=13)
        ax.text(x-40000, y-10000, data['p95'].round(1),
                transform=proj,
                va='top',
                ha='right',
                fontsize=13)

    # Legend
    x, y = 0.1, 0.9
    dx, dy = 0.01, 0.005
    ax.scatter(x, y, 50, c='k',
               transform=ax.transAxes, zorder=3)
    ax.text(x+dx, y-dy, 'Station Name',
            transform=ax.transAxes,
            va='top',
            ha='left',
            fontsize=12)
    ax.text(x+dx, y+dy, '$P_{max}$',
            transform=ax.transAxes,
            va='bottom',
            ha='left',
            fontsize=13)
    ax.text(x-dx, y+dy, '$P_{99th}$',
            transform=ax.transAxes,
            va='bottom',
            ha='right',
            fontsize=13)
    ax.text(x-dx, y-dy, '$P_{95th}$',
            transform=ax.transAxes,
            va='top',
            ha='right',
            fontsize=13)
    
    return ax
