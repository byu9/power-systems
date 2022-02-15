#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
#
# Converts a Gregorian date into Julian calendar accounding for the difference
# between Earth rotation time and Terrestrial Time (delta_T) published in the
# yearly Astronomical Alamanac.
from pandas import Timestamp
from functools import cached_property

class Julian:
    def __init__(self, datetime, delta_T, timezone=None):
        timestamp = Timestamp(datetime)

        if timestamp.tz is None:
            if timezone is None:
                raise ValueError(
                    'Datetime is timezone-naive, and a timezone'
                    'is not provided')
            else:
                timestamp = timestamp.tz_localize(timezone)

        self._JD = timestamp.tz_convert('GMT').to_julian_date()
        self._Delta_T = delta_T

    @cached_property
    def _JDE(self):
        return self._JD + self._Delta_T / 86400

    @cached_property
    def _JC(self):
        return (self._JD - 2451545) / 36525

    @cached_property
    def _JCE(self):
        return (self._JDE - 2451545) / 36525

    @cached_property
    def _JME(self):
        return self._JCE / 10

    @property
    def day(self):
        return self._JD

    @property
    def century(self):
        return self._JC

    @property
    def ephermeris_day(self):
        return self._JDE

    @property
    def ephemeris_century(self):
        return self._JCE

    @property
    def ephemeris_millennium(self):
        return self._JME
