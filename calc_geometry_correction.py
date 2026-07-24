def correct_geometry(params, results, damping_geo=0.5, sae_limit=3.81, length_pad=0.05, tol=1e-4):
    """Damped geometry correction: grow L_fuse first, then a/b under SAE L+W+H.

    Working geometry lives in results['L_fuse'], results['a'], results['b'].
    params['*_initial'] are left untouched as seeds.
    """
    L_fuse = results['L_fuse']
    a = results['a']
    b = results['b']
    l_tail = results['l_tail']
    ms = params['ms']

    # Step 1 — grow fuselage toward required tail arm
    if l_tail > L_fuse:
        L_fuse = L_fuse + damping_geo * (l_tail - L_fuse)

    # Step 2 — enforce SAE box at current height
    H = max(a, b)
    L_fuse_max = sae_limit - length_pad - ms - H
    if L_fuse_max < tol:
        L_fuse_max = tol
    if L_fuse > L_fuse_max:
        L_fuse = L_fuse_max

    results['L_fuse_max_sae'] = L_fuse_max

    # Step 3 — if tail still does not fit, grow a+b to shrink next l_tail
    # l_tail = sqrt(K / (a+b))  =>  target_sum = K / L_fuse^2 for l_tail ≈ L_fuse
    K = results['S_wing'] * (
        params['Vht'] * results['C_wing_adj'] + params['Vvt'] * params['ms']
    )

    if l_tail > L_fuse + tol and L_fuse > tol:
        target_sum = K / (L_fuse ** 2)
        current_sum = a + b
        if target_sum > current_sum:
            new_sum = current_sum + damping_geo * (target_sum - current_sum)
        else:
            new_sum = current_sum

        # Remaining height budget under SAE with current L_fuse
        max_H = sae_limit - length_pad - ms - L_fuse
        if max_H < tol:
            max_H = tol

        # Preserve a:b ratio (square if equal); enforce b <= a
        if a + b > 0:
            ratio_a = a / (a + b)
            ratio_b = b / (a + b)
        else:
            ratio_a = 0.5
            ratio_b = 0.5

        a_new = new_sum * ratio_a
        b_new = new_sum * ratio_b

        # Cap so max(a,b) <= max_H
        peak = max(a_new, b_new)
        if peak > max_H:
            scale = max_H / peak
            a_new *= scale
            b_new *= scale

        # Enforce b <= a
        if b_new > a_new:
            a_new, b_new = b_new, a_new

        a, b = a_new, b_new

        # Recompute implied l_tail at new a+b for feasibility flag
        if a + b > 0:
            l_tail_implied = (K / (a + b)) ** 0.5
        else:
            l_tail_implied = float('inf')
    else:
        l_tail_implied = l_tail

    results['L_fuse'] = L_fuse
    results['a'] = a
    results['b'] = b

    # Feasibility: can current working geometry host l_tail under SAE?
    H = max(a, b)
    LHW = (L_fuse + length_pad) + ms + H
    tail_ok = l_tail_implied <= L_fuse + tol
    sae_ok = LHW <= sae_limit + tol
    results['geometry_feasible'] = tail_ok and sae_ok
