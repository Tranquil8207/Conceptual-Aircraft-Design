"""
uav_sizing.correlations
========================

One function per Battery-class power-law relationship from Verstraete,
Palmer & Hornung (2017). All functions:

  * take/return NumPy arrays (scalars are auto-promoted via np.asarray),
  * implement Y = A * X^B directly (Eq. 1 in the source paper) -- no
    mean-ratio shortcuts, per project scope,
  * pull A/B/R2/p-value from the user-supplied, verified config file
    rather than hardcoding any numeric value,
  * raise MissingCoefficientError if the relevant config entry has not
    yet been filled in.

See the package README for the full table-to-function mapping and the
verification requirement before using any of these in real sizing work.
"""

from .mass import mgtom_from_payload, empty_mass_from_mgtom
from .mission import payload_endurance_product_from_mgtom
from .geometry import (
    wingspan_from_mgtom,
    wing_area_from_mgtom,
    wing_area_from_wingspan,
)
from .propulsion import installed_power_from_mgtom, power_index_from_mgtom

__all__ = [
    "mgtom_from_payload",
    "empty_mass_from_mgtom",
    "payload_endurance_product_from_mgtom",
    "wingspan_from_mgtom",
    "wing_area_from_mgtom",
    "wing_area_from_wingspan",
    "installed_power_from_mgtom",
    "power_index_from_mgtom",
]
