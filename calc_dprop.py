def calc_dprop(params,results):
   '''
   Jae-hyun dprop formula
   kv = (-0.228*10**(-7))*((results['pmax'])**3) + 0.0003*(results['pmax'])**2 - 1.101*(results['pmax']) + 1685.676
   results['dprop'] = 4.735*(kv)**(-0.405)'''
   '''Tyan dprop formula - we run fixed dia props so ideally we will need to make this a constant?'''
   p_ff = results.get('pmax',0)
   p_vtol = results.get('Preq_VTOL',0)
   Pmax = max(p_ff,p_vtol)
   kp = 0.1072
   results['dprop'] = kp*(Pmax**0.25)
   