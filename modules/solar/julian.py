#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
#
# Converts a Gregorian date into Julian calendar accounding for the difference
# between Earth rotation time and Terrestrial Time (delta_T) published in the
# yearly Astronomical Alamanac.
from pandas import Timestamp

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
        self._delta_T = delta_T

    @property
    def day(self):
        return self._JD

    @property
    def century(self):
        return (self.day - 2451545) / 36525

    @property
    def ephermeris_day(self):
        return self.day + self._delta_T / 86400

    @property
    def ephemeris_century(self):
        return (self.ephermeris_day - 2451545) / 36525

    @property
    def ephemeris_millennium(self):
        return self.ephemeris_century / 10
