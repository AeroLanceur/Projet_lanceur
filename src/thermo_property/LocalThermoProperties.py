import numpy as np
from thermo_property.AfterShocProperties import AfterShock_var
from shock_management.Expansion import PrandtlMeyer, inv_PrandtlMeyer, solve_mach_from_nu
from shock_management.Oblique import Get_ShockAngle_Vectorized, Correct_Beta_Vector
from scipy.optimize import newton
from thermo_property.GammaManagement import calculate_gamma_rarefied

from scipy.optimize import root_scalar

def Shock_Growth_S(M, n=2, k=0.1):
    """
    Fonction de croissance du choc S(M) utilisée dans le modèle de croissance du choc (Shock Growth Model).

    Cette fonction modélise la transition entre l'écoulement subsonique et supersonique 
    en utilisant une loi de croissance continue.

    Paramètres :
    ------------
    M : float
        Nombre de Mach local.
    n : int, optionnel (par défaut = 2)
        Exposant contrôlant la rapidité de la transition.
    k : float, optionnel (par défaut = 0.1)
        Facteur de lissage pour éviter les discontinuités brutales.

    Retourne :
    ----------
    S_M : float
        Facteur de croissance du choc.

    Remarque :
    ----------
    - Cette fonction est utilisée pour interpoler entre les régimes subsonique et supersonique 
      dans le modèle de croissance du choc.
    """
    return ((M - 1)**n) / ((M - 1)**n + k)

