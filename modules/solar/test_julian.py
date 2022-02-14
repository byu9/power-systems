#!/usr/bin/env python3
import unittest
from .julian_date import to_julian_date

class Test_Julian_Date(unittest.TestCase):
    def test_nrel(self):
        CASES = (
            # (datetime, julian_date)
            ("January 1, 2000 12:00:00",    2451545),
            ("January 1, 1999 00:00:00",    2451179.5),
            ("January 27, 1987 00:00:00",   2446822.5),
            ("June 19, 1987 12:00:00",      2446966),
            ("January 27, 1988 00:00:00",   2447187.5),
            ("June 19, 1988 12:00:00",      2447332),
            ("January 1, 1900 00:00:00",    2415020.5),
        )

        for datetime, key in CASES:
            result = to_julian_date(datetime)
            self.assertAlmostEqual(key, result)
