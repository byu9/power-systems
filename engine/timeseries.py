#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
from abc import ABC, abstractmethod

class AbstractTimeSeriesData:
    def between_datetime(self, start, end, inclusive='both'):
        index = self.index

        if inclusive == 'left':
            mask = (index >= start) & (index < end)

        elif inclusive == 'right':
            mask = (index > start) & (index <= end)

        elif inclusive == 'both':
            mask = (index >= start) & (index <= end)

        else:
            raise ValueError('unrecognized inclusive directive')

        return self[mask]
