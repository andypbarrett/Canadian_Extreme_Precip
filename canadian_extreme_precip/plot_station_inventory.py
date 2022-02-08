'''Makes a plot of station inventory showing number of observations per month
for key variables'''

from pathlib import Path

import pandas as pd

DATAPATH = Path('/home/apbarret/Data/Rain_on_snow/Canada_extreme_precip/Combined_files')
def check_missing_dates(f):
    df = pd.read_csv(f, header=0, index_col=0, parse_dates=True)
    expected_index = pd.date_range(df.index[0], df.index[-1], freq='D')
    nrecords = len(df.index)
    nexpected = len(expected_index)
    location = f.name.split('.')[0]

    print(location.upper())
    print(f'{nrecords} records found, {nexpected} expected')
    for search_date in expected_index.difference(df.index).strftime('%Y-%m').unique():
        print(f'{search_date}  {len(df[search_date])}')
    print('-'*20)


for f in DATAPATH.glob('*.csv'):
    check_missing_dates(f)
