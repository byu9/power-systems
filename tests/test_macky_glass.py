#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 14:04:31 2022

@author: jdoe
"""

import unittest
from chaos.macky_glass import simulate


class Test_Macky_Glass(unittest.TestCase):
    def test1(self):
        x = simulate(10)
        correct_x = [
            1.200000e+00,
            1.080000e+00,
            9.720000e-01,
            8.748000e-01,
            7.873200e-01,
            7.085880e-01,
            6.377292e-01,
            5.739563e-01,
            5.165607e-01,
            4.649046e-01,
        ]
        for x_val, correct_val in zip(x, correct_x):
            self.assertAlmostEqual(x_val, correct_val)
