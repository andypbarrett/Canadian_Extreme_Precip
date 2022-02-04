'''Module for writing station data to stdout of file'''

these_columns = [
    'MEAN_TEMPERATURE',
    'MEAN_TEMPERATURE_FLAG',
    'MIN_TEMPERATURE',
    'MIN_TEMPERATURE_FLAG',
    'MAX_TEMPERATURE',
    'MAX_TEMPERATURE_FLAG',
    'TOTAL_PRECIPITATION',
    'TOTAL_PRECIPITATION_FLAG',
    'TOTAL_RAIN',
    'TOTAL_RAIN_FLAG',
    'TOTAL_SNOW',
    'TOTAL_SNOW_FLAG',
    'SNOW_ON_GROUND',
    'SNOW_ON_GROUND_FLAG',
    ]


HEADER = [
    'TMEAN', 'TMIN', 'TMAX', 'TOTALP', 'RAIN', 'SNOW', 'DSNOW'
    ]

def record_fmt(rec):
    '''Generates a formated string for a data record

    Assumes only temperature and precip data

    :r: record/row from iterrows

    :returns: str'''
    index = rec[0]
    data = rec[1]
    sfmt = [index.strftime('%Y-%m-%d')]
    varnames = [v for v in data.index if '_FLAG' not in v]
    for v in varnames:
        sfmt.append(var_fmt(data, v))
    return ' '.join(sfmt) + '\n'


def var_fmt(r, var):
    var_flag = var + '_FLAG'
    return f'{r[var]:6.1f} {r[var_flag]:3}' 


def write_formatted_data(df, outfile, columns=these_columns):
    with open(outfile, 'w') as f:
        # TODO - Add header
        for record in df[these_columns].iterrows():
            f.write(record_fmt(record))
    return
