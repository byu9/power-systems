#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import pandas
import logging

from ..tools import (
    Remote_File,
    Compressed_File,
)


class Integrated_Real_Time_Load_Remote_Archive(Remote_File, Compressed_File):
    def __init__(self, month, year):
        download_name = '{}{}01palIntegrated_csv.zip'.format(year, month)
        url = 'http://mis.nyiso.com/public/csv/palIntegrated/{}'.format(
            download_name)
        Remote_File.__init__(self, url, download_name)

def read_csv(f):
    logging.info('reading csv file "{}"'.format(f))
    return pandas.read_csv(f,
                           header=0,
                           index_col=0,
                           parse_dates=[0])

def read_csv_slices(filenames):
    dataframes = pandas.Series(filenames).apply(read_csv)
    dataframe = pandas.concat(dataframes, axis='index')
    dataframe.drop(columns='Time Zone', inplace=True)
    dataframe.drop_duplicates(inplace=True)

    dataframe.index = dataframe.index.tz_localize(
        'America/New_York').tz_convert('UTC')
    dataframe.sort_index(axis='index', inplace=True)
    dataframe.index.rename('utc_time', inplace=True)

    rename_columns = {
        # old_name                          : new_name
        'Name'                              : 'zone',
        'PTID'                              : 'ptid',
        'Integrated_Load'                   : 'integrated_load',
    }

    dataframe.rename(columns=rename_columns, inplace=True)

    return dataframe
