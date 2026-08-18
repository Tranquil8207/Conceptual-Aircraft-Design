import numpy as np
import calc_pmaxandTW_helpers as helper

#This part I had to look up. We're making an overall array here, to find out our best W/S. Technically our optimization code.
def ws_sweep(params, results):
    """Sweep wing loading and return T/W arrays for each flight segment.
    Call this AFTER wingsizing(params, results) has populated results['AR_wing']."""
    AR_wing = results['AR_wing']
    k = helper.calc_K(params, results)

def ws_sweep_and_optimize(params, results, WS_min=10, WS_max=200, n_points=500):
    AR_wing = results['AR_wing']
    k = helper.calc_K(params, results)

    WS_sweep = np.linspace(WS_min, WS_max, n_points)
    TW_takeoff_array = np.zeros_like(WS_sweep)
    TW_climb_array = np.zeros_like(WS_sweep)
    TW_cruise_array= np.zeros_like(WS_sweep)
    TW_ceiling_array = np.zeros_like(WS_sweep)
    TW_turn_array = np.zeros_like(WS_sweep)

    #Assume here we have a table where the entire first column is just the wing loading values, from 10 to 200, with 500 points in between (including decimals if any)
    for i, WS in enumerate(WS_sweep):
        results['WLfinal'] = WS
        helper.TW_takeoff(params, results)
        TW_takeoff_array[i] = results['TW_takeoff']

        tw_climb_val, V_climb = helper.TW_climb(WS, AR_wing, params, k)
        TW_climb_array[i] = tw_climb_val
        results['V_climb'] = V_climb

        TW_cruise_array[i] = helper.TW_cruise(WS, AR_wing, params, k)
        TW_ceiling_array[i] = helper.TW_ceiling(AR_wing, params, V_climb, k)
        TW_turn_array[i] = helper.TW_turn(WS, AR_wing, params, k)

    #Each of the Thrust to Weight v/s Wing Loading curves are added to a dictionary
    curves = {'Takeoff': TW_takeoff_array,'Climb': TW_climb_array,'Cruise': TW_cruise_array,'Ceiling': TW_ceiling_array,'Turn': TW_turn_array}

    #We select the maximum of all the Thrust to Weight v/s Wing Loading curves
    TW_envelope = np.max(np.vstack(list(curves.values())), axis=0)

    # Stall-speed cap on wing loading (not service-ceiling T/W).
    WS_ceiling = helper.stall_limited_ws(AR_wing, params, k)

    #As can be seen again, feasible MUST be lesser than stall cond
    feasible = WS_sweep <= WS_ceiling
    if not np.any(feasible):
        raise ValueError("No feasible W/S -- stall limit is below your sweep range.")

    #If all feasible, we're good to go, we add them to this array
    WS_feasible = WS_sweep[feasible]
    TW_feasible = TW_envelope[feasible]

    #Now we find the index of the minimum thrust to weight ratio
    min_index = np.argmin(TW_feasible)

    #And hence select the minimum thrust to weight ratio and wing loading value
    WS_opt = WS_feasible[min_index]
    TW_opt = TW_feasible[min_index]

    results['WS_opt'] = WS_opt
    results['TW_opt'] = TW_opt
    results['WLfinal'] = results['WS_opt']
    results['WS_sweep'] = WS_sweep
    results['TW_curves'] = curves
    results['TW_envelope'] = TW_envelope
    results['WS_stall_limit'] = WS_ceiling

    return {'WS_sweep': WS_sweep,'curves': curves,'TW_envelope': TW_envelope,'WS_ceiling': WS_ceiling,'WL_Final': WS_opt,'TW_opt': TW_opt}
