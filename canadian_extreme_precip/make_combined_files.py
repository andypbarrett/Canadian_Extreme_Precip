'''Combines station files to generate long climate records following recipes in 
dataset_preparation/station_merge_recipe.json'''

from pathlib import Path
import json
import datetime as dt
import re
import warnings

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from canadian_extreme_precip.reader import read_station_file
from canadian_extreme_precip.filepath import raw_station_filepath, COMBINED_PATH

MERGE_RECIPE_JSON = Path('/', 'home', 'apbarret', 'src', 'Canadian_extreme_precip', 'dataset_preparation', 'station_merge_recipe.json')
BAD_RECORD_LIST_PATH = Path('/', 'home', 'apbarret', 'src', 'Canadian_extreme_precip', 'data', 'bad_records.csv')

XBEGIN = dt.datetime(1920,1,1)
XEND = dt.datetime(2021,12,31)

VARIABLE_LIST = [
    'MEAN_TEMPERATURE',
    'MIN_TEMPERATURE',
    'MAX_TEMPERATURE',
    'TOTAL_PRECIPITATION',
    'TOTAL_RAIN',
    'TOTAL_SNOW',
    'SNOW_ON_GROUND',
    ]


def plot_temperature_panel(df, variable, ax=None, hide_xaxis=False,
                           add_legend=True):
    '''Plot a temperature panel'''
    df[variable].plot(ax=ax)
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(-55, 30)
    ax.axhline(0., color='0.6', zorder=0)
    ax.text(0.01, 0.85, ' '.join(variable.split('_')),
            transform=ax.transAxes)

    # Plot flags
    temp_labels = {
        'M': 'Missing',
        'Y': 'Missing but < 0',
        'N': 'Missing byt > 0',
        }
    temp_flags = ['M', 'Y', 'N']
    flag_colors = ['k', 'r', 'y']
    for color, flag in zip(flag_colors, temp_flags):
        x = df[df[variable+'_FLAG'] == flag].index
        y = [-52]*len(x)
        if len(x) > 0:
            ax.scatter(x, y, marker='+', c=color, label=temp_labels[flag])

    if add_legend:
        thandles, tlabels = ax.get_legend_handles_labels()  # needed to drop line label
        ax.legend(thandles[1:], tlabels[1:],
                 loc='lower left', fontsize=8)

    if hide_xaxis:
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_xlabel('')
        
    
def plot_snowdepth_panel(df, variable, ax=None, hide_xaxis=False,
                         add_legend=True):
    '''Plot a snow depth panel'''
    ymax = np.ceil(df[variable].max() * .1) * 10.
    ymin = -.15 * ymax
    df[variable].plot(ax=ax)
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(ymin, ymax)
    ax.axhline(0., color='0.6', zorder=0)
    ax.text(0.01, 0.85, ' '.join(variable.split('_')),
            transform=ax.transAxes)

    # Plot flags
    snow_labels = {
        'M': 'Missing',
        'Y': 'Missing but < 0',
        'N': 'Missing byt > 0',
        }
    snow_flags = ['M', 'Y', 'N']
    flag_colors = ['k', 'r', 'y']
    for color, flag in zip(flag_colors, snow_flags):
        x = df[df[variable+'_FLAG'] == flag].index
        y = [ymin*0.5]*len(x)
        if len(x) > 0:
            ax.scatter(x, y, marker='+', c=color, label=snow_labels[flag])

    if add_legend:
        thandles, tlabels = ax.get_legend_handles_labels()  # needed to drop line label
        ax.legend(thandles[1:], tlabels[1:],
                  loc='lower left', fontsize=8)
    
    if hide_xaxis:
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_xlabel('')
        
    
def plot_precipitation_panel(df, variable, ax=None, hide_xaxis=False,
                             add_legend=True):
    '''Plot a precipitation panel'''
    ymax = np.ceil(df[variable].max() * .1) * 10.
    ymin = -.15 * ymax
    ax.fill_between(df.index, df[variable], step='pre', color='k')
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(ymin, ymax)
    ax.axhline(0., color='0.6', zorder=0)
    ax.text(0.01, 0.85, ' '.join(variable.split('_')),
            transform=ax.transAxes)

    # Plot flags
    precip_labels = {
        'T': 'Trace',
        'M': 'Missing',
        'L': 'Occurrence uncertain',
        'C': 'Amount uncertain',
        }
    precip_flags = ['T', 'M', 'L', 'C']
    flag_colors = ['b', 'k', 'y', 'g']
    for color, flag in zip(flag_colors, precip_flags):
        x = df[df[variable+'_FLAG'] == flag].index
        y = [ymin*.5]*len(x)
        if len(x) > 0:
            ax.scatter(x, y, marker='+', c=color, label=precip_labels[flag])

    if add_legend:
        ax.legend(loc='lower left', fontsize=8)
    
    if hide_xaxis:
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_xlabel('')


