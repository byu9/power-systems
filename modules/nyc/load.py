#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import pandas
import logging
from multiprocessing import Pool

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
    with Pool(processes=None) as pool:
        dataframes = pool.map(read_csv, filenames)

    dataframe = pandas.concat(dataframes, axis='index')
    dataframe.drop_duplicates(inplace=True)

    timezone_mapping = {
        'EST': 'Etc/GMT-5',
        'EDT': 'Etc/GMT-4',
    }

    dataframe['utc_time'] = dataframe.apply(
        lambda r: r.name.tz_localize(
            timezone_mapping[r['Time Zone']]
        ).tz_convert('UTC'), 
        axis='columns'
    )

    dataframe.drop(columns='Time Zone', inplace=True)
    dataframe.set_index('utc_time', drop=True, inplace=True)
    dataframe.sort_index(axis='index', inplace=True)

    rename_columns = {
        # old_name                          : new_name
        'Name'                              : 'zone',
        'PTID'                              : 'ptid',
        'Integrated Load'                   : 'integrated_load',
    }

    dataframe.rename(columns=rename_columns, inplace=True)

    return dataframe
