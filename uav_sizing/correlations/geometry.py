"""
geometry.py
===========

Geometric power-law correlations for battery-powered UAVs, from
Verstraete, Palmer & Hornung (2017).
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

import numpy as np

from ..config_loader import get_coefficients
from ._powerlaw import evaluate_power_law


def wingspan_from_mgtom(
    mgtom,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate wingspan from MGTOM.

    Implements the Battery-row power-law fit of Table 5:
        b = A * m_TO^B
    (Sec. III.B.2 of the source paper.)

    Parameters
    ----------
    mgtom : array_like
        Maximum Gross Takeoff Mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated wingspan, m.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 5 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "wingspan_from_mgtom",
        config=config,
        config_path=config_path,
    )
    return evaluate_power_law(mgtom, coeffs.A, coeffs.B)


def wing_area_from_mgtom(
    mgtom,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate wing area from MGTOM.

    Implements the Battery-row power-law fit of Table 6:
        S_W = A * m_TO^B
    (Sec. III.B.3 of the source paper.)

    Parameters
    ----------
    mgtom : array_like
        Maximum Gross Takeoff Mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated wing area, m^2.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 6 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "wing_area_from_mgtom",
        config=config,
        config_path=config_path,
    )
    return evaluate_power_law(mgtom, coeffs.A, coeffs.B)


def wing_area_from_wingspan(
    wingspan,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate wing area from wingspan.

    Implements the Battery-row power-law fit of Table 7:
        S_W = A * b^B
    (Sec. III.B.3 of the source paper, Eq. 4 for the overall-population
    version of this relationship.)

    Parameters
    ----------
    wingspan : array_like
        Wingspan, m.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated wing area, m^2.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 7 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "wing_area_from_wingspan",
        config=config,
        config_path=config_path,
    )
    return evaluate_power_law(wingspan, coeffs.A, coeffs.B)
    