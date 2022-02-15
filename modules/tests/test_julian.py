#!/usr/bin/env python3
import unittest
from solar.julian import Julian

class Test_Julian_Date(unittest.TestCase):
    def test_nrel1(self):
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
            result = Julian(datetime, Delta_T=0, timezone='GMT').day
            self.assertAlmostEqual(key, result)

    def test_nrel2(self):
        delta_T = 67
        julian = Julian('2003-10-17T12:30:30.000-07:00', delta_T)
        self.assertAlmostEqual(julian._JD, 2452930.312847, places=6)
        self.assertAlmostEqual(julian._JC, 0.037928, places=6)
        self.assertAlmostEqual(julian._JDE, 2452930.313623, places=6)
        self.assertAlmostEqual(julian._JCE, 0.037928, places=6)
        self.assertAlmostEqual(julian._JME, 0.003793, places=6)
