"""Metrics for evaluating regression accuracy
"""


import numpy
import pandas

def max_absolute_error(pred, actual):
    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    return max(abs(pred - actual))

def min_absolute_error(pred, actual):
    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    return min(abs(pred - actual))

def mean_absolute_error(pred, actual):
    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    return abs(actual - pred).mean()

def mean_squared_error(pred, actual):
    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    return ((actual - pred)**2).mean()

def root_mean_squared_error(pred, actual):
    mse = mean_squared_error(pred, actual)

    return sqrt(mse)

def mean_absolute_percent_error(pred, actual):
    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    return abs((actual - pred) / actual).mean() * 100

def mean_absolute_percent_error_full_scale(pred, actual):
    """Mean Absolute Percentage Error Definition by US Department of Energy
    Divides by the max/full scale of the actual series
    """
    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    return abs((actual - pred) / max(actual)).mean() * 100




def explained_variance(pred, actual):
    """The proportion of the variance explained by the prediction.

    Using equation 1 - RSS / TSS

    The best score is 1.0 and lower values are worse. It is possible that the
    score is negative, in which case the prediction variance is larger than that
    of the actual target.
    """

    pred = numpy.asarray(pred)
    actual = numpy.asarray(actual)

    RSS = sum((actual - pred)**2)
    TSS = actual.var()

    return 1 - RSS / TSS


def evaluate_regression(pred, actual):
    metrics = {
        'MAX'    : max_absolute_error(pred, actual),
        'MIN'    : min_absolute_error(pred, actual),
        'MAE'    : mean_absolute_error(pred, actual),
        'MSE'    : mean_squared_error(pred, actual),
        'RMSE'   : root_mean_squared_error(pred, actual),
        'MAPE'   : mean_absolute_percent_error(pred, actual),
        'MAPEFS' : mean_absolute_percent_error_full_scale(pred, actual),
        'Explained Variance': explained_variance(pred, actual),
    }

    df = pandas.DataFrame(results)

    return df
