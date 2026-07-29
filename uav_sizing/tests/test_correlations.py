"""
test_correlations.py
=====================

Scaffolding tests only. These verify:
  * the config loader reads JSON and raises on unfilled placeholders,
  * each correlation function accepts NumPy arrays and returns arrays
    of the correct shape,
  * each function correctly raises MissingCoefficientError against the
    shipped (placeholder) config.

These are NOT numeric-accuracy tests -- there are no real assertions
against known correct sizing outputs, because the shipped config has no
verified coefficients yet. Once you populate and verify
config/battery_coefficients.json, add real regression-style assertions
(e.g. against known reference aircraft or hand calculations) separately.

A local fixture file (fixture_coefficients.json) with arbitrary
A=1.0, B=1.0 placeholder values is used to exercise the array-handling
plumbing without pretending those values are real.
"""

from pathlib import Path

import numpy as np
import pytest

from uav_sizing.config_loader import (
    load_battery_coefficients,
    get_coefficients,
    MissingCoefficientError,
    DEFAULT_CONFIG_PATH,
)
from uav_sizing import correlations

FIXTURE_PATH = Path(__file__).parent / "fixture_coefficients.json"

ALL_FUNCS_AND_KEYS = [
    (correlations.mgtom_from_payload, "mgtom_from_payload"),
    (correlations.payload_endurance_product_from_mgtom, "payload_endurance_product_from_mgtom"),
    (correlations.empty_mass_from_mgtom, "empty_mass_from_mgtom"),
    (correlations.wingspan_from_mgtom, "wingspan_from_mgtom"),
    (correlations.wing_area_from_mgtom, "wing_area_from_mgtom"),
    (correlations.wing_area_from_wingspan, "wing_area_from_wingspan"),
    (correlations.installed_power_from_mgtom, "installed_power_from_mgtom"),
    (correlations.power_index_from_mgtom, "power_index_from_mgtom"),
]


def test_default_config_file_loads_and_parses():
    """The shipped placeholder config file must be valid JSON."""
    config = load_battery_coefficients(DEFAULT_CONFIG_PATH)
    assert "mgtom_from_payload" in config
    assert "power_index_from_mgtom" in config


@pytest.mark.parametrize("func,key", ALL_FUNCS_AND_KEYS)
def test_shipped_placeholder_config_raises_missing_coefficient(func, key):
    """
    Every function must refuse to run against the unfilled shipped
    config, since A/B are still null placeholders.
    """
    with pytest.raises(MissingCoefficientError):
        func(np.array([1.0, 2.0, 3.0]))


@pytest.mark.parametrize("func,key", ALL_FUNCS_AND_KEYS)
def test_function_accepts_array_and_returns_array_with_fixture_config(func, key):
    """
    Using the arbitrary (A=1.0, B=1.0) test fixture, confirm each
    function correctly plumbs a NumPy array through evaluate_power_law
    and returns an array of matching shape. Not a numeric-accuracy test.
    """
    fixture_config = load_battery_coefficients(FIXTURE_PATH)
    x = np.array([1.0, 2.0, 4.0, 10.0])
    y = func(x, config=fixture_config)

    assert isinstance(y, np.ndarray)
    assert y.shape == x.shape
    # With A=1.0, B=1.0 the fixture reduces to the identity function.
    np.testing.assert_allclose(y, x)


@pytest.mark.parametrize("func,key", ALL_FUNCS_AND_KEYS)
def test_function_accepts_scalar_input(func, key):
    """Scalars should be promoted to 0-d arrays without error."""
    fixture_config = load_battery_coefficients(FIXTURE_PATH)
    y = func(5.0, config=fixture_config)
    assert isinstance(y, np.ndarray)


def test_get_coefficients_raises_on_unknown_key():
    fixture_config = load_battery_coefficients(FIXTURE_PATH)
    with pytest.raises(KeyError):
        get_coefficients("not_a_real_relationship", config=fixture_config)