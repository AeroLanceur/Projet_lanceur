import numpy as np

def Get_Pressure_Coeff(Mach, inf_cst, P):

    P_inf = inf_cst["PRESSION"]
    rho_inf = inf_cst["MASSE VOLUMIQUE"]
    v_inf = inf_cst["VITESSE"]
    gamma = inf_cst["GAMMA"]
    S_ref = inf_cst["S_REF"]

    if Mach < 0.3:
        Cp = (P - P_inf) / (0.5 * rho_inf * v_inf**2)
        return Cp
    
    elif 0.3 <= Mach and Mach < 0.7:
        beta = np.sqrt(1 - Mach**2)
        Cp_inc = (P - P_inf) / (0.5 * rho_inf * v_inf**2)
        return Cp_inc / beta
    
    elif 0.7 <= Mach and Mach < 1:
        beta = np.sqrt(1 - Mach**2)
        Cp_inc = (P - P_inf) / (0.5 * rho_inf * v_inf**2)
        return Cp_inc / (beta + (Mach**2 * Cp_inc)/(2*(1 + beta)))
    
    elif 1 <= Mach:

        return (P - P_inf) / (0.5 * rho_inf * v_inf**2)
    
    else:
        return 0