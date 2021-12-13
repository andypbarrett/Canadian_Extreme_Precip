'''Generates a JSON file that contains climate identifiers and start and end 
dates used to combine station records'''

from pathlib import Path
import re
import pprint

import pandas as pd

# Path to combined data file from Mark
DATAPATH = Path('/', 'home', 'apbarret', 'Data',
                'Rain_on_snow',
                'Canada_extreme_precip',
                'From_Mark')


def get_filelist():
    '''Returns dictionary keyed by station location containing filepaths'''
    p1 = re.compile('.*(?=_Combined)')
    p2 = re.compile('.*(?=\.+csv)')

    data = {}
    for fp in DATAPATH.glob('*.csv'):
        m1 = p1.search(fp.name)
        if m1:
            station_name = m1.group(0)
        else:
            m2 = p2.search(fp.name)
            if m2:
                station_name = m2.group(0)
            else:
                print(f'{fp.name} No match!')
                continue
        station_name = ' '.join(station_name.split('_'))
        if station_name.endswith('.'):
            station_name = station_name[:-1]
        if station_name.endswith(' A'):
            station_name = station_name[:-2]
        data[station_name] = fp
    return data


def load_data(filepath):
    '''Loads a combined file'''
    df = pd.read_csv(filepath, skiprows=2)
    df = df.dropna(how='all')
    return df


def get_station_metadata(df):
    '''Extracts station metadata from first and last records of each unique CLIMATE_IDENTIFIER'''
    grouper = df.groupby(df.CLIMATE_IDENTIFIER)

    first = grouper.first().loc[:,['x', 'y', 'STATION_NAME',
                                   'LOCAL_DATE', 'PROVINCE_CODE']]
    last = grouper.last().loc[:, 'LOCAL_DATE']
    
    metadata = first.join(last, rsuffix='_last')
    metadata = metadata.rename({
        'LOCAL_DATE': 'START_DATE',
        'LOCAL_DATE_last': 'END_DATE'
    },
                               axis=1)
    
    metadata.index = metadata.index.astype(int)
    metadata['START_DATE'] = pd.to_datetime(metadata['START_DATE'])
    metadata['END_DATE'] = pd.to_datetime(metadata['END_DATE'])
    return metadata


def make_station_merge_recipes():
    '''Generates JSON with station merge recipes'''
    filedict = get_filelist()

    combine_recipes = []
    for station_name, fp in filedict.items():
        df = load_data(fp)
        try:
            metadata = get_station_metadata(df)
        except Exception as error:
            print(error)
            continue

        station = []
        for row in metadata.iterrows():
            station.append(
                {
                    'climate_identifier': row[0],
                    'start_date': row[1].START_DATE.strftime('%Y-%m-%d'),
                    'end_date': row[1].END_DATE.strftime('%Y-%m-%d'),
                }
            )

        tmp = {'location': station_name.lower(), 'stations': station}
        combine_recipes.append(tmp)

    pprint.pprint(combine_recipes)

    return


if __name__ == "__main__":
    make_station_merge_recipes()
