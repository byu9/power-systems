#!/usr/bin/env python3
import unittest
from solar.position import Observer_Solar_Position

class Test_Solar_Position(unittest.TestCase):
    def test_case1(self):
        from solar.julian import Julian
        import numpy
        delta_T = 67
        julian = Julian('2003-10-17T12:30:30.000-07:00', delta_T)

        position = Observer_Solar_Position(
            latitude = 39.742476,
            longitude = -105.1786,
            elevation = 1830.14,
            annual_millibar = 820,
            avg_celsius = 11,
            hori_slope = 30,
            azimuth_angle= -10
        ).get_solar_position(julian)

        self.assertAlmostEqual(position._L, 24.0182616917)
        self.assertAlmostEqual(position._B, -0.0001011219)
        self.assertAlmostEqual(position._R, 0.9965422974)
        self.assertAlmostEqual(position._Theta, 204.0182616917)
        self.assertAlmostEqual(position._beta, 0.0001011219)
        self.assertAlmostEqual(position._Delta_Psi, -0.00399840)
        self.assertAlmostEqual(position._Delta_epsilon, 0.00166657)
        self.assertAlmostEqual(position._lambda, 204.0085519281)
        self.assertAlmostEqual(position._epsilon, 23.440465, places=6)
        self.assertAlmostEqual(position._alpha, 202.22741, places=5)
        self.assertAlmostEqual(position._delta, -9.31434, places=6)
        self.assertAlmostEqual(position._alpha_prime, 202.22704, places=5)
        self.assertAlmostEqual(position._delta_prime, -9.316179, places=6)
        self.assertAlmostEqual(position._H, 11.105900, places=5)
        self.assertAlmostEqual(position._H_prime, 11.10629, places=4)
        self.assertAlmostEqual(position._theta, 50.11162, places=5)
        self.assertAlmostEqual(position._Phi, 194.34024, places=6)
        self.assertAlmostEqual(position._I, 25.18700, places=6)
        self.assertAlmostEqual(position.equation_of_time, 14.641503, places=4)
