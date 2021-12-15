'''Combines station files to generate long climate records following recipes in 
dataset_preparation/station_merge_recipe.json'''

from pathlib import Path
import json

import pandas as pd

from reader import read_station_file
from filepath import raw_station_filepath

MERGE_RECIPE_JSON = Path('/', 'home', 'apbarret', 'src', 'Canadian_extreme_precip', 'dataset_preparation', 'station_merge_recipe.json')


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
    return pd.concat(df_list)


def make_combined_files():
    '''Merges station files'''
    recipes = get_recipe()

    for recipe in recipes:
        print(recipe['location'])
        combined_df = combine_files(recipe)


if __name__ == "__main__":
    make_combined_files()
