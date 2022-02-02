#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu

class Time_Period:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def filter(self, dataframe, inclusive='left'):
        import operator
        comparators = {
            'left'    : (operator.le, operator.gt),
            'right'   : (operator.lt, operator.ge),
            'both'    : (operator.le, operator.ge),
            'neither' : (operator.lt, operator.gt),
        }

        (after, before) = comparators[inclusive]

        index_is_between = (
            after(self._start, dataframe.index) &
            before(self._end, dataframe.index)
        )

        return dataframe[index_is_between]
