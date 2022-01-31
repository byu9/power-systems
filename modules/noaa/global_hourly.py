#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import pandas
import logging
from multiprocessing import Pool

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


def read_csv(f):
    logging.info('reading csv file "{}"'.format(f))
    return pandas.read_csv(f,
                           header=0,
                           index_col=1,
                           parse_dates=[1],
                           dtype='str')



def read_csv_slices(filenames):
    with Pool(processes=None) as pool:
        dataframes = pool.map(read_csv, filenames)

    dataframe = pandas.concat(dataframes, axis='index')

    dataframe.sort_index(axis='index', inplace=True)
    dataframe.index = dataframe.index.tz_localize('UTC')
    dataframe.index.rename('utc_time', inplace=True)

    tmp_code = dataframe['TMP'].str.split(',', expand=True)
    dataframe['tmp_val'] = tmp_code[0]
    dataframe['tmp_quality'] = tmp_code[1]

    INVALID_TMP_VAL = '+9999'
    dataframe.drop(dataframe.index[
        dataframe['tmp_val'] == INVALID_TMP_VAL], inplace=True)

    celsius = dataframe['tmp_val'].astype(float) / 10
    CELSIUS_MAX = 61.8
    CELSIUS_MIN = -93.2
    if not all(celsius.between(CELSIUS_MIN, CELSIUS_MAX, inclusive='both')):
        raise ValueError('unable to eliminate implausible celsius readings')

    return pandas.DataFrame({
        'station' : dataframe['STATION'],
        'latitude': dataframe['LATITUDE'].astype(float),
        'longitude': dataframe['LONGITUDE'].astype(float),
        'elevation': dataframe['ELEVATION'].astype(float),
        'name': dataframe['NAME'],
        'celsius': celsius,
        'celsius_quality': dataframe['tmp_quality'],
    })
