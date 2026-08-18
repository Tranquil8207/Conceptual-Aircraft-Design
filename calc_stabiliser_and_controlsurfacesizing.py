def stabiliser_and_controlsurfacesizing(params, results):
    delta = 1e-4
    if results['b']>results['a']:
        raise Exception("b must be smaller than a")
    root = (results['S_wing'])*((params['Vht']*results['C_wing_adj'])+(params['Vvt']*results['ms']))/(results['a']+results['b'])
    results['l_tail'] = root**0.5
    results['tail_length_excess'] = results['l_tail'] - results['L_fuse']
    results['tail_fit_ok'] = results['tail_length_excess'] <= delta
    results['S_ht'] = params['Vht']*results['S_wing']*results['C_wing_adj']/results['l_tail']
    results['S_vt'] = params['Vvt']*results['S_wing']*results['ms']/results['l_tail']
    results['span_ht'] = (params['AR_ht']*results['S_ht'])**0.5
    results['span_vt'] = (params['AR_vt']*results['S_vt'])**0.5
    results['C_ht'] = results['S_ht']/results['span_ht']
    results['C_vt'] = results['S_vt']/results['span_vt']
    results['S_aileron'] = 0.075*results['S_wing']
    results['S_elevator'] = 0.275*results['S_ht']
    results['S_rudder'] = 0.25*results['S_vt']
    results['C_aileron'] = 0.225*results['C_wing_adj']
    results['C_elevator'] = 0.30*results['C_ht']
    results['C_rudder'] = 0.275*results['C_vt']
