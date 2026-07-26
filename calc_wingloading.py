import math

def calc_WL(params,results):
    A1 = 1.15*3*(2/(params['rho_air']*params['clmax']))**0.5
    B1 = 1.3225/(params['g']*params['rho_air']*params['clmax']*params['RFC'])
    quad = (-A1 + (A1**2 + 4*B1*params['Ld'])**0.5)/(2*B1)
    WLmax = quad**2
    results['WLfinal'] = WLmax*0.80
