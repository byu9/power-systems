#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import logging

from ..tools import (
    Remote_File,
    Compressed_File,
)


class Dayahead_LBMP_Remote_Archive(Remote_File, Compressed_File):
    def __init__(self, month, year):
        download_name = '{}{}01damlbmp_zone_csv.zip'.format(year, month)
        url = 'http://mis.nyiso.com/public/csv/damlbmp/{}'.format(download_name)
        Remote_File.__init__(self, url, download_name)


class Realtime_LBMP_Remote_Archive(Remote_File, Compressed_File):
    def __init__(self, month, year):
        download_name = '{}{}01realtime_zone_csv.zip'.format(year, month)
        url = 'http://mis.nyiso.com/public/csv/realtime/{}'.format(
            download_name)
        Remote_File.__init__(self, url, download_name)


def read_csv(filename):
    import pandas
    logging.info('reading csv file "{}"'.format(filename))
    return pandas.read_csv(filename, header=0, index_col=0, parse_dates=[0])


def read_csv_slices(filenames, pivot_values=None):
    from ..tools import Multiprocessing_Pool
    import pandas

    with Multiprocessing_Pool() as pool:
        dataframes = pool.map(read_csv, filenames)
    dataframe = pandas.concat(dataframes, axis='index')

    logging.info('Converting timezone to UTC')
    dataframe.index = dataframe.index.tz_localize('EST').tz_convert('UTC')
    dataframe.index.rename('utc_time', inplace=True)

    rename_columns = {
        # old_name                          : new_name
        'Name'                              : 'zone',
        'PTID'                              : 'ptid',
        'LBMP ($/MWHr)'                     : 'lbmp',
        'Marginal Cost Losses ($/MWHr)'     : 'lbmp_loss',
        'Marginal Cost Congestion ($/MWHr)' : 'lbmp_congest'
    }
    dataframe.rename(columns=rename_columns, inplace=True)

    logging.info('Sorting dataframe index')
    dataframe.sort_index(axis='index', inplace=True)

    if pivot_values is not None:
        dataframe = dataframe.pivot_table(index=dataframe.index,
                                          columns='zone', values=pivot_values)
        dataframe.rename_axis(None, axis='columns', inplace=True)

    return dataframe
