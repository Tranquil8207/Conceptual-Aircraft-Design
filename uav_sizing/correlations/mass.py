"""
mass.py
=======

Mass-related power-law correlations for battery-powered UAVs, from
Verstraete, Palmer & Hornung (2017).
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

import numpy as np

from ..config_loader import get_coefficients
from ._powerlaw import evaluate_power_law


def mgtom_from_payload(
    payload_mass,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate Maximum Gross Takeoff Mass (MGTOM) from payload mass.

    Implements the Battery-row power-law fit of Table 2:
        m_TO = A * m_PL^B
    (Eq. 1 applied to the payload-mass / MGTOM dataset described in
    Sec. III.A.1 of the source paper.)

    Parameters
    ----------
    payload_mass : array_like
        Payload mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated MGTOM, kg.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 2 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "mgtom_from_payload",
        config=config,
        config_path=config_path,
        p_value_field="p_value_B0_equals_1",
    )
    return evaluate_power_law(payload_mass, coeffs.A, coeffs.B)


def empty_mass_from_mgtom(
    mgtom,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate empty (airframe) mass from MGTOM.

    Implements the Battery-row power-law fit of Table 4:
        m_E = A * m_TO^B
    (Sec. III.B.1 of the source paper.)

    Parameters
    ----------
    mgtom : array_like
        Maximum Gross Takeoff Mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated empty mass, kg.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 4 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "empty_mass_from_mgtom",
        config=config,
        config_path=config_path,
        p_value_field="p_value_B0_equals_1",
    )
    return evaluate_power_law(mgtom, coeffs.A, coeffs.B)
    