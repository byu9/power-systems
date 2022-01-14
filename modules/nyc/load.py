#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
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


class Real_Time_Load_Remote_Archive(Remote_File, Compressed_File):
    def __init__(self, month, year):
        download_name = '{}{}01pal_csv.zip'.format(year, month)
        url = 'http://mis.nyiso.com/public/csv/pal/{}'.format(
            download_name)
        Remote_File.__init__(self, url, download_name)


def read_csv(filename):
    import pandas
    logging.debug('reading csv file "{}"'.format(filename))
    return pandas.read_csv(filename, header=0, index_col=0, parse_dates=[0])


def read_csv_slices(filenames, pivot_values=None):
    from ..tools import Multiprocessing_Pool
    import pandas

    with Multiprocessing_Pool() as pool:
        dataframes = pool.map(read_csv, filenames)
    dataframe = pandas.concat(dataframes, axis='index')

    timezone_has_dst = {
        'EST': False,
        'EDT': True,
    }

    logging.info('Localizing timezone')
    dst_mask = dataframe['Time Zone'].map(timezone_has_dst)
    dataframe.index = dataframe.index.tz_localize(
        'America/New_York', ambiguous=dst_mask)
    dataframe.index.name = 'time'
    dataframe.drop(columns=['Time Zone'], inplace=True)

    rename_columns = {
        # old_name                          : new_name
        'Name'                              : 'zone',
        'PTID'                              : 'ptid',
        'Integrated Load'                   : 'load',
        'Load'                              : 'load',
    }
    dataframe.rename(columns=rename_columns, inplace=True)

    if pivot_values is not None:
        dataframe = dataframe.pivot_table(index=dataframe.index,
                                          columns='zone', values=pivot_values)
        dataframe.rename_axis(None, axis='columns', inplace=True)

    return dataframe
