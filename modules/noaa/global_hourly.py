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

    with Multiprocessing_Pool() as pool:
        raw_dataframes = pool.map(read_csv, filenames)
    raw_dataframe = pandas.concat(raw_dataframes, axis='index')

    logging.info('Localizing timezone')
    raw_dataframe.index = raw_dataframe.index.tz_localize('UTC')
    raw_dataframe.index.rename('time', inplace=True)

    tmp_code = raw_dataframe['TMP'].str.split(',', n=1, expand=True)
    raw_dataframe['tmp_val']     = tmp_code[0]
    raw_dataframe['tmp_quality'] = tmp_code[1]

    INVALID_TMP_VAL = '+9999'
    drop_mask = (raw_dataframe['tmp_val'] == INVALID_TMP_VAL)
    raw_dataframe.drop(raw_dataframe.index[drop_mask], inplace=True)

    CELSIUS_MAX = 61.8
    CELSIUS_MIN = -93.2
    celsius = tmp_val.to_numeric() / 10
    if not all(celsius.between(CELSIUS_MIN, CELSIUS_MAX, inclusive='both')):
        raise ValueError('unable to eliminate implausible celsius readings')

    dataframe = pandas.DataFrame(index=raw_dataframe.index)

    dataframe['station']         = raw_dataframe['STATION'].astype(str)
    dataframe['name']            = raw_dataframe['NAME'].astype(str)
    dataframe['latitude']        = raw_dataframe['LATITUDE'].to_numeric()
    dataframe['longitude']       = raw_dataframe['LONGITUDE'].to_numeric()
    dataframe['elevation']       = raw_dataframe['ELEVATION'].to_numeric()
    dataframe['celsius']         = celsius
    dataframe['celsius_quality'] = raw_dataframe['tmp_quality'].astype(str)

    logging.info('Sorting dataframe index')
    dataframe.sort_index(axis='index', inplace=True)

    return dataframe
