import numpy as np
from thermo_property.GammaManagement import calculate_gamma_rarefied

def Reynolds(rho, velocity, viscosity, s_x):
    
    return (rho * velocity * s_x) / viscosity

def Get_Frot_Coeff(Reynold, Mach):

    Cf_arr = np.zeros(shape=len(Reynold))

    for idx, Re in enumerate(Reynold):

        if Mach < 1.0:
            if Re < 5e5: # --> laminaire
                Cf_arr[idx] = 1.328 / np.sqrt(Re)
            else:
                Cf_arr[idx] = 0.072 / (Re**(1/5))
        else:
            Cf_arr[idx] = 0.455 / ((np.log10(Re))**2.58 * (1 + 0.144 * Mach**2)**0.65)

    return Cf_arr

def Get_Wall_Constraint(Mach, Cf, rho, velocity, Temperature):

    if Mach < 1.0:
        return 0.5 * Cf * rho * velocity**2
    else:
        return 0.5 * Cf * rho * velocity**2 * (Temperature["LOCAL"] / Temperature["T_INF"])**(-0.2)

def Get_Drag_Coeff(tau_w, Cp, x_arr, y_arr, ds_x_arr, inf_cst, dev_angle):

    S_ref, rho, V, mach, gamma, T_inf = inf_cst["S_REF"], inf_cst["MASSE VOLUMIQUE"], inf_cst["VITESSE"], inf_cst["MACH"], inf_cst["GAMMA"], inf_cst["TEMPERATURE"]

    q_inf = 0.5 * rho * V**2 
    theta = np.arctan(np.gradient(y_arr, x_arr))

    if mach < 3:
        gamma_mach = gamma
    else:
        gamma_mach = calculate_gamma_rarefied(M_infty=mach, T_infty=T_inf)

        # --> traînée de frottement
    dF_x_frott = tau_w * np.cos(theta) * ds_x_arr 
    Cd_frott_arr = np.cumsum(dF_x_frott) / (q_inf * S_ref)

        # --> traînée de pression
    if mach < 0.8:
        Cd_press_arr = np.cumsum((1/S_ref) * Cp * np.cos(dev_angle) * ds_x_arr) *1e-2
    else:
        Cd_press_arr = (4/(gamma_mach * mach**2)) * np.cumsum((1/x_arr[-1]) * np.sin(dev_angle)**2 * ds_x_arr)

        # --> traînée d'onde
    if mach < 0.8:
        Cd_wave_arr = np.full(shape=len(x_arr), fill_value=0.0)
    elif 0.8 <= mach and mach < 1.2:
        Cd_wave_arr = 0.25 * (2/(gamma_mach * mach**2)) * np.sin(theta)**2
    else:
        Cd_wave_arr = (2/(gamma_mach * mach**2)) * np.sin(theta)**2


    return Cd_frott_arr, Cd_press_arr, Cd_wave_arr

def Get_Total_Drag(Cd_frott, Cd_press, Cd_wave):

    Cd_tot_frott = np.abs(Cd_frott["UPP"]) + np.abs(Cd_frott["LOW"])
    Cd_tot_pression = np.abs(Cd_press["UPP"]) + np.abs(Cd_press["LOW"])
    Cd_tot_wave = np.abs(Cd_wave["UPP"]) + np.abs(Cd_wave["LOW"])

    Cd_tot = Cd_tot_frott + Cd_tot_pression + Cd_tot_wave

    return Cd_tot, Cd_tot_frott, Cd_tot_pression, Cd_tot_wave