"""Search wing loading (WS) & wingspan to minimize MTOW.

Python port of MATLAB's objective_function.m + optimize_design.m +
rca_constraints.m. MATLAB searches x = [W_S, AR_wing]; here x = [WS, span]
instead, since this codebase treats wingspan (not AR) as the first-class
competition-limited variable that AR is derived from
(AR_wing = span**2 / S_wing, per calc_wingsizing.py).

Each objective/constraint evaluation re-runs the full convergence loop
for that design point (process(x=...)) -- this mirrors how MATLAB's
rca_constraints.m calls run_conceptual_design(req, x, refData) fresh on
every call. It's more function evaluations than a cached approach, but
keeps this a faithful, simple port; revisit if the optimizer is slow.
"""

from scipy.optimize import minimize

from process import process
from calc_wingloading import calc_WL
from inputs import get_inputs

G = 9.81

# --- SAE DDC RCA rulebook bounds ---
WINGSPAN_MAX = 72 * 0.0254        # m (72 in)
MTOW_MIN_N = 2.0 * G              # N (payload excluded, per define_requirements.m)
MTOW_MAX_N = 4.0 * G              # N

# Landing-distance-feasible wing loading ceiling (independent of span) --
# this is the same quantity calc_WL.py's 0.80 heuristic is 80% of. Kept
# here as an extra constraint so the optimizer can't pick a WS that would
# violate your landing-distance requirement; MATLAB's rca_constraints.m
# doesn't have this check (it has no landing-distance module), so this is
# a Python-side addition, not a strict port.
_params0, _results0 = get_inputs()
calc_WL(_params0, _results0)
WL_LANDING_MAX = _results0['WLfinal'] / 0.80

# Search bounds -- tune to your actual feasible range
WS_BOUNDS = (10.0, WL_LANDING_MAX)
SPAN_BOUNDS = (0.6, WINGSPAN_MAX)


def _evaluate(x):
    """Run one converged design point for x = [WS, span]."""
    return process(x=list(x))


def _converged(results):
    w_guess = results.get('WTO_guess')
    w_computed = results.get('W_computed')
    if not w_guess or w_computed is None:
        return False
    delta = abs(w_computed - w_guess) / w_guess
    tail_ok = (results.get('l_tail', 1e9) - results.get('L_fuse', 0)) <= 1e-4
    return delta <= 0.0075 and tail_ok and results.get('sae_ok', False)


def objective(x):
    """Scalar objective for the optimizer: minimize MTOW (kg)."""
    results = _evaluate(x)
    w_computed = results.get('W_computed')
    if w_computed is None:
        return 1e6  # sizing failed outright for this x

    J = w_computed / G  # kg
    if not _converged(results):
        # Penalize non-convergence heavily rather than trusting a
        # misleading number -- mirrors objective_function.m.
        J += 1000.0
    return J


def constraint_wingspan(x):
    return WINGSPAN_MAX - x[1]                       # span <= 72 in


def constraint_ws_landing(x):
    return WL_LANDING_MAX - x[0]                     # WS <= landing-distance limit


def constraint_sae_box(x):
    return _evaluate(x).get('remaining_space', -1.0)  # L+W+H <= SAE box


def constraint_mtow_max(x):
    return MTOW_MAX_N - _evaluate(x).get('W_computed', 1e9)


def constraint_mtow_min(x):
    return _evaluate(x).get('W_computed', 0.0) - MTOW_MIN_N


def constraint_stall_ws(x):
    return _evaluate(x).get('WS_stall_limit', 0.0) - x[0]  # WS <= stall-limited WS


def optimize_design(x0=None):
    if x0 is None:
        x0 = [WL_LANDING_MAX * 0.80, WINGSPAN_MAX]  # today's heuristic, as a starting guess

    constraints = [
        {'type': 'ineq', 'fun': constraint_wingspan},
        {'type': 'ineq', 'fun': constraint_ws_landing},
        {'type': 'ineq', 'fun': constraint_sae_box},
        {'type': 'ineq', 'fun': constraint_mtow_max},
        {'type': 'ineq', 'fun': constraint_mtow_min},
        {'type': 'ineq', 'fun': constraint_stall_ws},
    ]

    result = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=[WS_BOUNDS, SPAN_BOUNDS],
        constraints=constraints,
        options={'maxiter': 100, 'ftol': 1e-6},
    )

    x_opt = list(result.x)
    design_opt = process(x=x_opt)
    return x_opt, design_opt, result


if __name__ == '__main__':
    x_opt, design_opt, result = optimize_design()
    print(f"Optimizer: {result.message}  (success={result.success})")
    print(f"x_opt -> WS = {x_opt[0]:.3f} N/m^2, span = {x_opt[1]:.4f} m")
    print(f"Converged MTOW = {design_opt['W_computed']/G:.3f} kg")
    print(f"AR_wing = {design_opt['AR_wing']:.3f}")
    print(f"Governing power case = {design_opt.get('governing_case')}, "
          f"pmax = {design_opt.get('pmax'):.2f}")
