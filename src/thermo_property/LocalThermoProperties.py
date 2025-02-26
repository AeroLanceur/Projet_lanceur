import numpy as np
from thermo_property.AfterShocProperties import AfterShock_var
from shock_management.Expansion import PrandtlMeyer, inv_PrandtlMeyer, solve_mach_from_nu
from shock_management.Oblique import Get_ShockAngle_Vectorized, Correct_Beta_Vector
from scipy.optimize import newton
from thermo_property.GammaManagement import calculate_gamma_rarefied

from scipy.optimize import root_scalar

def Shock_Growth_S(M, n=2, k=0.1):
    """ Fonction de croissance du choc S(M) utilisée dans le Shock Growth Model """
    return ((M - 1)**n) / ((M - 1)**n + k)

def Get_Local_Params(inf_cst, Mach, Velocity, deviation_angle, gamma):

    P_inf = inf_cst["PRESSION"]
    T_inf = inf_cst["TEMPERATURE"]
    rho_inf = inf_cst["MASSE VOLUMIQUE"]

    Mach_inf = Mach["MACH_INF"]
    Mach_local = Mach["MACH_LOCAL"]

    v_inf = Velocity["V_INF"]
    v_local = Velocity["V_LOCAL"]

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

        P_local = P_inf * ((1 + (gamma - 1) / 2 * Mach_inf**2) / (1 + (gamma - 1) / 2 * Mach_local**2))**(gamma / (gamma - 1))
        T_local = T_inf * ((1 + (gamma - 1) / 2 * Mach_inf**2) / (1 + (gamma - 1) / 2 * Mach_local**2))
        rho_local = rho_inf * ((1 + (gamma - 1) / 2 * Mach_inf**2) / (1 + (gamma - 1) / 2 * Mach_local**2))**(1 / (gamma - 1))

        local_params = {
            "PRESSION": P_local,
            "TEMPERATURE": T_local,
            "MASSE VOLUMIQUE": rho_local, 
        }

        return local_params

    elif 1 <= Mach_inf and Mach_inf < 1.2:
        # régime transsonique (mach < 1.2)

        S_M = Shock_Growth_S(Mach_local)

        P_sub = P_inf * ((1 + (gamma - 1) / 2 * Mach_inf**2) / (1 + (gamma - 1) / 2 * Mach_local**2))**(gamma / (gamma - 1))
        P_sup = P_inf * (1 - 0.2 * (Mach_local - 1))

        T_sub = T_inf * ((1 + (gamma - 1) / 2 * Mach_inf**2) / (1 + (gamma - 1) / 2 * Mach_local**2))
        T_sup = T_inf * (1 - 0.2 * (Mach_local - 1))

        rho_sub = rho_inf * ((1 + (gamma - 1) / 2 * Mach_inf**2) / (1 + (gamma - 1) / 2 * Mach_local**2))**(1 / (gamma - 1))
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
        # régime supersonique + hypersonique

        if np.all(deviation_angle > 0): 
            # --> méthode des chocs

            shock_angle = Correct_Beta_Vector(Get_ShockAngle_Vectorized(Mach_inf, deviation_angle, gamma))
            mach_n = Mach_inf * np.sin(shock_angle)

            AfterShock = AfterShock_var(mach_n=mach_n, P_down=P_inf, T_down=T_inf, rho_down=rho_inf, gamma=gamma)

            local_params = {
                "PRESSION": AfterShock["PRESSION"],
                "TEMPERATURE": AfterShock["TEMPERATURE"],
                "MASSE VOLUMIQUE": AfterShock["MASSE VOLUMIQUE"], 
            }

        else:
            # --> méthode Prandtl-Meyer

            mach_after = np.zeros(shape=len(deviation_angle))
            deviation_angle = np.abs(deviation_angle)

            if Mach_inf < 3:
                gamma_mach = 1.4
            else:
                gamma_mach = calculate_gamma_rarefied(M_infty=Mach_inf, T_infty=T_inf)

            for idx, theta in enumerate(deviation_angle):
                
                nu_before = PrandtlMeyer(mach=Mach_inf, gamma=gamma_mach)
                nu_after = nu_before + theta
                mach_after[idx] = newton(inv_PrandtlMeyer, Mach_inf, args=(gamma_mach, nu_after))

                # mach_after[idx] = solve_mach_from_nu(nu_after, Mach_inf, gamma)

            T2_T1 = (1 + (gamma_mach - 1) / 2 * Mach_inf**2) / (1 + (gamma_mach - 1) / 2 * mach_after**2)
            P2_P1 = T2_T1 ** (gamma_mach / (gamma_mach - 1))
            rho2_rho1 = T2_T1 ** (1 / (gamma_mach - 1))

            local_params = {
                "PRESSION": P2_P1 * P_inf,
                "TEMPERATURE": T2_T1 * T_inf,
                "MASSE VOLUMIQUE": rho2_rho1 * rho_inf, 
            }

        return local_params

    else:
        return np.nan