def calc_WL(params,results):
    A1 = 1.15*3*(2/(params['rho_air']*params['clmax']))**0.5
    B1 = 1.3225/(params['g']*params['rho_air']*params['clmax']*params['RFC'])
    quad = (-A1 + (A1**2 + 4*B1*params['Ld'])**0.5)/(2*B1)
    WLmax = quad**2
    results['WLfinal'] = WLmax*0.80

#New constraints

def SA_stall_limit(W_S, params):
    # Oswald-based induced drag factor, eq. (3-4)
    k = 1 / (math.pi * params['e'] * params['AR_wing'])
    
    # 3D CLmax from 2D airfoil value and sweep, eq. (3-8)
    CL_max_3D = 0.9 * params['Cl_max'] * math.cos(params['sweep_c4'])
    
    # Stall-limited wing loading -- an UPPER BOUND on W_S, not the design
    # point. Feed this back as a nonlinear constraint in the optimizer:
    #   W_S <= WS_stall_limit
    WS_stall_limit = 0.5 * params['rho_air'] * params['V_stall']**2 * CL_max_3D
    
    return WS_stall_limit

def TW_takeoff(W_S, params):
    # Take-off, eq. (2-50)
    V_To = params['V_To_factor'] * params['V_stall']
    q_To = 0.5 * params['rho_air'] * V_To**2
    TW_takeoff = V_To**2 / (2 * params['g'] * params['S_g']) + (q_To * params['CD_To']) / W_S \
               + params['mu_ground'] * (1 - (q_To * params['CL_To']) / W_S)
    
    return TW_takeoff

def TW_climb(W_S, params):
    # Climb, eq. (3-1) for V_climb, then eq. (2-51)
    k = 1 / (math.pi * params['e'] * params['AR_wing'])
    V_climb = math.sqrt((2 / params['rho_air']) * W_S * math.sqrt(k / (3 * params['CD_min'])))
    q_climb = 0.5 * params['rho_air'] * V_climb**2
    TW_climb = params['V_climb_ROC'] / V_climb + (q_climb / W_S) * params['CD_min'] + (k / q_climb) * W_S
    
    return TW_climb

def TW_cruise(W_S, params):
    # Cruise, eq. (2-52)
    q_cruise = 0.5 * params['rho_air'] * params['V_cruise']**2
    TW_cruise = q_cruise * (params['CD_min'] / W_S) + (k / q_cruise) * W_S
    
    return TW_cruise

def TW_ceiling(W_S, params):
    # Service ceiling, eq. (2-53)
    k = 1 / (math.pi * params['e'] * params['AR_wing'])
    TW_ceiling = params['ROC_ceiling'] / math.sqrt((2 / params['rho_air']) * W_S * math.sqrt(k / (3 * params['CD_min']))) \
               + 4 * math.sqrt(k * params['CD_min'] / 3)
    
    return TW_ceiling

def TW_turn(W_S, params):
    # Steady turn, eq. (2-54), (3-7)
    k = 1 / (math.pi * params['e'] * params['AR_wing'])
    n_turn = 1 / math.cos(params['bank_angle'])
    q_turn = 0.5 * params['rho_air'] * params['V_cruise']**2   # turn performed at cruise speed
    TW_turn = q_turn * (params['CD_min'] / W_S + k * (n_turn / q_turn)**2 * W_S)
    
    return TW_turn
