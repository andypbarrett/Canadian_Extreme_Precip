'''Combines station files to generate long climate records following recipes in 
dataset_preparation/station_merge_recipe.json'''

from pathlib import Path
import json
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd

from canadian_extreme_precip.reader import read_station_file
from canadian_extreme_precip.filepath import raw_station_filepath

MERGE_RECIPE_JSON = Path('/', 'home', 'apbarret', 'src', 'Canadian_extreme_precip', 'dataset_preparation', 'station_merge_recipe.json')

XBEGIN = dt.datetime(1929,1,1)
XEND = dt.datetime(2021,12,31)


def plot_temperature_panel(ts, variable, ax=None):
    '''Plot a temperature panel'''
    ts.plot(ax=ax)
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(-50,30)
    ax.axhline(0.)
    ax.text(0.01, 0.85, variable, transform=ax.transAxes)

    
def plot_precipitation_panel(ts, variable, ax=None):
    '''Plot a precipitation panel'''
    ts.plot(ax=ax)
    ax.set_xlim(XBEGIN, XEND)
    ax.set_ylim(0,40)
    ax.axhline(0.)
    ax.text(0.01, 0.85, variable, transform=ax.transAxes)

    
def plot_variable_time_series(df):
    '''Generates a plot of main variables for checking'''

    variable_list = ['MEAN_TEMPERATURE', 'MIN_TEMPERATURE', 'MAX_TEMPERATURE',
                     'TOTAL_PRECIPITATION', 'TOTAL_RAIN', 'TOTAL_SNOW']

    fig, ax = plt.subplots(6, 1, figsize=(15, 20))

    plot_temperature_panel(df['MEAN_TEMPERATURE'], 'MEAN TEMPERATURE', ax=ax[0])
    plot_temperature_panel(df['MIN_TEMPERATURE'], 'MIN TEMPERATURE', ax=ax[1])
    plot_temperature_panel(df['MAX_TEMPERATURE'], 'MAX TEMPERATURE', ax=ax[2])
    
    plot_precipitation_panel(df['TOTAL_PRECIPITATION'], 'TOTAL PRECIPITATION', ax=ax[3])
    plot_precipitation_panel(df['TOTAL_RAIN'], 'TOTAL RAIN', ax=ax[4])
    plot_precipitation_panel(df['TOTAL_SNOW'], 'TOTAL_SNOW', ax=ax[5])
    
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


def make_combined_files():
    '''Merges station files'''
    recipes = get_recipe()

    for recipe in recipes:
        print(recipe['location'])
        combined_df = combine_files(recipe)
        print(f'   Earliest: {combined_df.index.min()}  Start: {combined_df.iloc[0].name}')
        print(f'   Latest: {combined_df.index.max()}    End: {combined_df.iloc[-1].name}')
        print('')
        fig, ax = plot_variable_time_series(combined_df)
        plt.show()
        break


if __name__ == "__main__":
    make_combined_files()
