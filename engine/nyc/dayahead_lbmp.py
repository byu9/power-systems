#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu

from ..url_retrievers import (
    AbstractUrlRetriever,
)

from ..archive_unpackers import (
    AbstractArchive,
)

from ..timeseries import (
    AbstractTimeSeriesData,
)

import pandas



class Archive(AbstractUrlRetriever, AbstractArchive):
    def __init__(self, month_year):
        # month_year like '01-2022'

        (month, year) = month_year.split('-')
        self._filename = '{}{}01damlbmp_zone_csv.zip'.format(year, month)
        self._url = 'http://mis.nyiso.com/public/csv/damlbmp/{}'.format(
            self.filename)

    @property
    def download_url(self):
        return self._url

    @property
    def filename(self):
        return self._filename


class DataFrame(AbstractTimeSeriesData, pandas.DataFrame):
    @property
    def _constructor(self):
        return DataFrame


def read_csv(file_path):
    dataframe = pandas.read_csv(file_path, header=0, index_col=0,
                                parse_dates=[0])
    return DataFrame(dataframe)
