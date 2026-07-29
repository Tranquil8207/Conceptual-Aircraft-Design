import math


def get_inputs():
    params = {
        # Design variables/project specific inputs - leave empty if not used for comp
        'clmax'                 : 1.5*0.85,          # Clmax
        'WTO_max'               : 4.0*9.81,         # Max Takeoff weight guess (N)
        'WTO_min'               : 0*9.81,         # Min Takeoff weight guess (N)
        'RFC'                   : 0.03,         # Runway Friction Coefficient
        'Ld'                    : 121.92,         # Landing Distance (m)
        'WTO'                   : 4.0*9.81,         # Initial Takeoff weight guess (N)
        'ms'                    : 1.8288,       # Max Wingspan (m)
        'TR'                    : 0.4,          # Taper Ratio
        'a_initial'             : 0.17,         # Fuselage front face edge (m)
        'b_initial'             : 0.17,         # Fuselage rear face edge (m)
        'AR_ht'                 : 2.5,          # Horizontal tail Aspect Ratio
        'AR_vt'                 : 2.5,          # Vertical tail Aspect Ratio
        'rho_mat'               : 700,       # Density of structural material (kg/m³)
        'wing_thickness_factor' : 0.15,         # t/c (last two digits of NACA / 100)
        'stab_thickness_factor' : 0.12,         # t/c for stabilizers
        'L_fuse_initial'        : 1.0,         # Fuselage length (m)
        'Vmax'                  : 25.2,         # Max Battery voltage (V)
        'L_LG'                  : 0.15,         # Landing gear length (m)
        'dto'                   : 20,          # Takeoff distance (m)
        'n_blade'               : 2,           # Number of blades
        'n_prop_FF'             : 1,           # Number of propellers
        
        # Full flight-envelope power sizing (climb/cruise/ceiling/turn) --
        # placeholder values carried over from the MATLAB toolchain;
        # replace with real mission numbers once available.
        'V_stall'               : 10.0,             # Desired stall speed (m/s) [PLACEHOLDER]
        'V_cruise'              : 18.0,             # Cruise speed (m/s) [PLACEHOLDER]
        'climb_ROC'             : 3.0,              # Desired rate of climb (m/s) [PLACEHOLDER]
        'ROC_ceiling'           : 0.5,              # ROC at service ceiling (m/s) [PLACEHOLDER]
        'CD_min'                : 0.035,            # Min drag coeff, whole aircraft [PLACEHOLDER]
        'e'                     : 0.8,               # Oswald efficiency factor [PLACEHOLDER]
        'bank_angle'            : math.radians(30), # Design turn bank angle (rad) [PLACEHOLDER]
        'sweep_c4'              : 0.0,               # Quarter-chord sweep, rad (straight wing)
        'eta_prop'              : 0.75,             # Propeller efficiency, forward flight [PLACEHOLDER]
        
        # VTOL flight specific inputs
        'RoC_VTOL'              : 2.5,               # Rate of climb for VTOL operation (m/s)
        's_ratio'               : 1.3,              # Ratio of total aircraft surface area to wing area
        'n_prop_lift'           : 4,                # Number of lift props

        

        # Constants
        'k_rho_wing'            : 0.00125,
        'k_rho_ht'              : 0.0175,
        'k_rho_vt'              : 0.055,
        'k_rho_fus'             : 0.0020,
        'k_LG'                  : 0.45,
        'n_ult'                 : 2.625,
        'KL'                    : 1.0,
        'K_ret'                 : 1.0,
        'Vht'                   : 0.5000,
        'Vvt'                   : 0.0400,
        'n_LG'                  : 3.0,
        'g'                     : 9.81,
        'rho_air'               : 1.225,
        'eta_prop_ground'       : 0.65,
        'K_TO'                  : 0.015,
        'F1'                    : 0.889,
        'E1'                    : -0.288,
        'E2'                    : 0.1588,
        'F_esc'                 : 0.7383*(10**(-4)),
        'E_esc'                 : 0.8854,
        'FoM'                   : 0.7
    }
        
        

    results ={}
    return params, results


'''NOTES
Wing airfoil - NACA2415
Stab airfoils - NACA0012
C_tip_min_raw'         : ,           # Min chord length (unused input)
#SAE specific inputs
        'SAE_limit'             : 3.81,      # Greatest possible value of L+W+H of the aircraft (m)
'''
'''inputs'''
# clmax = float(input("Clmax = "))
# RFC = float(input("Runway Friction Coefficient = "))
# Ld = float(input("Landing Distance(m) = "))
# WTO = float(input("Takeoff weight(N) = "))
# ms = float(input("Max Wingspan(m) = "))
# TR = float(input("Taper Ratio = "))
# a = float(input("Fuselage front face edge length(m)(for square pyramidal fuselage) = "))
# b = float(input("Fuselage rear face edge length(m)(for square pyramidal fuselage)(should be <a) = "))
# AR_ht = float(input("Aspect Ratio of Horizontal Tail = "))
# AR_vt = float(input("Aspect Ratio of Vertical Tail = "))
# C_tip_min_raw = input("Minimum Tip Chord(m) (leave blank if not specified) = ")
# rho_mat = float(input("Density of chosen structural material (kg/m^3) = "))
# rho_mat_prop = float(input("Density of propellor material (kg/m^3) = "))
# wing_thickness_factor = float(input("Last 2 digits of the NACA number of the foil = "))/100
# stab_thickness_factor = float(input("Last 2 digits of the NACA number of the foil = "))/100
# L_fuse = float(input("Length of the fuselage(m) = "))
# dto = float(input("Takeoff distance = "))
# Vmax = float(input("Fully charged battery pack voltage(V) = "))
'''Set constant values -'''
# k_rho_wing = 0.00125
# k_rho_ht = 0.0175
# k_rho_vt = 0.055
# k_rho_fus = 0.0020
# k_LG = 0.45
# n_ult = 2.625
# KL = 1.0
# K_ret = 1.0
# Vht = 0.5000
# Vvt = 0.0400
# n_LG = 3.0
# g = 9.81
# rho_air = 1.225
# eta_prop_ground = 0.65
# F1 = 0.889
# E1 = -0.288
# E2 = 0.1588
# F_esc = 0.7383*(10**(-4))
# E_esc = 0.8854
