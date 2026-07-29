from inputs import get_inputs
from calc_wingloading import calc_WL
from calc_wingsizing import wingsizing
from calc_winggeometry import winggeometry
from calc_stabiliser_and_controlsurfacesizing import stabiliser_and_controlsurfacesizing
from calc_pmaxandTW import pmax,power_requirement
from calc_dprop import calc_dprop
from calc_weightestimation import weight_estimation
from VTOL_formulae.calc_TW_VTOL_and_helpers import TW_climb,Pmax_helpers
from VTOL_formulae.calc_pmax_VTOL import Preq_VTOL
from calc_optimalwingloading import ws_sweep_and_optimize

def process(x=None):
    """Run one full sizing convergence loop.

    x : optional [WS, span] design-vector override, N/m^2 and m.
        Used by optimize_design.py to evaluate an arbitrary design point
        instead of the built-in wing-loading heuristic / fixed max span.
        Leave as None for the original single-point behaviour.
    """
    params, results = get_inputs()
    helper = {}

    if x is not None:
        params = dict(params)   # don't mutate the shared defaults
        params['ms'] = x[1]
    results['WTO_guess'] = params['WTO']
    results['L_fuse'] = params['L_fuse_initial']
    results['a'] = params['a_initial']
    results['b'] = params['b_initial']
    calc_WL(params, results)
    if x is not None:
        results['WLfinal'] = x[0]   # optimizer-supplied wing loading overrides the heuristic
    max_iterations = 30
    change = 0.0075
    damping = 0.5
    damping_geo = 0.5
    delta = 1e-4
    for i in range(0, max_iterations, 1):
        wingsizing(params, results)
        winggeometry(params, results)
        if x is None:
            out = ws_sweep_and_optimize(params, results)
            results['constraint_diagram'] = out
            wingsizing(params, results)
            winggeometry(params, results)
        stabiliser_and_controlsurfacesizing(params, results)
        pmax(params, results)
        power_requirement(params, results)
        TW_climb(params, results, helper)
        Pmax_helpers(params, results, helper)
        Preq_VTOL(params, results, helper)
        calc_dprop(params, results)
        weight_estimation(params, results)

        results['W_payload'] = 1.000 * params['g']
        results['W_computed'] = results['W_computed'] + results['W_payload']

        W_computed = results['W_computed']
        W_guess = results['WTO_guess']
        delta = abs(W_computed - W_guess) / W_guess

        if delta <= change:
            break
        new_guess = W_guess + damping * (W_computed - W_guess)
        if new_guess > params['WTO_max']:
            new_guess = params['WTO_max']
        elif new_guess < params['WTO_min']:
            new_guess = params['WTO_min']
        results['WTO_guess'] = new_guess
    return results

if __name__ == '__main__':
    from report import main as print_report
    from sizematchingplot import plot_size_matching

    results = process()
    print_report(results=results)
    if 'constraint_diagram' in results:
        try:
            plot_size_matching(results['constraint_diagram'])
        except Exception as e:
            print(f'constraint diagram plot failed: {e}')
