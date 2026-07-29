"""
config_loader.py
=================

Loads the Battery-class power-law coefficients used by
`uav_sizing.correlations`. Coefficients are never hardcoded in this
package -- they are read from an external JSON config file that the
user must populate and verify against the source paper (Verstraete,
Palmer & Hornung, 2017).

This module deliberately does NOT contain any numeric coefficient
values. Its only job is to load, validate, and hand off the config
dict/namedtuples that the correlation functions consume.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Default location of the placeholder/verified config file, relative to
# the repository root (config/battery_coefficients.json).
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "battery_coefficients.json"
)


@dataclass(frozen=True)
class PowerLawCoefficients:
    """
    Container for a single Y = A * X^B power-law fit (Eq. 1 in the source
    paper), plus the associated goodness-of-fit / hypothesis-test values
    reported in the paper's tables.

    Attributes
    ----------
    table : str
        Table number in the source paper this relationship is drawn from
        (structural reference only, e.g. "Table 4").
    relationship : str
        Human-readable form of the equation, e.g. "m_E = A * m_TO^B".
    A : float
        Power-law coefficient A. Must be supplied by the user.
    B : float
        Power-law exponent B. Must be supplied by the user.
    R2 : float, optional
        Coefficient of correlation reported for this fit, if available.
    p_value : float, optional
        p-value from the paper's t-test on the mean-ratio null hypothesis
        for this relationship, if available/relevant.
    """

    table: str
    relationship: str
    A: float
    B: float
    R2: Optional[float] = None
    p_value: Optional[float] = None


class MissingCoefficientError(ValueError):
    """Raised when a required coefficient has not been filled in yet."""


def _require_numeric(value, field_name: str, relationship_key: str):
    if value is None:
        raise MissingCoefficientError(
            f"Coefficient '{field_name}' for relationship "
            f"'{relationship_key}' is still a placeholder (null). "
            f"Fill in and verify this value against the source PDF "
            f"before calling this correlation."
        )
    return float(value)


def load_battery_coefficients(
    config_path: Optional[Path] = None,
) -> dict:
    """
    Load the Battery-class coefficient config file.

    Parameters
    ----------
    config_path : Path, optional
        Path to the JSON config file. Defaults to
        ``config/battery_coefficients.json`` in the repo root.

    Returns
    -------
    dict
        Raw parsed JSON dict, keyed by relationship name (e.g.
        "mgtom_from_payload", "wingspan_from_mgtom", ...). Each value is
        itself a dict with keys "table", "relationship", "x_units",
        "y_units", "A", "B", "R2", and (where applicable) a p-value
        field. Numeric fields may be ``None`` if not yet verified by the
        user -- callers should use ``get_coefficients`` to fetch a
        validated ``PowerLawCoefficients`` object that raises on
        unfilled placeholders.

    Notes
    -----
    This function performs no numeric validation itself; it only reads
    and parses JSON. Validation happens in ``get_coefficients``, which is
    called internally by each correlation function.
    """
    path = config_path or DEFAULT_CONFIG_PATH
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_coefficients(
    relationship_key: str,
    config: Optional[dict] = None,
    config_path: Optional[Path] = None,
    p_value_field: Optional[str] = None,
) -> PowerLawCoefficients:
    """
    Fetch and validate the coefficients for a single named relationship.

    Parameters
    ----------
    relationship_key : str
        Key into the config file, e.g. "wingspan_from_mgtom".
    config : dict, optional
        Pre-loaded config dict (as returned by ``load_battery_coefficients``).
        If not provided, the config is loaded from ``config_path`` (or the
        default path).
    config_path : Path, optional
        Only used if ``config`` is not provided.
    p_value_field : str, optional
        Name of the p-value field in the config entry to surface on the
        returned object (tables use different null-hypothesis p-value
        column names, e.g. "p_value_B0_equals_1" vs
        "p_value_B0_equals_7_over_6").

    Returns
    -------
    PowerLawCoefficients

    Raises
    ------
    MissingCoefficientError
        If A or B has not yet been filled in (still ``null`` in the
        config file).
    KeyError
        If ``relationship_key`` is not present in the config file.
    """
    if config is None:
        config = load_battery_coefficients(config_path)

    entry = config[relationship_key]

    A = _require_numeric(entry.get("A"), "A", relationship_key)
    B = _require_numeric(entry.get("B"), "B", relationship_key)
    R2 = entry.get("R2")
    p_value = entry.get(p_value_field) if p_value_field else None

    return PowerLawCoefficients(
        table=entry.get("table", "UNKNOWN"),
        relationship=entry.get("relationship", "UNKNOWN"),
        A=A,
        B=B,
        R2=R2,
        p_value=p_value,
    )
    