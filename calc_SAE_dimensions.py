def SAE_dimensions(params,results, sae_limit=3.81, length_pad=0.05, tol=1e-4):
    results['adjusted_L'] = results['L_fuse'] + length_pad
    results['forward_fuse_L'] = results['adjusted_L'] - results['l_tail']
    results['ac_W'] = params['ms']
    results['ac_H'] = max(results['a'], results['b'])
    results['LHW_total'] = results['adjusted_L'] + results['ac_W'] + results['ac_H']

    condition = sae_limit
    results['sae_ok'] = results['LHW_total'] <= condition + tol
    if results['LHW_total'] > condition:
        excess = results['LHW_total'] - condition
        results['remaining_space'] = -excess
    elif results['LHW_total'] < condition:
        results['remaining_space'] = condition - results['LHW_total']
    else:
        results['remaining_space'] = 0.0
