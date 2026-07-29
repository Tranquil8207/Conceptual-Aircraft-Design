"""
mission.py
==========

Mission-capability power-law correlations for battery-powered UAVs, from
Verstraete, Palmer & Hornung (2017).
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

import numpy as np

from ..config_loader import get_coefficients
from ._powerlaw import evaluate_power_law


def payload_endurance_product_from_mgtom(
    mgtom,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
) -> np.ndarray:
    """
    Estimate the payload-mass x endurance product from MGTOM.

    Implements the Battery-row power-law fit of Table 3:
        [m_PL * E] = A * m_TO^B
    (Sec. III.A.2 of the source paper.) Note this returns the *product*
    of payload mass (kg) and endurance (h) -- splitting it into
    individual payload/endurance values requires an additional
    assumption not provided by this fit alone.

    Parameters
    ----------
    mgtom : array_like
        Maximum Gross Takeoff Mass, kg.
    config, config_path : see uav_sizing.config_loader.get_coefficients

    Returns
    -------
    np.ndarray
        Estimated payload-mass x endurance product, kg*h.

    Raises
    ------
    MissingCoefficientError
        If the Battery-row A/B for Table 3 have not yet been filled in
        and verified in the config file.
    """
    coeffs = get_coefficients(
        "payload_endurance_product_from_mgtom",
        config=config,
        config_path=config_path,
    )
    return evaluate_power_law(mgtom, coeffs.A, coeffs.B)
    