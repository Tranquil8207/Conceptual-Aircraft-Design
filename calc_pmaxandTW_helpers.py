'''This is where the helper functions for the powerrequirements calcs live'''
import math
import numpy as np
#We calculate drag factor 
def calc_K(params,results):
    k = 1 / (math.pi * params['e'] * results['AR_wing'])
    return k

#We calculate stall limited wing loading using stall speed as the parameter
def stall_limited_ws(AR_wing, params,k):
    """Upper bound on wing loading from stall speed -- eq. (2-55).
    Feed back as an optimizer constraint (WS <= this), not applied here."""
    CL_max_3D = 0.9 * params['clmax'] * math.cos(params['sweep_c4'])
    stall_limited_WL = 0.5 * params['rho_air'] * params['V_stall'] ** 2 * CL_max_3D
    return stall_limited_WL

#Here we're considering our various situations of flight, of sorts. Take-off, climb etc., you name it.
def TW_takeoff(params,results):
    results['TW_takeoff'] = (1.21*results['WLfinal'])/(params['g']*params['rho_air']*params['clmax']*params['dto'])

def TW_climb(W_S, AR_wing, params,k):
    """Climb, eq. (3-1) for V_climb, then eq. (2-51)."""
    V_climb = math.sqrt((2 / params['rho_air']) * W_S * math.sqrt(k / (3 * params['CD_min'])))
    q_climb = 0.5 * params['rho_air'] * V_climb ** 2
    TW_climb = (params['climb_ROC'] / V_climb + (q_climb / W_S) * params['CD_min'] + (k / q_climb) * W_S)
    return TW_climb, V_climb

def TW_cruise(W_S, AR_wing, params,k):
    """Cruise, eq. (2-52)."""
    q_cruise = 0.5 * params['rho_air'] * params['V_cruise'] ** 2
    TW_cruise = q_cruise * (params['CD_min'] / W_S) + (k / q_cruise) * W_S
    return TW_cruise

def TW_ceiling(AR_wing, params, V_climb,k):
    """Service ceiling, eq. (2-53). Reuses V_climb from TW_climb() rather
    than recomputing it, since it's the same quantity."""
    TW_ceiling = params['ROC_ceiling'] / V_climb + 4 * math.sqrt(k * params['CD_min'] / 3)
    return TW_ceiling

def TW_turn(W_S, AR_wing, params,k):
    """Steady turn, eq. (2-54), (3-7). Performed at cruise speed."""
    n_turn = 1 / math.cos(params['bank_angle'])
    q_turn = 0.5 * params['rho_air'] * params['V_cruise'] ** 2
    TW_turn = q_turn * (params['CD_min'] / W_S + k * (n_turn / q_turn) ** 2 * W_S)
    return TW_turn

#This part I had to look up. We're making an overall array here, to find out our best W/S. Technically our optimization code.
def ws_sweep(params, results):
    """Sweep wing loading and return T/W arrays for each flight segment.
    Call this AFTER wingsizing(params, results) has populated results['AR_wing']."""
    AR_wing = results['AR_wing']
    k = calc_K(params, results)

def ws_sweep_and_optimize(params, results, WS_min=10, WS_max=200, n_points=500):
    AR_wing = results['AR_wing']
    k = calc_K(params, results)
    #This part below is needed as this is our original Wing Loading. Like, the Python file one from calc_wingloading.py
    WLfinal_actual = results.get('WLfinal')

    WS_sweep = np.linspace(WS_min, WS_max, n_points)
    TW_takeoff_array = np.zeros_like(WS_sweep)
    TW_climb_array = np.zeros_like(WS_sweep)
    TW_cruise_array= np.zeros_like(WS_sweep)
    TW_ceiling_array = np.zeros_like(WS_sweep)
    TW_turn_array = np.zeros_like(WS_sweep)
    #Assume here we have a table where the entire first column is just the wing loading values, from 10 to 200, with 500 points in between. Decimals.
    for i, WS in enumerate(WS_sweep):
        results['WLfinal'] = WS
        TW_takeoff(params, results)
        TW_takeoff_array[i] = results['TW_takeoff']

        tw_climb_val, V_climb = TW_climb(WS, AR_wing, params, k)
        TW_climb_array[i] = tw_climb_val

        TW_cruise_array[i] = TW_cruise(WS, AR_wing, params, k)
        TW_ceiling_array[i] = TW_ceiling(AR_wing, params, V_climb, k)
        TW_turn_array[i] = TW_turn(WS, AR_wing, params, k)
    #We're done with array, now we bring back our original W/S
    if WLfinal_actual is not None:
        results['WLfinal'] = WLfinal_actual
    #Each of the Thrust to Weight v/s Wing Loading curves are added to a dictionary
    curves = {'Takeoff': TW_takeoff_array,'Climb': TW_climb_array,'Cruise': TW_cruise_array,'Ceiling': TW_ceiling_array,'Turn': TW_turn_array}
    #We select the maximum of all the Thrust to Weight v/s Wing Loading curves
    TW_envelope = np.max(np.vstack(list(curves.values())), axis=0)
    #And constraint it by our maximum stall thrust to weight.
    WS_max_stall = stall_limited_ws(AR_wing, params, k)
    WS_ceiling = WS_max_stall

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
    #We finally call our obtained values
    return {'WS_max_stall': WS_max_stall,'WL_Final': WS_opt,'TW_opt': TW_opt}
    #Below code is the generated one. I think most of these are pure clutter so I commented it off. Take if you'd need. 
    #return {'WS_sweep': WS_sweep,'curves': curves,'TW_envelope': TW_envelope,'WS_max_stall': WS_max_stall,'WL_Final': WS_opt,'TW_opt': TW_opt}
    