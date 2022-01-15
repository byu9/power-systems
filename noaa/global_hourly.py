#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
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
