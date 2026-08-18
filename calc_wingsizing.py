def wingsizing(params, results):
    results['S_wing'] = results['WTO_guess']/results['WLfinal']
    results['AR_wing'] = (params['ms']**2)/results['S_wing']
    results['C_wing'] = results['S_wing']/params['ms']
