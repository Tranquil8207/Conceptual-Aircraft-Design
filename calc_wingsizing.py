def wingsizing(params, results):
    results['S_wing'] = results['WTO_guess']/results['WLfinal']
    results['AR_wing'] = (params['ms']**2)/results['S_wing']
    if results['AR_wing'] > params['AR_max']:
        results['AR_wing'] = params['AR_max']
        results['ms'] = (results['AR_wing'] * results['S_wing'])**0.5
    else:
        results['ms'] = params['ms']
    results['C_wing'] = results['S_wing']/results['ms']
