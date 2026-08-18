from inputs import get_inputs
from calc_wingloading import calc_WL
from calc_wingsizing import wingsizing
from calc_winggeometry import winggeometry
from calc_stabiliser_and_controlsurfacesizing import stabiliser_and_controlsurfacesizing
from calc_pmaxandTW import pmax, power_requirement
from calc_dprop import calc_dprop
from calc_weightestimation import weight_estimation
from calc_optimalwingloading import ws_sweep_and_optimize


def process():
    """Free-sizing loop: wing, geometry, tails, FF power/T/W, dprop, weight, damped WTO."""
    params, results = get_inputs()
    results['WTO_guess'] = params['WTO']
    results['L_fuse'] = params['L_fuse_initial']
    results['a'] = params['a_initial']
    results['b'] = params['b_initial']
    calc_WL(params, results)
    max_iterations = 30
    change = 0.0075
    damping = 0.5
    delta = 1.0
    for i in range(0, max_iterations, 1):
        wingsizing(params, results)
        winggeometry(params, results)
        ws_sweep_and_optimize(params, results)
        wingsizing(params, results)
        winggeometry(params, results)
        stabiliser_and_controlsurfacesizing(params, results)
        pmax(params, results)
        power_requirement(params, results)
        if params.get('use_vtol'):
            from VTOL_formulae.calc_TW_VTOL_and_helpers import TW_climb, Pmax_helpers
            from VTOL_formulae.calc_pmax_VTOL import Preq_VTOL
            helper = {}
            TW_climb(params, results, helper)
            Pmax_helpers(params, results, helper)
            Preq_VTOL(params, results, helper)
        calc_dprop(params, results)
        weight_estimation(params, results)

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

    results['iterations'] = i + 1
    results['weight_residual'] = delta
    results['weight_ok'] = delta <= change
    return results


if __name__ == '__main__':
    from report import main as print_report

    results = process()
    print_report(results=results)
