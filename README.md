# Conceptual Aircraft Design

Free-sizing toolchain: Poelma-style weight loop, Sadraey structure, Tyan propulsion mass.

Edit `inputs.py`, then run:

```
python process.py
```

`inputs.py` is a single hardcoded `params` dict. The loop in `process.py` sizes the wing, geometry, tails, forward-flight power / T/W, propeller diameter, and analytical empty weight, then damps `WTO` until `|W_computed - WTO_guess| / WTO_guess` closes. After the first wing size, `calc_optimalwingloading.py` picks `WLfinal` from the envelope sweep and the wing is resized; there is no constraint-diagram plot.

Optional: VTOL formulae (`use_vtol`, default off) add lift-plant power and Tyan lift-motor mass.

Dependencies: `numpy`, `tabulate`.
