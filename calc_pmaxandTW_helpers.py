'''This is where the helper functions for the powerrequirements calcs live'''
import math

def calc_K(params,results):
    k = 1 / (math.pi * params['e'] * results['AR_wing'])
    return k


def stall_limited_ws(AR_wing, params,k):
    """Upper bound on wing loading from stall speed -- eq. (2-55).
    Feed back as an optimizer constraint (WS <= this), not applied here."""
    CL_max_3D = 0.9 * params['clmax'] * math.cos(params['sweep_c4'])
    stall_limited_WL = 0.5 * params['rho_air'] * params['V_stall'] ** 2 * CL_max_3D
    return stall_limited_WL

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