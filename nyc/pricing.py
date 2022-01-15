#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
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
