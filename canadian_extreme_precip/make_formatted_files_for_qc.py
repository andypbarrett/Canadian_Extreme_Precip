'''Creates fixed width files showing temperature and precipitation data'''

from pathlib import Path

from canadian_extreme_precip.reader import read_combined_file
from canadian_extreme_precip.write_files import write_formatted_data

DATAPATH = Path('/home/apbarret/Data/Rain_on_snow/Canada_extreme_precip/Combined_files')


def make_one_file(fpath):
    outfile = fpath.name.replace('.csv', '.for_qc.txt')
    df = read_combined_file(fpath)
    write_formatted_data(df, outfile)


for f in DATAPATH.glob('*.csv'):
    print(f'Processing {f.name}')
    make_one_file(f)
    
