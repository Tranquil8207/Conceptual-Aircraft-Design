def calc_dprop(params,results):
   '''
   Jae-hyun dprop formula
   kv = (-0.228*10**(-7))*((results['pmax'])**3) + 0.0003*(results['pmax'])**2 - 1.101*(results['pmax']) + 1685.676
   results['dprop'] = 4.735*(kv)**(-0.405)'''
   '''Tyan dprop formula - we run fixed dia props so ideally we will need to make this a constant?'''
   kp = 0.1072
   results['dprop'] = kp*((results['pmax'])**0.25)
   