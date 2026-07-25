"""
Addendum(from anish - 25/07/2026)
This also completely dead code
I completed the migration of all these functions into calc_pmaxandTW
Until Maxon gives me his go ahead ill keep it here though


Full flight-envelope thrust-to-weight and power sizing.

Adds the climb / cruise / service-ceiling / steady-turn segments on top
of the existing ground-roll takeoff sizing in calc_pmaxandTW.py, then
takes the governing (max power) segment across the whole envelope.

Written as one function per flight segment (matching the standalone
per-segment style pulled from the MATLAB conversion), each taking wing
loading and aspect ratio explicitly rather than reading off a shared
results dict. power_requirement() at the bottom wires them together and
is what process.py actually calls.
addendum(from anish) - spun off all the flight segment based TW calcs as a helper function
they can be found in calc_pmaxandTW_helpers, only the main powerrequirement function is
present here
second addendum(from anish) - merged calc_powerrequirement with calc_pmaxandTW
deprecated old TW calculation from calc_pmaxandTW - 1030pm 25/07/2026
Two things from that MATLAB conversion are intentionally NOT here:
  - TW_takeoff() / a Gudmundsson placeholder takeoff formula -- takeoff
    power already comes from calc_pmaxandTW.py's dto/Ld-based estimate,
    which uses your real competition takeoff/landing distances.
  - SA_stall_limit() -- same equation, kept below as stall_limited_ws().


import math
import calc_pmaxandTW_helpers as helper

def power_requirement(params, results):
    Call each segment function, convert T/W -> power (eq. 3-2), and
    pick the governing (max power) segment. Must run AFTER
    calc_pmaxandTW() each iteration (uses its 'pmax' as takeoff power).
    
    WS = results['WLfinal']
    AR = results['AR_wing']

    results['WS_stall_limit'] = helper.stall_limited_ws(AR, params)

    tw_climb, V_climb = helper.TW_climb(WS, AR, params)
    tw_cruise = helper.TW_cruise(WS, AR, params)
    tw_ceiling = helper.TW_ceiling(AR, params, V_climb)
    tw_turn = helper.TW_turn(WS, AR, params)

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

    # Takeoff power already computed by calc_pmaxandTW.py from real dto/Ld data.
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
    results['pmax'] = segments[governing_case] """
