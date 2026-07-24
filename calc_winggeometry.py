def winggeometry(params,results):
    results['C_root'] = (2*results['S_wing'])/(params['ms']*(1+params['TR']))
    results['C_tip'] = results['C_root']*params['TR']
    results['C_wing_adj'] = (2/3)*results['C_root']*((1+params['TR']+(params['TR']**2))/(1+params['TR']))
