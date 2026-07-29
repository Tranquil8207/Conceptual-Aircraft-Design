# uav-sizing

Preliminary sizing correlations for **battery-powered fixed-wing UAVs**,
scaffolded from the empirical power-law relationships in:

> Verstraete, D., Palmer, J. L., and Hornung, M., "Preliminary Sizing
> Correlations for Fixed-Wing Unmanned Aerial Vehicle Characteristics,"
> *Journal of Aircraft*, 2017. DOI: [10.2514/1.C034199](https://doi.org/10.2514/1.C034199)

This package is scoped to the **Battery** propulsion class only (no
multi-class selector). It is scaffolding: function signatures, config
schema, and structure are complete, but **no numeric coefficients are
included**. You must supply and verify them yourself.

## ⚠️ Before you use this for anything

`config/battery_coefficients.json` ships with every `A`, `B`, `R2`, and
`p_value` field set to `null`. Every correlation function will raise
`MissingCoefficientError` until you:

1. Open the source PDF and locate the **Battery** row of the relevant
   table.
2. Transcribe `A`, `B`, and (where present) `R2` / the p-value column
   into the config file yourself.
3. Double check the transcription — table columns are easy to
   mis-align, and this package intentionally does not pre-fill or
   sanity-check these values for you.

No coefficient, equation number, `R2`, or p-value in this repository
was filled in from memory. All numeric fields are your responsibility.

## Table → function mapping

| Function | Source table | Relationship |
|---|---|---|
| `mgtom_from_payload` | Table 2 | `m_TO = A * m_PL^B` |
| `payload_endurance_product_from_mgtom` | Table 3 | `[m_PL * E] = A * m_TO^B` |
| `empty_mass_from_mgtom` | Table 4 | `m_E = A * m_TO^B` |
| `wingspan_from_mgtom` | Table 5 | `b = A * m_TO^B` |
| `wing_area_from_mgtom` | Table 6 | `S_W = A * m_TO^B` |
| `wing_area_from_wingspan` | Table 7 | `S_W = A * b^B` |
| `installed_power_from_mgtom` | Table 8 | `P = A * m_TO^B` |
| `power_index_from_mgtom` | Table 9 | `PI = A * m_TO^B` |

All relationships implement the paper's general power-law form
`Y = A * X^B` (Eq. 1), fit directly per the Battery-row regression
coefficients — **not** the paper's mean-ratio shortcuts (`B≈1`,
`B≈2/3`, `B≈7/6`). The paper itself notes that for several tables, the
Battery-class p-values do not support the mean-ratio assumption, so the
power-law fit is used unconditionally here. If you later decide a
mean-ratio fallback is appropriate for a specific parameter (after
checking the relevant p-value yourself), that would be a deliberate
addition on top of this scaffolding — it is not implemented by default.

## Package layout

```
uav_sizing/
├── config_loader.py          # loads + validates the coefficient config
└── correlations/
    ├── _powerlaw.py           # shared Y = A * X^B evaluator (no coefficients)
    ├── mass.py                 # Table 2, Table 4
    ├── mission.py               # Table 3
    ├── geometry.py               # Table 5, 6, 7
    └── propulsion.py              # Table 8, 9

config/
└── battery_coefficients.json  # <-- fill this in and verify against the PDF

tests/
├── fixture_coefficients.json  # arbitrary A=1,B=1 values, for plumbing tests only
└── test_correlations.py       # structural tests, no numeric-accuracy assertions
```

## Usage

```python
import numpy as np
from uav_sizing import correlations

mgtom = np.array([1.0, 2.0, 5.0, 10.0])  # kg

# Raises MissingCoefficientError until config/battery_coefficients.json
# has verified Battery-row values filled in for Table 5.
wingspan = correlations.wingspan_from_mgtom(mgtom)
```

To point at a different config file (e.g. while testing):

```python
from pathlib import Path
wingspan = correlations.wingspan_from_mgtom(
    mgtom, config_path=Path("path/to/my_coefficients.json")
)
```

## Units

This package does **no unit conversion or validation**. All inputs and
outputs are in whatever units the source table specifies (see the table
above and the docstrings), and it is the caller's responsibility to
ensure consistency — matching the "units already handled on my end"
convention used by the rest of this project's pipeline.

## Dependencies

NumPy + Python standard library only.

## Testing

```
pip install -e ".[dev]"  # or just: pip install -e . pytest
pytest
```

Current tests are structural only (array plumbing, config loading,
error handling on unfilled placeholders). Once you've verified real
coefficients, add numeric regression tests separately (e.g. against a
known reference aircraft or a hand calculation) — do not just delete
the placeholder-config tests, since they guard against someone
accidentally shipping unverified numbers.