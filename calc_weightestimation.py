def weight_estimation(params, results):
    '''Sadraey formulae'''
    W_wing = results['S_wing']*results['C_wing_adj']*params['rho_mat']*params['k_rho_wing']*((params['TR'])**0.04)*params['g']*((results['AR_wing']*params['n_ult'])**0.6)*params['wing_thickness_factor']
    W_ht = results['S_ht']*results['C_ht']*params['rho_mat']*params['k_rho_ht']*((params['TR'])**0)*((params['Vht'])**0.3)*params['g']*params['stab_thickness_factor']*((params['AR_ht']*params['n_ult'])**0.6)*((results['C_elevator']/results['C_ht'])**0.4)
    W_vt = results['S_vt']*results['C_vt']*params['rho_mat']*params['k_rho_vt']*((params['TR'])**0)*((params['Vvt'])**0.2)*params['g']*params['stab_thickness_factor']*((params['AR_vt']*params['n_ult'])**0.6)*((results['C_rudder']/results['C_vt'])**0.4)
    W_fus = results['L_fuse']*params['rho_mat']*params['k_rho_fus']*params['g']*((params['n_ult'])**0.25)*(results['a']**2)
    W_LG = params['KL'] * params['K_ret'] * params['k_LG'] * results['WTO_guess'] * (params['L_LG'] / params['ms']) * (params['n_LG'] ** 0.20)
    '''Jae Hyun formulae
    W_motor = (-0.922*10**(-5))*(results['pmax']**2) + 0.196*(results['pmax']) + 23.342
    W_esc = (0.324*10**(-2))*results['esc_wt_coeff']**2 + 0.847*(results['esc_wt_coeff']) + 1.532
    W_prop = 670.644*(results['dprop'])**2.784'''

    '''Tyan Formulae'''
    p_ff = results.get('pmax', 0)
    if params.get('use_vtol'):
        p_vtol = results.get('Preq_VTOL', 0)
        nprop = params['n_prop_FF'] + params.get('n_prop_lift', 0)
        W_motor_FF = params['F1'] * (p_ff ** params['E1']) * (params['Vmax'] ** params['E2']) * p_ff * params['g'] * 0.001
        W_motor_lift = params['F1'] * (p_vtol ** params['E1']) * (params['Vmax'] ** params['E2']) * p_vtol * params['g'] * 0.001
        W_motor = W_motor_lift + W_motor_FF
        Pmax = max(p_ff, p_vtol)
    else:
        nprop = params['n_prop_FF']
        W_motor = params['F1'] * (p_ff ** params['E1']) * (params['Vmax'] ** params['E2']) * p_ff * params['g'] * 0.001
        W_motor_FF = W_motor
        W_motor_lift = 0.0
        Pmax = p_ff
    W_esc = params['F_esc'] * (Pmax ** params['E_esc']) * params['g'] * 0.001
    W_prop = (6.514e-3 * 1.0 * 15.0 * nprop * (params['n_blade']**0.391) * ((results['dprop'] * Pmax / (1000.0 * nprop)) ** 0.782)) * params['g'] * 0.001

    W_batt = params['W_batt_kg'] * params['g']
    W_ancilliary = params['W_ancillary_kg'] * params['g']

    '''Correction for underestimation of sadraey formulae'''
    W_wing = W_wing*1.45
    W_fus = W_fus*1.55
    W_ht = W_ht*1.75
    W_vt = W_vt*1.85

    W_structure = W_wing + W_ht + W_vt + W_fus + W_LG
    W_propulsion = W_motor + W_esc + W_prop
    W_empty = (W_structure + W_propulsion + W_batt + W_ancilliary) * params['build_factor']
    W_payload = params['payload_kg'] * params['g']

    results['W_wing'] = W_wing
    results['W_ht'] = W_ht
    results['W_vt'] = W_vt
    results['W_fus'] = W_fus
    results['W_LG'] = W_LG
    results['W_motor'] = W_motor
    results['W_motor_FF'] = W_motor_FF
    results['W_motor_lift'] = W_motor_lift
    results['W_esc'] = W_esc
    results['W_prop'] = W_prop
    results['W_batt'] = W_batt
    results['W_ancilliary'] = W_ancilliary
    results['W_structure'] = W_structure
    results['W_propulsion'] = W_propulsion
    results['W_empty'] = W_empty
    results['W_payload'] = W_payload
    results['W_computed'] = W_empty + W_payload
