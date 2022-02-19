#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates timeseries of the Macky-Glass difference equation

The Macky-Glass equations originally model the variation in the relative
quantity of mature cells in the blood and exhibit chaotic behavior in some
parameter combinations. The implementation uses the equation commonly numbered
as equation 2.
"""
import numpy


def simulate(n_samples, tau=20, gamma=0.1, beta=0.2, n=10, init=1.2):
    """
    Creates a macky glass time series

    Parameters
    ----------
    n_samples : int
        Number of samples to generate, must be positive.
    tau : int
        Delay in number of samples, must be positive.
    gamma : float
        Decay rate, must be positive
    beta : float
        production rate, must be positive.
    n : int
        Power of the term in the denominator, must be positive.

    init: float
        Initial condition.

    Returns
    -------
    Numpy array of shape (n_samples, ).

    """

    assert isinstance(n_samples, int) and (n_samples > 0)
    assert isinstance(tau, int) and (tau > 0)
    assert gamma > 0
    assert beta > 0
    assert n > 0

    x = numpy.empty(n_samples + tau)
    x[:tau] = 0
    x[tau] = init

    for t in range(tau, n_samples + tau - 1):
        xdot = beta * x[t-tau] / (1 + x[t-tau]**n) - gamma * x[t]
        x[t+1] = x[t] + xdot

    return x[-n_samples:]
