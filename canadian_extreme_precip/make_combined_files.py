'''Combines station files to generate long climate records following recipes in 
dataset_preparation/station_merge_recipe.json'''

from pathlib import Path
import json
import datetime as dt
import re

import matplotlib.pyplot as plt
import pandas as pd

from canadian_extreme_precip.reader import read_station_file
from canadian_extreme_precip.filepath import raw_station_filepath

MERGE_RECIPE_JSON = Path('/', 'home', 'apbarret', 'src', 'Canadian_extreme_precip', 'dataset_preparation', 'station_merge_recipe.json')

XBEGIN = dt.datetime(1929,1,1)
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


def plot_temperature_panel(df, variable, ax=None, hide_xaxis=False):
    '''Plot a temperature panel'''
    df[variable].plot(ax=ax)
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(-55,30)
    ax.axhline(0., color='0.6', zorder=0)
    ax.text(0.01, 0.85, ' '.join(variable.split('_')),
            transform=ax.transAxes)

    # Plot flags
    temp_flags = ['M', 'Y', 'N']
    flag_colors = ['k', 'r', 'y']
    for color, flag in zip(flag_colors, temp_flags):
        x = df[df[variable+'_FLAG'] == flag].index
        y = [-52]*len(x)
        ax.scatter(x, y, marker='.', c=color, label=flag)

    #ax.legend()
    
    if hide_xaxis:
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_xlabel('')
        
    
def plot_snowdepth_panel(df, variable, ax=None, hide_xaxis=False):
    '''Plot a snow depth panel'''
    df[variable].plot(ax=ax)
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(-10,100.)
    ax.axhline(0., color='0.6', zorder=0)
    ax.text(0.01, 0.85, ' '.join(variable.split('_')),
            transform=ax.transAxes)

    # Plot flags
    temp_flags = ['M', 'Y', 'N']
    flag_colors = ['k', 'r', 'y']
    for color, flag in zip(flag_colors, temp_flags):
        x = df[df[variable+'_FLAG'] == flag].index
        y = [-5]*len(x)
        ax.scatter(x, y, marker='.', c=color, label=flag)

    #ax.legend()
    
    if hide_xaxis:
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_xlabel('')
        
    
def plot_precipitation_panel(df, variable, ax=None, hide_xaxis=False):
    '''Plot a precipitation panel'''
    ax.fill_between(df.index, df[variable], step='pre', color='k')
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(-10,50)
    ax.text(0.01, 0.85, ' '.join(variable.split('_')),
            transform=ax.transAxes)

    # Plot flags
    precip_flags = ['T', 'M', 'L', 'C']
    flag_colors = ['b', 'k', 'y', 'g']
    for color, flag in zip(flag_colors, precip_flags):
        x = df[df[variable+'_FLAG'] == flag].index
        y = [-5]*len(x)
        ax.scatter(x, y, marker='+', c=color, label=flag)
    
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


def combine_files(recipe):
    '''Combines station files'''
    df_list = []
    for station in recipe['stations']:
        filepath = raw_station_filepath(station['climate_identifier'])
        df_list.append(read_station_file(filepath)[station['start_date']:station['end_date']])
    df = pd.concat(df_list)
    df = df.sort_index()
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


def make_png_filename(location, outdir='.'):
    this_path = Path(outdir)
    loc_name = '_'.join(re.split('-|\s', location))
    return this_path / f'{loc_name}.variable.time_series.png'
    

def make_combined_files(save_merged_file=True, outdir=None, plot_dir='.',
                        verbose=False, make_plot=False, save_plot=False):
    '''Merges station files according to recipes

    :save_merged_file: Save combined file (default True).  Set to False
                       if you just want to check plots before creating merged file
    :outdir: output directory for data files
    :plot_dir: output directory for plots (default cwd)
    :make_plot: creates plot of temperature and precipitation variables (default False)
    :save_plot: save plot of key variables (default False).  If False image is displayed
                window.
    :verbose: write progress messages to stdout
    '''
    recipes = get_recipe()

    for recipe in recipes:
        if verbose: print(f'Combining files for {recipe["location"]}')
        combined_df = combine_files(recipe)
        #print_record_timerange(combined_df)
        #print_variable_flags(combined_df)
        #print('')

        if make_plot:
            fig, ax = plot_variable_time_series(combined_df, recipe['location'].upper())

        if save_plot:
            outfile = make_png_filename(recipe["location"], outdir=plot_dir)
            if verbose: print(f'Saving figure to {outfile}')
            fig.savefig(outfile)
        else:
            plt.show()

        #break


if __name__ == "__main__":
    make_combined_files(verbose=True, make_plot=True)
