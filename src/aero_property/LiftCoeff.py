import numpy as np

def Get_LiftCoeff(Cp_dict, ds_dict, theta_dict, x_arr):
    """
    Calcule le coefficient de portance total et ses contributions provenant des faces supérieure et inférieure.

    Paramètres :
    ------------
    Cp_dict : dict
        Dictionnaire contenant les coefficients de pression :
        - "UPP" : Face supérieure du profil.
        - "LOW" : Face inférieure du profil.
    ds_dict : dict
        Dictionnaire contenant les éléments de surface élémentaires :
        - "UPP" : Face supérieure du profil.
        - "LOW" : Face inférieure du profil.
    theta_dict : dict
        Dictionnaire contenant les angles de déviation du profil :
        - "UPP" : Face supérieure du profil.
        - "LOW" : Face inférieure du profil.
    x_arr : array-like
        Coordonnées x des points du profil.

    Retourne :
    ---------
    tuple :
        - CL_x : np.ndarray
            Coefficient de portance total en fonction de la position sur le profil.
        - Cl_x_upper : np.ndarray
            Contribution de la face supérieure au coefficient de portance.
        - Cl_x_lower : np.ndarray
            Contribution de la face inférieure au coefficient de portance.

    Remarque :
    ----------
    - La portance est calculée à partir des coefficients de pression et des angles de déviation.
    - Les contributions de la face supérieure et inférieure sont calculées séparément avant d’être additionnées.
    - La somme cumulée est utilisée pour intégrer la portance le long du profil.
    """
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
