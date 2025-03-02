import numpy as np
from thermo_property.GammaManagement import calculate_gamma_rarefied

def Reynolds(rho, velocity, viscosity, s_x):
    """
    Calcule le nombre de Reynolds.

    Paramètres :
    ------------
    rho : float
        Densité du fluide (kg/m³).
    velocity : float
        Vitesse caractéristique du fluide (m/s).
    viscosity : float
        Viscosité dynamique du fluide (Pa.s).
    s_x : float
        Longueur caractéristique (m).

    Retourne :
    ---------
    float :
        Nombre de Reynolds adimensionnel.
    """
    return (rho * velocity * s_x) / viscosity

def Get_Frot_Coeff(Reynold, Mach):
    """
    Calcule le coefficient de frottement en fonction du nombre de Reynolds et du nombre de Mach.

    Paramètres :
    ------------
    Reynold : array-like
        Tableau contenant les nombres de Reynolds.
    Mach : float
        Nombre de Mach de l'écoulement.

    Retourne :
    ---------
    np.ndarray :
        Tableau des coefficients de frottement Cf.
    
    Remarque :
    ----------
    - Pour Mach < 1.0 :
        * Si Re < 5e5, l'écoulement est considéré comme laminaire et le coefficient est donné par la loi de Blasius.
        * Sinon, l'écoulement est turbulent et le coefficient est estimé avec une loi de puissance.
    - Pour Mach ≥ 1.0 :
        * Le coefficient de frottement est calculé selon une loi empirique prenant en compte les effets compressibles.
    """
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
    """
    Calcule la contrainte pariétale (wall shear stress).

    Paramètres :
    ------------
    Mach : float
        Nombre de Mach de l'écoulement.
    Cf : float
        Coefficient de frottement pariétal.
    rho : float
        Densité du fluide (kg/m³).
    velocity : float
        Vitesse de l'écoulement (m/s).
    Temperature : dict
        Dictionnaire contenant la température locale ("LOCAL") et la température de l'écoulement libre ("T_INF").

    Retourne :
    ---------
    float :
        Valeur de la contrainte pariétale en N/m².
    
    Remarque :
    ----------
    - Pour un écoulement subsonique (Mach < 1.0), la contrainte pariétale est calculée classiquement.
    - Pour un écoulement supersonique, une correction est appliquée en fonction du rapport de température locale à la température de l'écoulement libre.
    """
    if Mach < 1.0:
        return 0.5 * Cf * rho * velocity**2
    else:
        return 0.5 * Cf * rho * velocity**2 * (Temperature["LOCAL"] / Temperature["T_INF"])**(-0.2)

