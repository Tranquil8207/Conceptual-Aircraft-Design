import math


def get_inputs():
    params = {
        # --- seed / loop ---
        'WTO'                   : 4.0*9.81,         # Initial takeoff-weight guess (N)
        'WTO_min'               : 2.0*9.81,              # Optional weight loop floor (N)
        'WTO_max'               : 4.0*9.81,        # Optional weight loop ceiling (N)
        'payload_kg'            : 1.0,              # Design payload (kg), will not optimise this further, it will only use this hardcoded
        'build_factor'          : 1.10,              # Optional empty-weight multiplier for further corrections (default 1.0)

        # --- wing / aero ---
        'clmax'                 : 2.5*0.85,         # 3D-adjusted CLmax
        'ms'                    : 1.8288,           # Max wingspan (m)
        'AR_max'                : 9.0,              # Aspect-ratio cap; span is reduced if b^2/S would exceed this
        'TR'                    : 0.4,              # Wing taper ratio
        'CD_min'                : 0.035,            # Parasite drag coefficient
        'e'                     : 0.8,              # Oswald efficiency
        'V_stall'               : 10.0,             # Stall-speed target (m/s)
        'V_cruise'              : 18.0,             # Cruise speed (m/s)
        'dto'                   : 60.0,             # Takeoff ground roll (m)
        'RFC'                   : 0.03,             # Runway friction coefficient
        'Ld'                    : 90.0,             # Landing distance (m)
        'climb_ROC'             : 3.0,              # Desired climb rate (m/s)
        'ROC_ceiling'           : 0.5,              # ROC at service ceiling (m/s)
        'bank_angle'            : math.radians(45), # Design turn bank angle (rad)
        'sweep_c4'              : 0.0,              # Quarter-chord sweep (rad)
        'eta_prop'              : 0.75,             # Propeller efficiency, forward flight
        'eta_prop_ground'       : 0.65,             # Propeller efficiency during ground roll

        # --- fuselage / tails (geometry seed) ---
        'a_initial'             : 0.17,             # Fuselage front-face edge (m)
        'b_initial'             : 0.17,             # Fuselage rear-face edge (m)
        'L_fuse_initial'        : 1.0,              # Fuselage length seed (m)
        'AR_ht'                 : 2.5,              # Horizontal-tail aspect ratio
        'AR_vt'                 : 2.5,              # Vertical-tail aspect ratio
        'Vht'                   : 0.5000,           # HT volume coefficient
        'Vvt'                   : 0.0400,           # VT volume coefficient

        # --- structure (Sadraey k_rho / LG) ---
        'rho_mat'               : 700,              # Structural material density (kg/m^3)
        'wing_thickness_factor' : 0.143,             # Wing t/c
        'stab_thickness_factor' : 0.12,             # Stabilizer t/c
        'k_rho_wing'            : 0.00125,          # Wing mass coefficient
        'k_rho_ht'              : 0.0175,           # HT mass coefficient
        'k_rho_vt'              : 0.055,            # VT mass coefficient
        'k_rho_fus'             : 0.0020,           # Fuselage mass coefficient
        'k_LG'                  : 0.45,             # Landing-gear mass coefficient
        'n_ult'                 : 2.625,            # Ultimate load factor
        'KL'                    : 1.0,              # LG layout factor
        'K_ret'                 : 1.0,              # LG retract factor
        'L_LG'                  : 0.15,             # Landing-gear length (m)
        'n_LG'                  : 3.0,              # Landing-gear load factor

        # --- propulsion (Tyan) ---
        'n_prop_FF'             : 1,                # Forward-flight propeller count
        'n_blade'               : 2,                # Blades per propeller
        'Vmax'                  : 18.5,             # Pack voltage used in Tyan motor mass (V)
        'F1'                    : 0.889,            # Tyan motor mass coefficient
        'E1'                    : -0.288,           # Tyan motor mass exponent on P
        'E2'                    : 0.1588,           # Tyan motor mass exponent on V
        'F_esc'                 : 0.7383*(10**(-4)),# Tyan ESC mass coefficient
        'E_esc'                 : 0.8854,           # Tyan ESC mass exponent
        'Battery_capacity'      : 2200/1000,        # Battery Capacity in Ah (converted inline from MAh)
        'Avionics_reserve'      : 0.20,             # Percentage of battery power reserved for hotel load (mainly avionics but could be anything else)

        # --- battery and ancilliary weights (mainly used to hardcode battery weight) ---
        'W_batt_kg'             : 0.282,            # Battery mass (kg)
        'W_ancillary_kg'        : 0.500,            # Ancillary weight (used to account for weights not directly estimated in the formulae we use) (kg)

        # --- optional modules (default unused / off) ---
        'use_vtol'              : False,            # If True, run VTOL_formulae and size lift plant
        'n_prop_lift'           : 4,                # Lift props; used only if use_vtol is True
        'RoC_VTOL'              : 2.5,              # VTOL climb rate (m/s); used only if use_vtol is True
        's_ratio'               : 1.3,              # Airframe/wing area ratio; used only if use_vtol is True
        'FoM'                   : 0.7,              # Rotor figure of merit; used only if use_vtol is True

        # --- constants ---
        'g'                     : 9.81,             # Acceleration due to gravity (m/s^2)
        'rho_air'               : 1.225,            # Sea-level air density (kg/m^3)

        # ---SAE specific---
        'SAE_limit'             : 0 ,               # SAE specific L+W+H constraint
    }

    results = {}
    return params, results


'''NOTES
Wing airfoil seed - Eppler 420
Stab airfoils seed - NACA0012
'''
