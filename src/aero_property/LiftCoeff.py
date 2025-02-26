import numpy as np

def Get_LiftCoeff(Cp_dict, ds_dict, theta_dict, x_arr):

    Cp_upper = Cp_dict["UPP"]
    Cp_lower = Cp_dict["LOW"]

    ds_x_upper = ds_dict["UPP"]
    ds_x_lower = ds_dict["LOW"]

    dev_angle_upper = theta_dict["UPP"]
    dev_angle_lower = theta_dict["LOW"]

    dCl_dx_upper = (1/x_arr[-1]) * Cp_upper * np.cos(dev_angle_upper) * ds_x_upper
    dCl_dx_lower = (1/x_arr[-1]) * Cp_lower * np.cos(dev_angle_lower) * ds_x_lower

        # --> Coefficient de portance face supérieure
    Cl_x_upper = np.cumsum(dCl_dx_upper)

        # --> Coefficient de portance face inférieure
    Cl_x_lower = np.cumsum(dCl_dx_lower)

        # --> Coefficient de portance totale
    CL_x = np.cumsum((Cp_upper * np.cos(dev_angle_upper) - Cp_lower * np.cos(dev_angle_lower)) * (ds_x_upper + ds_x_lower)) / x_arr[-1]

    return CL_x, Cl_x_upper, Cl_x_lower
