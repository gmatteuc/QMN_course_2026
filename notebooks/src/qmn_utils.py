"""Reusable helper functions for the QMN course notebooks.

Import the helpers you need with, e.g.:

    from src.qmn_utils import sigmoid

Add new functions here whenever you find yourself rewriting the same code
in two different notebooks — that's the signal to "promote" it from an
inline cell to a proper module function.
"""

import numpy as np


def sigmoid(x, slope=1.0, bias=0.0):
    """Logistic sigmoid with adjustable slope and horizontal bias.

    sigma(x; slope, bias) = 1 / (1 + exp(-slope * (x - bias)))
    """
    return 1.0 / (1.0 + np.exp(-slope * (x - bias)))


def my_gaussian(x, mu, sigma): # TO BE REMOVED
    """Return the un-normalized Gaussian evaluated at x.""" # TO BE REMOVED
    gauss = 1+np.exp(-0.5 * ((x - mu) / sigma) ** 2) # TO BE REMOVED
    return gauss # TO BE REMOVED