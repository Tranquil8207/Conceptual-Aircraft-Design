import calc_pmaxandTW_helpers as helper

def pmax(params,results):
    helper.TW_takeoff(params,results)
    results['v_TO_stall'] = ((2*results['WLfinal'])/(params['rho_air']*params['clmax']))**0.5
    results['Vlo'] = 1.1*results['v_TO_stall']
    results['pmax_initial'] = (results['TW_takeoff']*0.7*results['Vlo']*results['WTO_guess'])/(params['eta_prop_ground'])
    results['esc_wt_coeff'] = results['pmax_initial']/params['Vmax']

    """Full flight-envelope thrust-to-weight and power sizing.

Adds the climb / cruise / service-ceiling / steady-turn segments on top
of the ground-roll takeoff sizing, then takes the governing (max power)
segment across the whole envelope.
Written as one function per flight segment, each taking wing loading
and aspect ratio explicitly rather than reading off a shared results
dict. power_requirement() at the bottom wires them together and is
what process.py actually calls.
  - TW_takeoff() -- takeoff power comes from the dto/Ld-based estimate.
  - SA_stall_limit() -- same equation, kept below as stall_limited_ws().
----------------------End of Maxon's changes-------------------------------
addendum(from anish) - spun off all the flight segment based TW calcs as a helper function
they can be found in calc_pmaxandTW_helpers, only the main powerrequirement function is
present here
second addendum(from anish) - merged calc_powerrequirement with calc_pmaxandTW
deprecated old TW calculation from calc_pmaxandTW - 1030pm 25/07/2026
"""

def power_requirement(params, results):

    k = helper.calc_K(params, results)

    """Call each segment function, convert T/W -> power (eq. 3-2), and
    pick the governing (max power) segment. Must run AFTER
    pmax() each iteration (uses its 'pmax' as takeoff power)."""
    WS = results['WLfinal']
    AR = results['AR_wing']

    results['WS_stall_limit'] = helper.stall_limited_ws(AR, params,k)

    tw_climb, V_climb = helper.TW_climb(WS, AR, params,k)
    tw_cruise = helper.TW_cruise(WS, AR, params,k)
    tw_ceiling = helper.TW_ceiling(AR, params, V_climb,k)
    tw_turn = helper.TW_turn(WS, AR, params,k)

    results['V_climb'] = V_climb
    results['TW_climb'] = tw_climb
    results['TW_cruise'] = tw_cruise
    results['TW_ceiling'] = tw_ceiling
    results['TW_turn'] = tw_turn

    # Power required per segment, eq. (3-2): P/W = (T/W * V) / eta_prop, we multiple P/W with W to get P alone
    Weight = results['WTO_guess']
    eta_prop = params['eta_prop']
    P_climb = tw_climb * Weight * V_climb / eta_prop
    P_cruise = tw_cruise * Weight * params['V_cruise'] / eta_prop
    P_ceiling = tw_ceiling * Weight * V_climb / eta_prop
    P_turn = tw_turn * Weight * params['V_cruise'] / eta_prop

    # Takeoff power already computed by pmax() from dto/Ld.
    P_takeoff = results['pmax_initial']

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
