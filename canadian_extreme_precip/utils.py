"""Contains functions for processing data files"""
import numpy as np


def snow_day_fraction(x):
    """Calculates fraction of days with snow on the ground"""
    daysinmonth = x.index[0].daysinmonth
    nvalues = x.count()
    if nvalues == daysinmonth:
        xfraction = np.sum(x > 0) / daysinmonth
    else:
        xfraction = np.nan
    return xfraction


def month_mean(x):
    nvalues = x.count()
    if nvalues == x.index[0].daysinmonth:
        xavg = np.mean(x)
    else:
        xavg = np.nan
    return xavg


def month_sum(x):
    """Returns month sum if number of values equals days in month,
    otherwise returns nan"""
    nvalues = x.count()
    if nvalues == x.index[0].daysinmonth:
        xsum = np.sum(x)
    else:
        xsum = np.nan
    return xsum


def to_monthly(df):
    """Calculate monthly time series

    :df: pandas dataframe containing:
            MEAN_TEMPERATURE
            MIN_TEMPERATURE
            MAX_TEMPERATURE
            TOTAL_PRECIPITATION
            TOTAL_RAIN
            TOTAL_SNOW
            SNOW_ON_GROUND
    """
    return df.resample('M').apply({
        'MEAN_TEMPERATURE': month_mean,
        'MIN_TEMPERATURE': month_mean,
        'MAX_TEMPERATURE': month_mean,
        'TOTAL_PRECIPITATION': month_sum,
        'TOTAL_RAIN': month_sum,
        'TOTAL_SNOW': month_sum,
        'SNOW_ON_GROUND': snow_day_fraction,  # Days with snow on the ground
        })


def to_climatology(df):
    """Calculates climatology for min, mean and max temperatures;
       total precipitation, rain and snow; and frequency of snow on ground.

    :df: pandas dataframe containing:
            MEAN_TEMPERATURE
            MIN_TEMPERATURE
            MAX_TEMPERATURE
            TOTAL_PRECIPITATION
            TOTAL_RAIN
            TOTAL_SNOW
            SNOW_ON_GROUND
    """
    return df.groupby(df.index.month).mean()
