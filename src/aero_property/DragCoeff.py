import numpy as np

def Reynolds(rho, velocity, viscosity, s_x):

    return (rho * velocity * s_x) / viscosity

def Get_Frot_Coeff(Reynold):

    Cf_arr = np.zeros(shape=len(Reynold))

    for idx, Re in enumerate(Reynold):

        if Re < 5e5: # --> laminaire
            Cf_arr[idx] = 1.328 / np.sqrt(Re)
        else:
            Cf_arr[idx] = 0.072 / (Re**(1/5))

    return Cf_arr

def Get_Wall_Constraint(Cf, rho, velocity):

    return 0.5 * Cf * rho * velocity**2

def Get_Drag_Coeff(tau_w, Cp, x_arr, y_arr, ds_x_arr, args):

    S_ref, rho, V, mach, gamma = args 
    q_inf = 0.5 * rho * V**2 
    theta = np.arctan(np.gradient(y_arr, x_arr))

        # --> traînée de frottement
    dF_x_frott = tau_w * np.cos(theta) * ds_x_arr
    Cd_frott_arr = np.cumsum(dF_x_frott) / (q_inf * S_ref)

        # --> traînée de pression
    dCd_pressure = Cp * np.sin(theta) / S_ref
    Cd_press_arr = np.cumsum(dCd_pressure)

        # --> traînée d'onde
    if mach < 0.8:
        Cd_wave_arr = np.full(shape=len(x_arr), fill_value=0.0)
    elif 0.8 <= mach and mach < 1.2:
        Cd_wave_arr = np.full(shape=len(x_arr), fill_value=4/(mach**2 - 1))
    else:
        Cd_wave_arr = (2/(gamma * mach**2)) * np.sin(theta)**2


    return Cd_frott_arr, Cd_press_arr, Cd_wave_arr

def Get_Total_Drag(Cd_frott, Cd_press, Cd_wave):

    Cd_tot_frott = np.abs(Cd_frott["UPP"]) + np.abs(Cd_frott["LOW"])
    Cd_tot_pression = np.abs(Cd_press["UPP"]) + np.abs(Cd_press["LOW"])
    Cd_tot_wave = np.abs(Cd_wave["UPP"]) + np.abs(Cd_wave["LOW"])

    Cd_tot = Cd_tot_frott + Cd_tot_pression + Cd_tot_wave

    return Cd_tot, Cd_tot_frott, Cd_tot_pression, Cd_tot_wave