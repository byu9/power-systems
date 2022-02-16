#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import logging

from ..tools import (
    Remote_File,
)

class ISD_Remote_File(Remote_File):
    def __init__(self, year, station):
        download_name = '{}-{}.csv'.format(year, station)
        url = (
            'https://www.ncei.noaa.gov/data/global-hourly/access/'
            '{}/{}.csv'
        ).format(year, station)

        Remote_File.__init__(self, url, download_name)


def read_csv(filename):
    import pandas
    logging.debug('reading csv file "{}"'.format(filename))
    return pandas.read_csv(filename, header=0, index_col=1, parse_dates=[1],
                           dtype='str')

def read_csv_slices(filenames):
    from ..tools import Multiprocessing_Pool
    import pandas
    from numpy import NaN

    with Multiprocessing_Pool() as pool:
        raw_dataframes = pool.map(read_csv, filenames)
    raw_dataframe = pandas.concat(raw_dataframes, axis='index')

    logging.info('Localizing timezone')
    raw_dataframe.index = raw_dataframe.index.tz_localize('UTC')
    raw_dataframe.index.rename('time', inplace=True)

    tmp_code = raw_dataframe['TMP'].str.split(',', n=1, expand=True)
    tmp_val     = tmp_code[0]
    tmp_quality = tmp_code[1]

    INVALID_TMP_VAL = '+9999'
    tmp_val[tmp_val == INVALID_TMP_VAL] = NaN

    CELSIUS_MAX = 61.8
    CELSIUS_MIN = -93.2
    celsius = pandas.to_numeric(tmp_val) / 10
    celsius[~celsius.between(CELSIUS_MIN, CELSIUS_MAX, inclusive='both')] = NaN

    dew_code = raw_dataframe['DEW'].str.split(',', n=1, expand=True)
    dew_val     = dew_code[0]
    dew_quality = dew_code[1]

    INVALID_DEW_VAL = '+9999'
    dew_val[dew_val == INVALID_DEW_VAL] = NaN

    DEW_MAX = 36.8
    DEW_MIN = -98.2
    dew = pandas.to_numeric(dew_val) / 10
    dew[~dew.between(DEW_MIN, DEW_MAX, inclusive='both')] = NaN

    dataframe = pandas.DataFrame(index=raw_dataframe.index)

    dataframe['station']         = raw_dataframe['STATION'].astype(str)
    dataframe['name']            = raw_dataframe['NAME'].astype(str)
    dataframe['latitude']        = pandas.to_numeric(raw_dataframe['LATITUDE'])
    dataframe['longitude']       = pandas.to_numeric(raw_dataframe['LONGITUDE'])
    dataframe['elevation']       = pandas.to_numeric(raw_dataframe['ELEVATION'])
    dataframe['celsius']         = celsius
    dataframe['celsius_quality'] = tmp_quality
    dataframe['dew']             = dew
    dataframe['dew_quality']     = dew_quality

    logging.info('Sorting dataframe index')
    dataframe.sort_index(axis='index', inplace=True)

    return dataframe
