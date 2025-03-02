import numpy as np

def Get_Pressure_Coeff(Mach, inf_cst, P):
    """
    Calcule le coefficient de pression Cp en fonction du nombre de Mach et des conditions de l'écoulement.

    Paramètres :
    ------------
    Mach : float
        Nombre de Mach de l'écoulement.
    inf_cst : dict
        Dictionnaire contenant les constantes de l'écoulement :
        - "PRESSION" : Pression de l'écoulement libre (Pa).
        - "MASSE VOLUMIQUE" : Densité de l'écoulement libre (kg/m³).
        - "VITESSE" : Vitesse de l'écoulement libre (m/s).
        - "GAMMA" : Rapport des chaleurs spécifiques.
        - "S_REF" : Surface de référence (m²).
    P : float
        Pression locale (Pa).

    Retourne :
    ---------
    float :
        Coefficient de pression Cp.

    Remarque :
    ----------
    - Pour Mach < 0.3, l'expression classique de Cp est utilisée (formule incompressible).
    - Pour 0.3 ≤ Mach < 0.7, une correction par le facteur de Prandtl-Glauert est appliquée.
    - Pour 0.7 ≤ Mach < 1, la correction de Karman-Tsien est utilisée.
    - Pour Mach ≥ 1, l'expression classique de Cp est de nouveau valable.
    - En dehors de ces cas, la fonction retourne 0 par sécurité.
    """
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