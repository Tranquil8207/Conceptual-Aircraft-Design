def characteristic_velocities(params, results):
    import numpy as np
    from calc_pmaxandTW_helpers import calc_K
    k = calc_K(params, results)
    """
    Forward-flight characteristic velocities from the same parabolic drag
    model used by Eq. 2-52 and Eq. 3-1.
    """

    V_max_range = (
        np.sqrt(2.0 * results['W_computed'] / (params['rho_air'] * results['S_wing']))
        * (k / params['CD_min']) ** 0.25
    )

    V_max_endurance = (
        np.sqrt(2.0 * results['W_computed'] / (params['rho_air'] * results['S_wing']))
        * (k / (3.0 * params['CD_min'])) ** 0.25
    )

    V_opt_climb = results['V_climb']

    return {
        "V_max_range": V_max_range,
        "V_max_endurance": V_max_endurance,
        "V_opt_climb": V_opt_climb,
    }

def battery_params(params, results):
    E_battery_Wh = params['Vmax'] * params['Battery_capacity']
    E_battery_J = E_battery_Wh * 3600.0
    E_propulsion_J = E_battery_J * (1.0 - params['Avionics_reserve'])
    return E_propulsion_J

def drag_forward(params, results, V, W):
    import numpy as np
    from calc_pmaxandTW_helpers import calc_K
    k = calc_K(params, results)
    q = 0.5 * params['rho_air'] * np.asarray(V) ** 2
    TW = q * (params['CD_min'] / (W / results['S_wing'])) + (k / q) * (W / results['S_wing'])
    return TW * W

def power_forward(params, results, V, W):
    import numpy as np
    return drag_forward(params, results, V, W) * np.asarray(V) / params['eta_prop']

def range_forward(params, results, V, W):
    import numpy as np
    return battery_params(params, results) * np.asarray(V) / power_forward(params, results, V, W)

def endurance_forward(params, results, V, W):
    return battery_params(params, results) / power_forward(params, results, V, W)

def V_sweep(params):
    import numpy as np
    return np.linspace(params['V_stall'], params['V_cruise'], 500)

def plots_path(filename):
    from pathlib import Path
    from datetime import datetime
    folder = Path(__file__).resolve().parent / 'plots'
    folder.mkdir(exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    path = Path(filename)
    return str(folder / f'{path.stem}_{stamp}{path.suffix}')

def plot_all(params, results, show=False):
    import importlib
    specs = [
        ('constraint_diagram', 'plot_constraint_diagram'),
        ('drag_curve', 'plot_drag_curve'),
        ('power_curve', 'plot_power_curve'),
        ('power_vs_range', 'plot_power_vs_range'),
        ('range_vs_endurance', 'plot_range_vs_endurance'),
        ('velocity_vs_range', 'plot_velocity_vs_range'),
        ('velocity_vs_endurance', 'plot_velocity_vs_endurance'),
    ]
    for mod_name, fn_name in specs:
        getattr(importlib.import_module(mod_name), fn_name)(params, results, show=show)
