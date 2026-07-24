def pmax_and_TW(params,results):
    results['TW'] = (1.21*results['WLfinal'])/(params['g']*params['rho_air']*params['clmax']*params['dto'])
    results['v_TO_stall'] = ((2*results['WLfinal'])/(params['rho_air']*params['clmax']))**0.5
    results['Vlo'] = 1.1*results['v_TO_stall']
    results['pmax'] = (results['TW']*0.7*results['Vlo']*results['WTO_guess'])/(params['eta_prop_ground'])
    results['esc_wt_coeff'] = results['pmax']/params['Vmax']