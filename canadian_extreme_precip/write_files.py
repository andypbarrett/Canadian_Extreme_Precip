'''Module for writing station data to stdout of file'''

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
    return ' '.join(sfmt)


def var_fmt(r, var):
    var_flag = var + '_FLAG'
    return f'{r[var]:6.1f} {r[var_flag]:3}' 

