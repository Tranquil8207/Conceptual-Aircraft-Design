"""
uav_sizing
==========

Preliminary sizing correlations for battery-powered fixed-wing UAVs,
scaffolded from the power-law relationships in:

    Verstraete, D., Palmer, J. L., and Hornung, M., "Preliminary Sizing
    Correlations for Fixed-Wing Unmanned Aerial Vehicle Characteristics,"
    Journal of Aircraft, 2017, DOI: 10.2514/1.C034199

IMPORTANT: This package ships with a placeholder coefficient config
(config/battery_coefficients.json) that contains no numeric values.
You must fill it in yourself with coefficients verified directly against
the source PDF before any function in `uav_sizing.correlations` will
produce real numbers. See the README for details.
"""

from .config_loader import load_battery_coefficients

__all__ = ["load_battery_coefficients"]
