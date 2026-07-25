"""Full flight-envelope thrust-to-weight and power sizing.

Adds the climb / cruise / service-ceiling / steady-turn segments on top
of the existing ground-roll takeoff sizing in calc_pmaxandTW.py, then
takes the governing (max power) segment across the whole envelope.

Written as one function per flight segment (matching the standalone
per-segment style pulled from the MATLAB conversion), each taking wing
loading and aspect ratio explicitly rather than reading off a shared
results dict. power_requirement() at the bottom wires them together and
is what process.py actually calls.

Two things from that MATLAB conversion are intentionally NOT here:
  - TW_takeoff() / a Gudmundsson placeholder takeoff formula -- takeoff
    power already comes from calc_pmaxandTW.py's dto/Ld-based estimate,
    which uses your real competition takeoff/landing distances.
  - SA_stall_limit() -- same equation, kept below as stall_limited_ws().
"""

import math


def stall_limited_ws(AR_wing, params):
    """Upper bound on wing loading from stall speed -- eq. (2-55).
    Feed back as an optimizer constraint (WS <= this), not applied here."""
    k = 1 / (math.pi * params['e'] * AR_wing)
    CL_max_3D = 0.9 * params['clmax'] * math.cos(params['sweep_c4'])
    return 0.5 * params['rho_air'] * params['V_stall'] ** 2 * CL_max_3D


def TW_climb(W_S, AR_wing, params):
    """Climb, eq. (3-1) for V_climb, then eq. (2-51)."""
    k = 1 / (math.pi * params['e'] * AR_wing)
    V_climb = math.sqrt((2 / params['rho_air']) * W_S * math.sqrt(k / (3 * params['CD_min'])))
    q_climb = 0.5 * params['rho_air'] * V_climb ** 2
    tw = (params['climb_ROC'] / V_climb
          + (q_climb / W_S) * params['CD_min']
          + (k / q_climb) * W_S)
    return tw, V_climb


def TW_cruise(W_S, AR_wing, params):
    """Cruise, eq. (2-52)."""
    k = 1 / (math.pi * params['e'] * AR_wing)  # <- this line was missing in the uploaded conversion
    q_cruise = 0.5 * params['rho_air'] * params['V_cruise'] ** 2
    return q_cruise * (params['CD_min'] / W_S) + (k / q_cruise) * W_S


def TW_ceiling(AR_wing, params, V_climb):
    """Service ceiling, eq. (2-53). Reuses V_climb from TW_climb() rather
    than recomputing it, since it's the same quantity."""
    k = 1 / (math.pi * params['e'] * AR_wing)
    return params['ROC_ceiling'] / V_climb + 4 * math.sqrt(k * params['CD_min'] / 3)


def TW_turn(W_S, AR_wing, params):
    """Steady turn, eq. (2-54), (3-7). Performed at cruise speed."""
    k = 1 / (math.pi * params['e'] * AR_wing)
    n_turn = 1 / math.cos(params['bank_angle'])
    q_turn = 0.5 * params['rho_air'] * params['V_cruise'] ** 2
    return q_turn * (params['CD_min'] / W_S + k * (n_turn / q_turn) ** 2 * W_S)


def power_requirement(params, results):
    """Call each segment function, convert T/W -> power (eq. 3-2), and
    pick the governing (max power) segment. Must run AFTER
    calc_pmaxandTW() each iteration (uses its 'pmax' as takeoff power)."""
    WS = results['WLfinal']
    AR = results['AR_wing']

    results['WS_stall_limit'] = stall_limited_ws(AR, params)

    tw_climb, V_climb = TW_climb(WS, AR, params)
    tw_cruise = TW_cruise(WS, AR, params)
    tw_ceiling = TW_ceiling(AR, params, V_climb)
    tw_turn = TW_turn(WS, AR, params)

    results['V_climb'] = V_climb
    results['TW_climb'] = tw_climb
    results['TW_cruise'] = tw_cruise
    results['TW_ceiling'] = tw_ceiling
    results['TW_turn'] = tw_turn

    # Power required per segment, eq. (3-2): P/W = (T/W * V) / eta_prop
    W_To_N = results['WTO_guess']
    eta_prop = params['eta_prop']
    P_climb = tw_climb * W_To_N * V_climb / eta_prop
    P_cruise = tw_cruise * W_To_N * params['V_cruise'] / eta_prop
    P_ceiling = tw_ceiling * W_To_N * V_climb / eta_prop
    P_turn = tw_turn * W_To_N * params['V_cruise'] / eta_prop

    # Takeoff power already computed by calc_pmaxandTW.py from real
    # dto/Ld data -- reuse it rather than a Gudmundsson placeholder formula.
    P_takeoff = results['pmax']

    segments = {
        'takeoff': P_takeoff,
        'climb': P_climb,
        'cruise': P_cruise,
        'ceiling': P_ceiling,
        'turn': P_turn,
    }
    governing_case = max(segments, key=segments.get)

    results['P_takeoff'] = P_takeoff
    results['P_climb'] = P_climb
    results['P_cruise'] = P_cruise
    results['P_ceiling'] = P_ceiling
    results['P_turn'] = P_turn
    results['governing_case'] = governing_case

    # Overwrite pmax with the envelope-governing value so downstream
    # modules (calc_dprop, calc_weightestimation) size off the worst case.
    results['pmax'] = segments[governing_case]
