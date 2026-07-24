def weight_estimation(params,results):
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
    W_motor = params['F1'] * (results['pmax'] ** params['E1']) * (params['Vmax'] ** params['E2']) * results['pmax'] * params['g'] * 0.001
    W_esc = params['F_esc'] * (results['pmax'] ** params['E_esc']) * params['g'] * 0.001
    W_prop = (6.514e-3 * 1.0 * 15.0 * params['n_prop'] * (params['n_blade']**0.391) * ((results['dprop'] * results['pmax'] / (1000.0 * params['n_prop'])) ** 0.782)) * params['g'] * 0.001
    '''Battery weight'''
    W_batt = 0.500*9.81
    
    '''Ancilliary component weight'''
    W_ancilliary = 0.500*9.81

    '''Correction for underestimation of sadraey formulae'''
    W_wing = W_wing*1.45
    W_fus = W_fus*1.55
    W_ht = W_ht*1.75
    W_vt = W_vt*1.85

    '''Total weight adjusted with a build factor'''
    results['W_computed'] = (W_wing + W_ht + W_vt + W_fus + W_LG + W_motor + W_esc + W_prop + W_batt + W_ancilliary)*1.20