def plot_variable_time_series(df, station):
    '''Generates a plot of main variables for checking'''

    fig, ax = plt.subplots(7, 1, figsize=(15, 20))

    plot_temperature_panel(df, 'MEAN_TEMPERATURE', 
                           ax=ax[0], hide_xaxis=True)
    plot_temperature_panel(df, 'MIN_TEMPERATURE', 
                           ax=ax[1], hide_xaxis=True)
    plot_temperature_panel(df, 'MAX_TEMPERATURE',
                           ax=ax[2], hide_xaxis=True)
    
    plot_precipitation_panel(df, 'TOTAL_PRECIPITATION', 
                             ax=ax[3], hide_xaxis=True)
    plot_precipitation_panel(df, 'TOTAL_RAIN', 
                             ax=ax[4], hide_xaxis=True)
    plot_precipitation_panel(df, 'TOTAL_SNOW', 
                             ax=ax[5], hide_xaxis=True)

    plot_snowdepth_panel(df, 'SNOW_ON_GROUND',
                         ax=ax[6])
    
    fig.subplots_adjust(hspace=0.05)

    fig.suptitle(station, x=0.5, y=0.9)
    
    return fig, ax


def get_recipe():
    '''Loads merge recipe json'''
    with open(MERGE_RECIPE_JSON) as json_file:
        recipes = json.load(json_file)
    return recipes


def combine_files(recipe, reindex_dataframe=True):
    '''Combines station files'''
    df_list = []
    for station in recipe['stations']:
        filepath = raw_station_filepath(station['climate_identifier'])
        df_list.append(read_station_file(filepath)[station['start_date']:station['end_date']])
    df = pd.concat(df_list)
    df = df.sort_index()
    
    # Check if number of records in df match days in timespan
    ndays = (df.index[-1] - df.index[0]).days
    nrecord = len(df.index)
    if nrecord != ndays:
        print(f'Record timespan in days does not match number of indices\n' + \
              f'{nrecord} records found, {ndays} expected!')
        if reindex_dataframe:
            print('Reindexing dataframe to generate temporaly complete series')
            expected_index = pd.date_range(df.index[0], df.index[-1], freq='D')
            df = df.reindex(expected_index)
            
    return df


def print_record_timerange(df):
    '''Prints earliest and latest record for a dataframe to stdout'''
    print(f'   Earliest: {df.index.min()}  Start: {df.iloc[0].name}')
    print(f'   Latest: {df.index.max()}    End: {df.iloc[-1].name}')
    return

    
def print_variable_flags(df):
    '''Prints a unique list of variable flags to stdout'''
    for var in VARIABLE_LIST:
        var_flag = var + '_FLAG'
        flags = [str(x) for x in df[var_flag].unique()]
        print(f'   {var_flag}: {",".join(flags)}')
    return


def make_png_filename(location):
    loc_name = '_'.join(re.split('-|\s', location))
    return COMBINED_PATH / f'{loc_name}.variable.time_series.png'
    

def make_csv_filename(location):
    loc_name = '_'.join(re.split('-|\s', location))
    return COMBINED_PATH / f'{loc_name}.combined.csv'


def get_bad_records_list():
    return pd.read_csv(BAD_RECORD_LIST_PATH, header=0, parse_dates=True)


def fix_bad_records(df, bad_df, location):
    for _, values in bad_df[bad_df.station == location].iterrows():
        df.loc[values.date, values.variable] = np.nan


def make_combined_files(save_merged_file=True, plot_dir='.',
                        verbose=False, make_plot=False, save_plot=False,
                        reindex_dataframe=True):
    '''Merges station files according to recipes

    :save_merged_file: Save combined file (default True).  Set to False
                       if you just want to check plots before creating 
                       merged file
    :outdir: output directory for data files
    :plot_dir: output directory for plots (default cwd)
    :make_plot: creates plot of temperature and precipitation variables (default False)
    :save_plot: save plot of key variables (default False).  If False image is displayed
                window.
    :reindex_dataframe: reindex dataframe to contain full record - set to False for debugging
    :verbose: write progress messages to stdout
    '''
    recipes = get_recipe()

    bad_records = get_bad_records_list()

    for recipe in recipes:
        if verbose: print(f'Combining files for {recipe["location"]}')
        combined_df = combine_files(recipe,
                                    reindex_dataframe=reindex_dataframe)

        fix_bad_records(combined_df, bad_records, recipe["location"])
        
        if save_merged_file:
            csv_outfile = make_csv_filename(recipe['location'])
            if verbose: print(f'Writing combined file to {csv_outfile}')
            combined_df.to_csv(csv_outfile, sep=',')

        if make_plot:
            fig, ax = plot_variable_time_series(combined_df,
                                                recipe['location'].upper())

        if make_plot & save_plot:
            outfile = make_png_filename(recipe["location"], outdir=plot_dir)
            if verbose: print(f'Saving figure to {outfile}')
            fig.savefig(outfile)
        else:
            plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Combines individual station files for Arctic stations')
    parser.add_argument('--save_merged_file', action='store_false',
                        help='Save combined file (default True)')
    parser.add_argument('--plot_dir', type=str, default='.',
                        help='Directory path to save plot')
    parser.add_argument('--make_plot', action='store_true',
                        help='Generate time series plot')
    parser.add_argument('--save_plot', action='store_true',
                        help='Save plot as png')
    parser.add_argument('--reindex_dataframe', action='store_false',
                        help='do not reindex dataframe')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()
    
    make_combined_files(save_merged_file=args.save_merged_file,
                        plot_dir=args.plot_dir,
                        make_plot=args.make_plot,
                        save_plot=args.save_plot,
                        reindex_dataframe=args.reindex_dataframe,
                        verbose=args.verbose)
