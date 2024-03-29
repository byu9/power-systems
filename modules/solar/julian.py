#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
#
# Converts a Gregorian date into Julian calendar accounding for the difference
# between Earth rotation time and Terrestrial Time (delta_T) published in the
# yearly Astronomical Alamanac.
from pandas import Timestamp

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

try:
    from functools import cached_property
except ImportError:
    from backports.cached_property import cached_property

#
# Corrections between Terristrial Time (TT), Universal Time (UTC) and
# Coordinated Universal Time (UTC)
#
_time_corrections = {
    # (start, TT-UT1,    UT1-UTC)
    ('1972-01-01T00:00:00.000GMT', +42.23,    -0.05),
    ('1972-07-01T00:00:00.000GMT', +42.80,    +0.38),
    ('1973-01-01T00:00:00.000GMT', +43.37,    +0.81),
    ('1973-07-01T00:00:00.000GMT', +43.93,    +0.25),
    ('1974-01-01T00:00:00.000GMT', +44.49,    +0.69),
    ('1974-07-01T00:00:00.000GMT', +44.99,    +0.19),
    ('1975-01-01T00:00:00.000GMT', +45.48,    +0.70),
    ('1975-07-01T00:00:00.000GMT', +45.97,    +0.21),
    ('1976-01-01T00:00:00.000GMT', +46.46,    +0.72),
    ('1976-07-01T00:00:00.000GMT', +46.99,    +0.19),
    ('1977-01-01T00:00:00.000GMT', +47.52,    +0.66),
    ('1977-07-01T00:00:00.000GMT', +48.03,    +0.15),
    ('1978-01-01T00:00:00.000GMT', +48.53,    +0.65),
    ('1978-07-01T00:00:00.000GMT', +49.06,    +0.12),
    ('1979-01-01T00:00:00.000GMT', +49.59,    +0.59),
    ('1979-07-01T00:00:00.000GMT', +50.07,    +0.11),
    ('1980-01-01T00:00:00.000GMT', +50.54,    +0.64),
    ('1980-07-01T00:00:00.000GMT', +50.96,    +0.22),
    ('1981-01-01T00:00:00.000GMT', +51.38,    -0.20),
    ('1981-07-01T00:00:00.000GMT', +51.78,    +0.40),
    ('1982-01-01T00:00:00.000GMT', +52.17,    +0.01),
    ('1982-07-01T00:00:00.000GMT', +52.57,    +0.61),
    ('1983-01-01T00:00:00.000GMT', +52.96,    +0.22),
    ('1983-07-01T00:00:00.000GMT', +53.38,    +0.80),
    ('1984-01-01T00:00:00.000GMT', +53.79,    +0.39),
    ('1984-07-01T00:00:00.000GMT', +54.07,    +0.11),
    ('1985-01-01T00:00:00.000GMT', +54.34,    -0.16),
    ('1985-07-01T00:00:00.000GMT', +54.61,    +0.57),
    ('1986-01-01T00:00:00.000GMT', +54.87,    +0.31),
    ('1986-07-01T00:00:00.000GMT', +55.10,    +0.08),
    ('1987-01-01T00:00:00.000GMT', +55.32,    -0.14),
    ('1987-07-01T00:00:00.000GMT', +55.57,    -0.39),
    ('1988-01-01T00:00:00.000GMT', +55.82,    +0.36),
    ('1988-07-01T00:00:00.000GMT', +56.06,    +0.12),
    ('1989-01-01T00:00:00.000GMT', +56.30,    -0.12),
    ('1989-07-01T00:00:00.000GMT', +56.58,    -0.40),
    ('1990-01-01T00:00:00.000GMT', +56.86,    +0.32),
    ('1990-07-01T00:00:00.000GMT', +57.22,    -0.04),
    ('1991-01-01T00:00:00.000GMT', +57.57,    +0.61),
    ('1991-07-01T00:00:00.000GMT', +57.94,    +0.24),
    ('1992-01-01T00:00:00.000GMT', +58.31,    -0.13),
    ('1992-07-01T00:00:00.000GMT', +58.72,    +0.46),
    ('1993-01-01T00:00:00.000GMT', +59.12,    +0.06),
    ('1993-07-01T00:00:00.000GMT', +59.55,    +0.63),
    ('1994-01-01T00:00:00.000GMT', +59.98,    +0.20),
    ('1994-07-01T00:00:00.000GMT', +60.38,    +0.80),
    ('1995-01-01T00:00:00.000GMT', +60.78,    +0.40),
    ('1995-07-01T00:00:00.000GMT', +61.20,    -0.02),
    ('1996-01-01T00:00:00.000GMT', +61.63,    +0.55),
    ('1996-07-01T00:00:00.000GMT', +61.96,    +0.22),
    ('1997-01-01T00:00:00.000GMT', +62.29,    -0.11),
    ('1997-07-01T00:00:00.000GMT', +62.63,    +0.55),
    ('1998-01-01T00:00:00.000GMT', +62.97,    +0.21),
    ('1998-07-01T00:00:00.000GMT', +63.22,    -0.04),
    ('1999-01-01T00:00:00.000GMT', +63.47,    +0.71),
    ('1999-07-01T00:00:00.000GMT', +63.66,    +0.52),
    ('2000-01-01T00:00:00.000GMT', +63.82,    +0.36),
    ('2000-07-01T00:00:00.000GMT', +63.98,    +0.20),
    ('2001-01-01T00:00:00.000GMT', +64.09,    +0.09),
    ('2001-07-01T00:00:00.000GMT', +64.20,    -0.02),
    ('2002-01-01T00:00:00.000GMT', +64.30,    -0.12),
    ('2002-07-01T00:00:00.000GMT', +64.41,    -0.23),
    ('2003-01-01T00:00:00.000GMT', +64.47,    -0.29),
    ('2003-07-01T00:00:00.000GMT', +64.55,    -0.37),
    ('2004-01-01T00:00:00.000GMT', +64.57,    -0.39),
    ('2004-07-01T00:00:00.000GMT', +64.65,    -0.47),
    ('2005-01-01T00:00:00.000GMT', +64.68,    -0.50),
    ('2005-07-01T00:00:00.000GMT', +64.80,    -0.62),
    ('2006-01-01T00:00:00.000GMT', +64.85,    +0.33),
    ('2006-07-01T00:00:00.000GMT', +64.99,    +0.19),
    ('2007-01-01T00:00:00.000GMT', +65.15,    +0.03),
    ('2007-07-01T00:00:00.000GMT', +65.34,    -0.16),
    ('2008-01-01T00:00:00.000GMT', +65.45,    -0.27),
    ('2008-07-01T00:00:00.000GMT', +65.63,    -0.45),
    ('2009-01-01T00:00:00.000GMT', +65.78,    +0.40),
    ('2009-07-01T00:00:00.000GMT', +65.95,    +0.23),
    ('2010-01-01T00:00:00.000GMT', +66.07,    +0.11),
    ('2010-07-01T00:00:00.000GMT', +66.24,    -0.06),
    ('2011-01-01T00:00:00.000GMT', +66.32,    -0.14),
    ('2011-07-01T00:00:00.000GMT', +66.47,    -0.29),
    ('2012-01-01T00:00:00.000GMT', +66.60,    -0.42),
    ('2012-07-01T00:00:00.000GMT', +66.77,    +0.41),
    ('2013-01-01T00:00:00.000GMT', +66.91,    +0.27),
    ('2013-07-01T00:00:00.000GMT', +67.13,    +0.05),
    ('2014-01-01T00:00:00.000GMT', +67.28,    -0.10),
    ('2014-07-01T00:00:00.000GMT', +67.49,    -0.31),
    ('2015-01-01T00:00:00.000GMT', +67.64,    -0.46),
    ('2015-07-01T00:00:00.000GMT', +67.86,    +0.32),
    ('2016-01-01T00:00:00.000GMT', +68.10,    +0.08),
    ('2016-07-01T00:00:00.000GMT', +68.40,    -0.22),
    ('2017-01-01T00:00:00.000GMT', +68.59,    +0.59),
    ('2017-07-01T00:00:00.000GMT', +68.82,    +0.36),
    ('2018-01-01T00:00:00.000GMT', +68.96,    +0.22),
    ('2018-07-01T00:00:00.000GMT', +69.11,    +0.07),
    ('2019-01-01T00:00:00.000GMT', +69.22,    -0.04),
    ('2019-07-01T00:00:00.000GMT', +69.35,    -0.17),
    ('2020-01-01T00:00:00.000GMT', +69.36,    -0.18),
    ('2020-07-01T00:00:00.000GMT', +69.42,    -0.24),
    ('2021-01-01T00:00:00.000GMT', +69.36,    -0.18),
    ('2021-07-01T00:00:00.000GMT', +69.35,    -0.17),
    ('2022-01-01T00:00:00.000GMT', +69.29,    -0.11),
}

class Julian:
    def __init__(self, datetime, Delta_T=None, timezone=None):
        timestamp = Timestamp(datetime)

        if timestamp.tz is None:
            if timezone is None:
                raise ValueError(
                    'Datetime is timezone-naive, and a timezone'
                    'is not provided')
            else:
                timestamp = timestamp.tz_localize(timezone)

        GMT = timestamp.tz_convert('GMT')

        if Delta_T is None:
            for start, Delta_T, Delta_UT1 in _time_corrections:
                if timestamp >= Timestamp(start):
                    break

        self._JD = GMT.to_julian_date()
        self._Delta_T = Delta_T
        self._timestamp = timestamp


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
