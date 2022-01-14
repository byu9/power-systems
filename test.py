#!/usr/bin/env python3
import logger_level_is_debug
import pandas

from nyc.pricing import (
    Dayahead_LBMP_Remote_Archive,
    Realtime_LBMP_Remote_Archive,
)

from nyc.timeseries import (
    read_csv_slices,
)

from glob import (
    glob,
)



months_to_download = {
    # year: [list_of_months]

    '2016': ['11', '12'],
    '2017': ['01', '02', '03', '04', '11', '12'],
    '2018': ['01', '02', '03', '04', '11', '12'],
    '2019': ['01', '02', '03', '04', '11', '12'],
    '2020': ['01', '02', '03', '04', '11', '12'],
    '2021': ['01', '02', '03', '04'],
}


dayahead_archives = [
    Dayahead_LBMP_Remote_Archive(m, y)

    for y, months in months_to_download.items()
    for m in months
]

realtime_archives = [
    Realtime_LBMP_Remote_Archive(m, y)

    for y, months in months_to_download.items()
    for m in months
]


for a in dayahead_archives + realtime_archives:
    a.download_into('999-data/download/')

for da in dayahead_archives:
    da.extract_into('999-data/dayahead/')

for rt in realtime_archives:
    rt.extract_into('999-data/realtime/')


dayahead_csv_files = glob('999-data/dayahead/*.csv')
realtime_csv_files = glob('999-data/realtime/*.csv')

df_dayahead = read_csv_slices(dayahead_csv_files)
df_realtime = read_csv_slices(realtime_csv_files)


# for convenience of typing
rename_columns = {
    # old_name                          : new_name
    'Time Stamp'                        : 'time',
    'Name'                              : 'zone',
    'PTID'                              : 'ptid',
    'LBMP ($/MWHr)'                     : 'lbmp',
    'Marginal Cost Losses ($/MWHr)'     : 'lbmp_loss',
    'Marginal Cost Congestion ($/MWHr)' : 'lbmp_congest'
}
for df in [df_dayahead, df_realtime]:
    df.rename(columns=rename_columns, inplace=True)


# filter data of interest
keep_zones = ['N.Y.C.', 'NORTH']

df_dayahead = df_dayahead.loc[df_dayahead['zone'].isin(keep_zones)][['lbmp']]
df_realtime = df_realtime.loc[df_realtime['zone'].isin(keep_zones)][['lbmp']]


print(df_dayahead, df_realtime)
