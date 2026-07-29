"""
_powerlaw.py
============

Internal helper shared by all correlation functions. Implements the
generic power-law form Y = A * X^B (Eq. 1 in Verstraete, Palmer &
Hornung, 2017) over NumPy arrays.

This module contains no coefficient values -- A and B are always passed
in by the caller, sourced from the verified config file.
"""

from __future__ import annotations

import numpy as np


def evaluate_power_law(x, A: float, B: float) -> np.ndarray:
    """
    Evaluate Y = A * X^B elementwise.

    Parameters
    ----------
    x : array_like
        Independent variable values. Scalars are promoted to a 0-d
        array. Units are the caller's responsibility (not validated or
        converted here).
    A : float
        Power-law coefficient, verified against the source table.
    B : float
        Power-law exponent, verified against the source table.

    Returns
    -------
    np.ndarray
        Y values, same shape as ``x``.
    """
    x_arr = np.asarray(x, dtype=float)
    return A * np.power(x_arr, B)
    