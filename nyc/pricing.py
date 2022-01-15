#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import pandas
import logging

from tools import (
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



class DataFrame(pandas.DataFrame):
    @property
    def _constructor(self):
        return DataFrame


def read_csv_slices(filenames):

    def read_csv(f):
        logging.info('reading csv file "{}"'.format(f))
        return pandas.read_csv(f,
                               header=0,
                               index_col=0,
                               parse_dates=[0])

    dataframes = [read_csv(f) for f in filenames]
    dataframe = pandas.concat(dataframes, axis='index')
    dataframe.sort_index(axis='index', inplace=True)

    return DataFrame(dataframe)
