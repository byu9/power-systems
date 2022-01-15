#!/usr/bin/env python3
import pandas
import logging

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

    return DataFrame(dataframe)