def Get_Drag_Coeff(tau_w, Cp, x_arr, y_arr, ds_x_arr, inf_cst, dev_angle):
    """
    Calcule les coefficients de traînée (frottement, pression et onde) pour un écoulement autour d'un profil.

    Paramètres :
    ------------
    tau_w : array-like
        Contraintes pariétales (wall shear stress) sur le profil.
    Cp : array-like
        Coefficients de pression sur le profil.
    x_arr : array-like
        Coordonnées x des points du profil.
    y_arr : array-like
        Coordonnées y des points du profil.
    ds_x_arr : array-like
        Éléments de surface élémentaires le long du profil.
    inf_cst : dict
        Dictionnaire contenant les constantes de l'écoulement :
        - "S_REF" : Surface de référence (m²).
        - "MASSE VOLUMIQUE" : Densité de l'écoulement libre (kg/m³).
        - "VITESSE" : Vitesse de l'écoulement libre (m/s).
        - "MACH" : Nombre de Mach.
        - "GAMMA" : Rapport des chaleurs spécifiques.
        - "TEMPERATURE" : Température de l'écoulement libre (K).
    dev_angle : array-like
        Angles de déviation du profil.

    Retourne :
    ---------
    tuple :
        - Cd_frott_arr : np.ndarray
            Coefficient de traînée de frottement (contribution due aux efforts pariétaux).
        - Cd_press_arr : np.ndarray
            Coefficient de traînée de pression (contribution due aux variations de pression).
        - Cd_wave_arr : np.ndarray
            Coefficient de traînée d'onde (contribution due aux ondes de choc et d'expansion).
    
    Remarque :
    ----------
    - La traînée de frottement est prise en compte uniquement pour Mach < 1.
    - La traînée de pression est calculée différemment selon Mach.
    - La traînée d'onde apparaît uniquement pour Mach ≥ 0.8 et évolue selon le régime subsonique, transsonique et supersonique.
    """
    S_ref, rho, V, mach, gamma, T_inf = inf_cst["S_REF"], inf_cst["MASSE VOLUMIQUE"], inf_cst["VITESSE"], inf_cst["MACH"], inf_cst["GAMMA"], inf_cst["TEMPERATURE"]

    q_inf = 0.5 * rho * V**2 
    theta = np.arctan(np.gradient(y_arr, x_arr))

    if mach < 3:
        gamma_mach = gamma
    else:
        gamma_mach = calculate_gamma_rarefied(M_infty=mach, T_infty=T_inf)

        # --> traînée de frottement
    dF_x_frott = tau_w * np.cos(dev_angle) * ds_x_arr if mach < 1 else 0.0
    if mach < 1:
        Cd_frott_arr = np.cumsum(dF_x_frott) / (q_inf * S_ref)
    else:
        Cd_frott_arr = np.zeros(shape=len(dev_angle))

        # --> traînée de pression
    if mach < 0.8:
        Cd_press_arr = np.cumsum((1/S_ref) * Cp * np.cos(dev_angle) * ds_x_arr) *1e-2
    else:
        Cd_press_arr = (4/(gamma_mach * mach**2)) * np.cumsum((1/x_arr[-1]) * np.sin(dev_angle)**2 * ds_x_arr)

        # --> traînée d'onde
    if mach < 0.8:
        Cd_wave_arr = np.full(shape=len(x_arr), fill_value=0.0)
    elif 0.8 <= mach and mach < 1.2:
        Cd_wave_arr = 0.25 * (2/(gamma_mach * mach**2)) * np.sin(dev_angle)**2
    else:
        Cd_wave_arr = (2/(gamma_mach * mach**2)) * np.sin(dev_angle)**2


    return Cd_frott_arr, Cd_press_arr, Cd_wave_arr

def Get_Total_Drag(Cd_frott, Cd_press, Cd_wave):
    """
    Calcule la traînée totale en sommant les contributions de frottement, de pression et d'onde.

    Paramètres :
    ------------
    Cd_frott : dict
        Dictionnaire contenant les coefficients de traînée de frottement pour les parties supérieure ("UPP") et inférieure ("LOW").
    Cd_press : dict
        Dictionnaire contenant les coefficients de traînée de pression pour les parties supérieure ("UPP") et inférieure ("LOW").
    Cd_wave : dict
        Dictionnaire contenant les coefficients de traînée d'onde pour les parties supérieure ("UPP") et inférieure ("LOW").

    Retourne :
    ---------
    tuple :
        - Cd_tot : float
            Coefficient de traînée totale.
        - Cd_tot_frott : float
            Contribution de la traînée de frottement.
        - Cd_tot_pression : float
            Contribution de la traînée de pression.
        - Cd_tot_wave : float
            Contribution de la traînée d'onde.

    Remarque :
    ----------
    - La traînée totale est obtenue en additionnant les valeurs absolues des contributions des parties supérieure et inférieure.
    - Cette méthode permet d'assurer une somme correcte même en présence de valeurs négatives dues à des variations locales.
    """
    Cd_tot_frott = np.abs(Cd_frott["UPP"]) + np.abs(Cd_frott["LOW"])
    Cd_tot_pression = np.abs(Cd_press["UPP"]) + np.abs(Cd_press["LOW"])
    Cd_tot_wave = np.abs(Cd_wave["UPP"]) + np.abs(Cd_wave["LOW"])

    Cd_tot = Cd_tot_frott + Cd_tot_pression + Cd_tot_wave

    return Cd_tot, Cd_tot_frott, Cd_tot_pression, Cd_tot_wave