from inputs import get_inputs
import math

'''main tyan TW climb calculation for VTOL operation'''
def TW_climb(params,results,helper):
    K = 1+((params['RoC_VTOL']**2)*params['rho_air']*params['s_ratio'])/results['WLfinal']
    TW_climb = 1.2*K
    results['TW_climb_VTOL'] = TW_climb

'''Helper function for tyan Pmax in VTOL operation calculation'''
def Pmax_helpers(params,results,helper):

    results['Hover_thrust'] = results['WTO_guess']
    helper['T_single_rotor'] = results['Hover_thrust']/params['n_prop_lift']

    Tclimb = results['TW_climb_VTOL']*results['WTO_guess']
    helper['Treqmax'] = max(Tclimb,results['Hover_thrust'])

    helper['DL'] = 3.261*(results['WTO_guess']/params['g']) + 74.991
    helper['S_rotor_single'] = helper['Treqmax']/(helper['DL']*params['n_prop_lift'])
    helper['vh'] = math.sqrt(helper['T_single_rotor']/(2*params['rho_air']*helper['S_rotor_single']))
    
    vi_root = math.sqrt(((1/2*params['RoC_VTOL'])**2) + (helper['vh']**2))
    vi_real = 1/2*params['RoC_VTOL']
    helper['vi'] = vi_root - vi_real