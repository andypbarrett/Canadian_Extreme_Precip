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


def plot_variable_time_series(df, variable_list=None):
    '''Generates a plot of main variables for checking'''

    if not variable_list:
        variable_list = ['MEAN_TEMPERATURE', 'MIN_TEMPERATURE', 'MAX_TEMPERATURE',
                     'TOTAL_PRECIPITATION', 'TOTAL_RAIN', 'TOTAL_SNOW']

    xbegin = dt.datetime(1929,1,1)
    xend = dt.datetime(2021,12,31)
    
    fig, ax = plt.subplots(6, 1, figsize=(15, 20))
    for axes, var in zip(ax, variable_list):
        df[var].plot(ax=axes)
        axes.set_xlim(xbegin, xend)
        axes.text(0.01, 0.85, var, transform=axes.transAxes)

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
