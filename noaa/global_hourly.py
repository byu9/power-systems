#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import pandas
import logging

from tools import (
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




class DataFrame(pandas.DataFrame):
    @property
    def _constructor(self):
        return DataFrame





def read_csv(f):
    logging.info('reading csv file "{}"'.format(f))
    return pandas.read_csv(f,
                           header=0,
                           index_col='DATE',
                           parse_dates=['DATE'],
                           dtype='str')


def parse_celsius(str_series):
    INVALID_CELSIUS = '+9999'
    temp_code = str_series.split(',', expand=True)
    celsius = temp_code[0]
    quality = temp_code[1]

    celsius = celsius.astype(float) / 10
    return celsius, quality


def read_csv_slices(filenames):
    dataframes = [read_csv(f) for f in filenames]
    dataframe = pandas.concat(dataframes, axis='index', sort=True)

    celsius, celsius_quality = parse_celsius(dataframe['TMP'].str)

    return DataFrame({
        'station' : dataframe['STATION'].astype(float),
        'latitude': dataframe['LATITUDE'].astype(float),
        'longitude': dataframe['LONGITUDE'].astype(float),
        'elevation': dataframe['ELEVATION'].astype(float),
        'name': dataframe['NAME'],
        'celsius': celsius,
        'celsius_quality': celsius_quality,
    })
