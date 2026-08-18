def correct_geometry(params, results):
    damping = 0.5
    length_pad = 0.05
    delta = 1e-4
    sae_limit = params['SAE_limit']
    L_fuse = results['L_fuse']
    a = results['a']
    b = results['b']
    l_tail = results['l_tail']
    ms = params['ms']
    H = max(a,b) + params['L_LG'] + results['span_ht']
    L_fuse_max = sae_limit - length_pad - ms - H

    if l_tail > L_fuse:
        L_fuse = L_fuse + damping*(l_tail - L_fuse)
    if L_fuse_max < delta:
        raise Exception("Aircraft geometry is not possible")
    if L_fuse > L_fuse_max:
        L_fuse = L_fuse_max

    results['L_fuse_max_sae'] = L_fuse_max

    K = results['S_wing'] * (params['Vht'] * results['C_wing_adj'] + params['Vvt'] * params['ms'])

    if l_tail > L_fuse + delta and L_fuse > delta:
        target_sum = K / (L_fuse ** 2)
        current_sum = a + b
        if target_sum > current_sum:
            new_sum = current_sum + damping * (target_sum - current_sum)
        else:
            new_sum = current_sum

        max_H = sae_limit - length_pad - ms - L_fuse
        if max_H < delta:
            raise Exception("Aircraft geometry is not possible")

        ratio_a = a / (a + b)
        ratio_b = b / (a + b)

        a_new = new_sum * ratio_a
        b_new = new_sum * ratio_b

        peak = max(a_new, b_new)
        if peak > max_H:
            scale = max_H / peak
            a_new *= scale
            b_new *= scale

        if b_new > a_new:
            a_new, b_new = b_new, a_new

        a, b = a_new, b_new

        if a + b > 0:
            l_tail_new = (K / (a + b)) ** 0.5
        else:
            l_tail_new = float('inf')
    else:
        l_tail_new = l_tail

    results['L_fuse'] = L_fuse
    results['a'] = a
    results['b'] = b

    H = max(a, b)
    LHW = (L_fuse + length_pad) + ms + H
    
    if l_tail_new <= L_fuse + delta:
        tail_check = True
    else:
        tail_check = False
    
    if LHW <= sae_limit + delta:
        sae_check = True
    else:
        sae_check = False
    
    results['geometry_feasible'] = tail_check == True and sae_check == True