def Get_Local_Params(inf_cst, Mach, Velocity, deviation_angle, basic_gamma):
    """
    Calcule les paramètres locaux thermodynamiques en fonction du régime d'écoulement.

    Cette fonction estime la pression, la température et la masse volumique locales en fonction 
    du nombre de Mach, de la vitesse locale et de l'angle de déviation.

    Paramètres :
    ------------
    inf_cst : dict
        Dictionnaire des conditions d'écoulement libre (pression, température, masse volumique).
    Mach : dict
        Contient :
        - "MACH_INF" : Nombre de Mach de l'écoulement libre.
        - "MACH_LOCAL" : Nombre de Mach local après prise en compte de la déviation.
    Velocity : dict
        Contient :
        - "V_INF" : Vitesse de l'écoulement libre.
        - "V_LOCAL" : Vitesse locale après prise en compte de l'angle effectif.
    deviation_angle : array-like
        Angles de déviation locaux en radians.
    basic_gamma : float
        Valeur de \(\gamma\) utilisée pour un écoulement standard.

    Retourne :
    ----------
    local_params : dict
        Contient :
        - "PRESSION" : Pression locale en Pascal.
        - "TEMPERATURE" : Température locale en Kelvin.
        - "MASSE VOLUMIQUE" : Masse volumique locale en kg/m³.

    Remarque :
    ----------
    - Le modèle de calcul dépend du régime de Mach :
      - Pour Mach < 0.3 : Écoulement subsonique incompressible (hypothèse de Bernoulli).
      - Pour 0.3 ≤ Mach < 1 : Écoulement subsonique compressible (formules isentropiques).
      - Pour 1 ≤ Mach < 1.2 : Interpolation entre régime subsonique et supersonique avec Shock Growth Model.
      - Pour Mach ≥ 1.2 :
        - Méthode des chocs obliques si l'angle de déviation est positif.
        - Méthode de Prandtl-Meyer si l'angle de déviation est négatif (zone d'expansion).

    - Dans le régime supersonique/hypersonique, la fonction appelle d'autres sous-fonctions :
      - `Get_ShockAngle_Vectorized` pour obtenir l'angle de choc.
      - `AfterShock_var` pour déterminer les conditions après le choc.
      - `PrandtlMeyer` pour calculer l'expansion si nécessaire.
    - Une gestion des erreurs est incluse pour assurer la robustesse du code.

    """
    P_inf = inf_cst["PRESSION"]
    T_inf = inf_cst["TEMPERATURE"]
    rho_inf = inf_cst["MASSE VOLUMIQUE"]

    Mach_inf = Mach["MACH_INF"]
    Mach_local = Mach["MACH_LOCAL"]

    v_inf = Velocity["V_INF"]
    v_local = Velocity["V_LOCAL"]


    if Mach_inf < 3:
        gamma_mach = basic_gamma
    else:
        gamma_mach = calculate_gamma_rarefied(M_infty=Mach_inf, T_infty=T_inf)

    if Mach_inf < 0.3:
        # régime subsonique incompressible

        P_local = P_inf + 0.5 * rho_inf * (v_inf**2 - v_local**2)
        T_local = T_inf
        rho_local = rho_inf

        local_params = {
            "PRESSION": P_local,
            "TEMPERATURE": T_local,
            "MASSE VOLUMIQUE": rho_local, 
        }
        
        return local_params
    
    elif 0.3 <= Mach_inf and Mach_inf < 1:
        # régime subsonique compressible + transsonique (mach < 1)

        P_local = P_inf * ((1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * Mach_local**2))**(gamma_mach / (gamma_mach - 1))
        T_local = T_inf * ((1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * Mach_local**2))
        rho_local = rho_inf * ((1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * Mach_local**2))**(1 / (gamma_mach - 1))

        local_params = {
            "PRESSION": P_local,
            "TEMPERATURE": T_local,
            "MASSE VOLUMIQUE": rho_local, 
        }

        return local_params

    elif 1 <= Mach_inf and Mach_inf < 1.2:
        # régime transsonique (mach < 1.2)

        S_M = Shock_Growth_S(Mach_local)

        P_sub = P_inf * ((1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * Mach_local**2))**(gamma_mach / (gamma_mach - 1))
        P_sup = P_inf * (1 - 0.2 * (Mach_local - 1))

        T_sub = T_inf * ((1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * Mach_local**2))
        T_sup = T_inf * (1 - 0.2 * (Mach_local - 1))

        rho_sub = rho_inf * ((1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * Mach_local**2))**(1 / (gamma_mach - 1))
        rho_sup = rho_inf * (1 - 0.2 * (Mach_local - 1))

        P_local = P_sub + S_M * (P_sup - P_sub)
        T_local = T_sub + S_M * (T_sup - T_sub)
        rho_local = rho_sub + S_M * (rho_sup - rho_sub)

        local_params = {
            "PRESSION": P_local,
            "TEMPERATURE": T_local,
            "MASSE VOLUMIQUE": rho_local, 
        }

        return local_params
    
    elif 1.2 <= Mach_inf:
        # Régime supersonique + hypersonique
            
        if np.all(deviation_angle > 0): 
            # --> méthode des chocs

            shock_angle = Correct_Beta_Vector(Get_ShockAngle_Vectorized(Mach_inf, deviation_angle, gamma_mach))
            mach_n = Mach_inf * np.sin(shock_angle)

            AfterShock = AfterShock_var(mach_n=mach_n, P_down=P_inf, T_down=T_inf, rho_down=rho_inf, gamma=gamma_mach)

            local_params = {
                "PRESSION": AfterShock["PRESSION"],
                "TEMPERATURE": AfterShock["TEMPERATURE"],
                "MASSE VOLUMIQUE": AfterShock["MASSE VOLUMIQUE"], 
            }

            return local_params

        else:        
            try:
            # Régime supersonique + hypersonique
        
                # --> méthode Prandtl-Meyer

                mach_after = np.zeros(shape=len(deviation_angle))
                deviation_angle = np.abs(deviation_angle)

                for idx, theta in enumerate(deviation_angle):
                    
                    nu_before = PrandtlMeyer(mach=Mach_inf, gamma=gamma_mach)
                    nu_after = nu_before + theta
                    mach_after[idx] = newton(inv_PrandtlMeyer, Mach_inf, args=(gamma_mach, nu_after), maxiter=200)

                T2_T1 = (1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * mach_after**2)
                P2_P1 = T2_T1 ** (gamma_mach / (gamma_mach - 1))
                rho2_rho1 = T2_T1 ** (1 / (gamma_mach - 1))

                local_params = {
                    "PRESSION": P2_P1 * P_inf,
                    "TEMPERATURE": T2_T1 * T_inf,
                    "MASSE VOLUMIQUE": rho2_rho1 * rho_inf, 
                }

                return local_params
            
            except Exception as e:
                print(f"Erreur détectée : {e}")  # Optionnel : pour déboguer
                return "CONSTANT"

    else:
        return np.nan