import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def Show_ThermoProperties(profil_shape, cst_dict, LocalParams, PressureCoeff):
    """
    Affiche l'évolution des paramètres thermodynamiques sur un profil donné.

    Cette fonction génère une figure contenant plusieurs sous-graphiques :
    1. Représentation du profil aérodynamique.
    2. Évolution de la pression sur les faces supérieure et inférieure du profil.
    3. Évolution de la température sur les faces supérieure et inférieure du profil.
    4. Évolution de la masse volumique sur les faces supérieure et inférieure du profil.
    5. Distribution du coefficient de pression sur le profil.

    Paramètres :
    ------------
    profil_shape : dict
        Contient les coordonnées du profil :
        - "x_shape" : Vecteur des abscisses (hauteur en m).
        - "y_upper_" : Coordonnées y de la face supérieure du profil.
        - "y_lower_" : Coordonnées y de la face inférieure du profil.

    cst_dict : dict
        Dictionnaire contenant les constantes de la simulation :
        - "INF_CST" : Dictionnaire des conditions de l'écoulement (Mach, pression, température, masse volumique).
        - "AoA" : Angle d'attaque en radians.

    LocalParams : dict
        Dictionnaire contenant les paramètres locaux sur le profil :
        - "UPPER" : Dictionnaire des valeurs pour la face supérieure.
        - "LOWER" : Dictionnaire des valeurs pour la face inférieure.
        Chaque face contient les clés :
        - "PRESSION" : Pression locale en Pascal.
        - "TEMPERATURE" : Température locale en Kelvin.
        - "MASSE VOLUMIQUE" : Masse volumique locale en kg/m³.

    PressureCoeff : dict
        Dictionnaire des coefficients de pression :
        - "UPPER" : Coefficients de pression sur la face supérieure.
        - "LOWER" : Coefficients de pression sur la face inférieure.

    Sortie :
    --------
    Affiche une figure matplotlib avec plusieurs graphiques détaillant l'évolution des paramètres thermodynamiques 
    le long du profil étudié.

    Remarque :
    ----------
    - Si le nombre de Mach est inférieur à 0.3, les valeurs de pression, température et masse volumique sont constantes 
      sur l'ensemble du profil.
    - Sinon, les variations des grandeurs thermodynamiques sont tracées pour les deux faces.
    """
    # argument manager -->
        # --> profil étudié
    x_shape = profil_shape["x_shape"]
    y_upper_ = profil_shape["y_upper_"]
    y_lower_ = profil_shape["y_lower_"]

        # --> constante de la simulation
    Mach_inf = cst_dict["INF_CST"]["MACH"]
    AoA = cst_dict["AoA"]
    inf_cst = cst_dict["INF_CST"]

        # --> paramètres local
    LocalParams_Lower = LocalParams["LOWER"]
    LocalParams_Upper = LocalParams["UPPER"]

        # --> coefficient de pression
    Cp_lower = PressureCoeff["LOWER"]
    Cp_upper = PressureCoeff["UPPER"]

    fig = plt.figure(figsize=(20, 12))
    fig.suptitle(f"Évolution des paramètres thermodynamiques (AoA = {np.rad2deg(AoA):.2f}°, Mach = {Mach_inf:.2f} et Z = {inf_cst['ALTITUDE']*1e-3:.4f} km)", fontsize=20)
    gs = GridSpec(3, 3, figure=fig)

    profil_ax = fig.add_subplot(gs[0, :])
    profil_ax.plot(x_shape, y_upper_, 'r', label='Face supérieure')
    profil_ax.plot(x_shape, y_lower_, 'b', label='Face inférieure')

    profil_ax.set_xlabel("Hauteur [m]")
    profil_ax.set_ylabel("Diamètre [m]")
    profil_ax.grid('on', alpha=0.75, linestyle=('-.'))
    profil_ax.legend()

    axs_0 = fig.add_subplot(gs[1, 0])
    axs_1 = fig.add_subplot(gs[1, 1])
    axs_2 = fig.add_subplot(gs[1, 2])

    if cst_dict["INF_CST"]["MACH"] < 0.3:
        axs_0.plot(x_shape, np.full(shape=len(x_shape), fill_value=LocalParams_Lower["PRESSION"]), 'k-.', label="Pression")
        axs_1.plot(x_shape, np.full(shape=len(x_shape), fill_value=LocalParams_Lower["TEMPERATURE"]), 'k-.', label="Température")
        axs_2.plot(x_shape, np.full(shape=len(x_shape), fill_value=LocalParams_Lower["MASSE VOLUMIQUE"]), 'k-.', label="Masse volumique")

    else:   
        axs_0.plot(x_shape, LocalParams_Lower["PRESSION"], 'b', label="Face inférieure")
        axs_0.plot(x_shape, LocalParams_Upper["PRESSION"], 'r', label="Face supérieure")
        axs_0.plot(x_shape, np.full(shape=len(x_shape), fill_value=cst_dict["INF_CST"]["PRESSION"]), 'k--', label=r"$P_{\infty}$")

        axs_1.plot(x_shape, LocalParams_Lower["TEMPERATURE"], 'b', label="Face inférieure")
        axs_1.plot(x_shape, LocalParams_Upper["TEMPERATURE"], 'r', label="Face supérieure")
        axs_1.plot(x_shape, np.full(shape=len(x_shape), fill_value=cst_dict["INF_CST"]["TEMPERATURE"]), 'k--', label=r"$T_{\infty}$")

        
        axs_2.plot(x_shape, LocalParams_Lower["MASSE VOLUMIQUE"], 'b', label="Face inférieure")
        axs_2.plot(x_shape, LocalParams_Upper["MASSE VOLUMIQUE"], 'r', label="Face supérieure")
        axs_2.plot(x_shape, np.full(shape=len(x_shape), fill_value=cst_dict["INF_CST"]["MASSE VOLUMIQUE"]), 'k--', label=r"$\rho_{\infty}$")

    axs_0.set_xlabel('Hauteur [m]')
    axs_0.set_ylabel(r'Pression [$Pa$]')
    axs_0.grid('on', alpha=0.75, linestyle='-.')
    axs_0.set_yscale('log')
    axs_0.legend(loc='best')

    axs_1.set_xlabel('Hauteur [m]')
    axs_1.set_ylabel(r'Température [$K$]')
    axs_1.grid('on', alpha=0.75, linestyle='-.')
    axs_1.legend(loc='best')

    axs_2.set_xlabel('Hauteur [m]')
    axs_2.set_ylabel(r'Masse volumique [$kg/m^3$]')
    axs_2.grid('on', alpha=0.75, linestyle='-.')
    axs_2.legend(loc='best')

    pressure_coeff_ax = fig.add_subplot(gs[2, :])
    pressure_coeff_ax.plot(x_shape, Cp_lower, 'b', label="Face inférieure")
    pressure_coeff_ax.plot(x_shape, Cp_upper, 'r', label="Face supérieure")
    pressure_coeff_ax.grid('on', alpha=0.75, linestyle='-.')
    pressure_coeff_ax.set_xlabel("Hauteur [m]")
    pressure_coeff_ax.set_ylabel("Coefficient de Pression")
    pressure_coeff_ax.legend(loc="best")

    plt.show()