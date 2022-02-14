#!/usr/bin/env python3
import unittest
from .heliocentric import heliocentric_vector

class Test_Heliocentric_Vector(unittest.TestCase):
    def test_case1(self):
        from .julian import Julian
        delta_T = 67
        julian = Julian('2003-10-17T12:30:30.000-07:00', delta_T)
        JME = julian.ephemeris_millennium

        (L, B, R) = heliocentric_vector(JME)

        self.assertAlmostEqual(L, 24.0182616917)
        self.assertAlmostEqual(B, -0.0001011219)
        self.assertAlmostEqual(R, 0.9965422974)
