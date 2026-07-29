"""
propulsion.py
=============

Engine/motor power-law correlations for battery-powered UAVs, from
Verstraete, Palmer & Hornung (2017).
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

import numpy as np

from ..config_loader import get_coefficients
from ._powerlaw import evaluate_power_law


def installed_power_from_mgtom(
    mgtom,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate installed engine/motor power from MGTOM.

    Implements the Battery-row power-law fit of Table 8:
        P = A * m_TO^B
    (Sec. III.C of the source paper.)

    Parameters
    ----------
    mgtom : array_like
        Maximum Gross Takeoff Mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated installed power, W.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 8 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "installed_power_from_mgtom",
        config=config,
        config_path=config_path,
        p_value_field="p_value_B0_equals_1",
    )
    return evaluate_power_law(mgtom, coeffs.A, coeffs.B)


def power_index_from_mgtom(
    mgtom,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate the power index (PI) from MGTOM.

    Implements the Battery-row power-law fit of Table 9:
        PI = A * m_TO^B
    where PI = b^2 * (m_TO / b^2)^(3/2) (Eq. 6), correlated against
    installed power via Eq. 7 for the overall population. (Sec. III.C of
    the source paper.)

    Parameters
    ----------
    mgtom : array_like
        Maximum Gross Takeoff Mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated power index, kg^(3/2)/m.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 9 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "power_index_from_mgtom",
        config=config,
        config_path=config_path,
        p_value_field="p_value_B0_equals_7_over_6",
    )
    return evaluate_power_law(mgtom, coeffs.A, coeffs.B)
    