def SAE_dimensions(params,results):
    length_pad = 0.05
    delta = 1e-4
    results['adjusted_L'] = results['L_fuse'] + length_pad
    results['forward_fuse_L'] = results['adjusted_L'] - results['l_tail']
    results['ac_W'] = params['ms']
    results['ac_H'] = max(results['a'], results['b'])
    results['LHW_total'] = results['adjusted_L'] + results['ac_W'] + results['ac_H']

    sae_limit = params['SAE_limit']
    results['sae_ok'] = results['LHW_total'] <= sae_limit + delta
    if results['LHW_total'] > sae_limit:
        excess = results['LHW_total'] - sae_limit
        results['remaining_space'] = -excess
    elif results['LHW_total'] < sae_limit:
        results['remaining_space'] = sae_limit - results['LHW_total']
    else:
        results['remaining_space'] = 0.0
