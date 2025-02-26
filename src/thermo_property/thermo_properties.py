import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

    # ========================================== #
    # ========== COUCHE ATMOSPHÉRIQUE ========== #
    # ========================================== #

temperature_layer = [
    (0, 288.15, -0.0065), 
    (11019, 216.65, 0.0),  
    (20063, 216.65, 0.001), 
    (32162, 228.65, 0.0028), 
    (47350, 270.65, 0.0), 
    (55000, 270.65, -0.00175),
    (65000, 253.15, -0.00483),
    (80000, 180.65, 0),
    (91000, 180.65, 0.0027272727),
    (102000, 210.65, 0.0060555556),
    (111000, 265.65, 0.007)
]

pressure_layer = [
    (0, 1.0134e5, -0.12773),
    (6000, 1.1772e5, -0.1537),
    (25000, 1.0134e5, -0.148),
    (36000, 0.4905e5, -0.12681), 
    (50000, 0, 0) 
]

density_layer = [
    (0, 1.225, -0.1064), 
    (11000, 2.2, -0.15983),
    (34000, 1.05, -0.13807),
    (50000, 0, 0)
]

    # ============================================================================================ #
    # ========== CALCUL DE LA TEMPÉRATURE / VITESSE DU SON / PRESSION / MASSE VOLUMIQUE ========== #
    # ============================================================================================ #

def temperature(Z, layers):
    for i in range(len(layers) - 1):
        Z_start, T_start, Tz = layers[i]
        Z_next = layers[i + 1][0]

        if Z_start <= Z < Z_next:
            return T_start + Tz * (Z - Z_start)

    Z_last, T_last, Tz_last = layers[-1]
    return T_last + Tz_last * (Z - Z_last)

def vitesse_son(gamma, R, T):
    return np.sqrt(gamma * R * T)

def pressure(Z, layers):
    for i in range(len(layers) - 1):
        Z_start, P_start, Pz = layers[i]
        Z_next = layers[i + 1][0]

        if Z_start <= Z < Z_next:
            return P_start * np.exp(Pz * (Z - Z_start))

    return 0 

def density(Z, layers):
    for i in range(len(layers) - 1):
        Z_start, rho_start, rho_z = layers[i]
        Z_next = layers[i + 1][0]

        if Z_start <= Z < Z_next:
            return rho_start * np.exp(rho_z * (Z - Z_start))

    return 0 

    # ================================= #
    # ========== PROPRIÉTÉES ========== #
    # ================================= #

def Get_ThermoProperties():

    Z = np.linspace(0, 110000, 1000)
    Z_km = Z * 1e-3

    temperatures_arr = [temperature(z, temperature_layer) for z in Z]
    vitesse_son_arr = [vitesse_son(1.4, (8.314/(28.966*1e-3)), T) for T in temperatures_arr]
    pressure_arr = [pressure(z, pressure_layer) for z in Z_km]
    density_arr = [density(z, density_layer) for z in Z_km]

    fig, axs = plt.subplots(2, 2, figsize=(14, 11), sharey=True, gridspec_kw={'wspace': 0.3})

    axs[0, 0].plot(temperatures_arr, Z_km, color='navy', linewidth=1.5)
    axs[0, 0].set_xlabel("Température [$K$]", fontsize=12)
    axs[0, 0].set_ylabel("Altitude [$km$]", fontsize=12)
    axs[0, 0].set_title("Évolution de la température en fonction de l'altitude", fontsize=14)
    axs[0, 0].grid(True, linestyle="-.", alpha=0.7)
    axs[0, 0].spines['top'].set_visible(False)
    axs[0, 0].spines['right'].set_visible(False)

    axs[0, 1].plot(vitesse_son_arr, Z_km, color='darkred', linewidth=1.5)
    axs[0, 1].set_xlabel(r"Vitesse du son [$m.s^{-1}$]", fontsize=12)
    axs[0, 1].set_title("Évolution de la vitesse du son en fonction de l'altitude", fontsize=14)
    axs[0, 1].grid(True, linestyle="--", alpha=0.7)
    axs[0, 1].spines['top'].set_visible(False)
    axs[0, 1].spines['right'].set_visible(False)

    axs[1, 0].plot(pressure_arr, Z_km, color='purple', linewidth=1.5)
    axs[1, 0].set_xlabel("Pression [$Pa$]", fontsize=12)
    axs[1, 0].set_ylabel("Altitude [$km$]", fontsize=12)
    axs[1, 0].set_title("Évolution de la pression en fonction de l'altitude", fontsize=14)
    axs[1, 0].grid(True, linestyle="-.", alpha=0.7)
    axs[1, 0].spines['top'].set_visible(False)
    axs[1, 0].spines['right'].set_visible(False)

    axs[1, 1].plot(density_arr, Z_km, color='darkgreen', linewidth=1.5)
    axs[1, 1].set_xlabel(r"Masse volumique du son [$kg.m^{-3}$]", fontsize=12)
    axs[1, 1].set_title("Évolution de la masse volumique en fonction de l'altitude", fontsize=14)
    axs[1, 1].grid(True, linestyle="--", alpha=0.7)
    axs[1, 1].spines['top'].set_visible(False)
    axs[1, 1].spines['right'].set_visible(False)

    layer_labels = ["Troposphère", "Stratosphère", "Mésosphère", "Thermosphère"]
    layer_altitudes = [11.019, 50, 85, 110]

    for ax in axs.flat:
        for i, label in enumerate(layer_labels):
            ax.axhline(layer_altitudes[i], color='gray', linestyle=":", alpha=0.6)
            ax.text(ax.get_xlim()[1], layer_altitudes[i] - 2, label, fontsize=10, color="gray",
                    verticalalignment='top', horizontalalignment='right')

    axs[0, 0].set_xlim(min(temperatures_arr) - 10, max(temperatures_arr) + 10)
    axs[0, 1].set_xlim(min(vitesse_son_arr) - 5, max(vitesse_son_arr) + 5)

    plt.suptitle("Évolution des paramètres Atmosphériques en Fonction de l'Altitude", fontsize=16)
    plt.show()

    ThermoProperties_dict = {
        'TEMPERATURE': np.array(temperatures_arr),
        "PRESSION": np.array(pressure_arr),
        "MASSE VOLUMIQUE": np.array(density_arr),
        "VITESSE DU SON": np.array(vitesse_son_arr),
        # "ALTITUDE_Z": np.array(Z)
    }

    return ThermoProperties_dict

def Get_RelativeSpeed():

    xp_alt = [0, 25, 50, 75, 100, 125, 150, 175, 200]
    yp_alt = [0, 2.546, 5.538, 15.084, 26.923, 42.552, 61.538, 86, 110]

    xp_vit = [0, 11, 22, 33, 44, 55, 66, 77, 88, 100, 125, 200]
    yp_vit = [0, 55.55, 166.66, 222, 277.76, 353, 395.016, 512.5, 777, 1000, 2000, 2300]

    x = np.linspace(0, 200, 1000)
    y_alt = np.interp(x, xp_alt, yp_alt)
    y_vit = np.interp(x, xp_vit, yp_vit)

    fig = plt.figure(figsize=(14, 6))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1, 1], wspace=0.3)

    ax1 = fig.add_subplot(gs[0])
    ax1.plot(x, y_alt, "y-", label="Altitude")
    ax1.set_xlabel('Temps (s)')
    ax1.set_ylabel('Altitude (m)')
    ax1.set_title("Évolution de l'altitude d'Ariane 5 en fonction du temps")
    ax1.legend()
    ax1.grid('on', alpha=0.75, linestyle='-.')

    ax2 = fig.add_subplot(gs[1])
    ax2.plot(x, y_vit, "y-", label="Vitesse relative")
    ax2.set_xlabel('Temps (s)')
    ax2.set_ylabel('Vitesse (m/s)')
    ax2.set_title("Évolution de la vitesse d'Ariane 5 en fonction du temps")
    ax2.legend()
    ax2.grid('on', alpha=0.75, linestyle='-.')

    plt.show()

    Pos = {
        "ALTITUDE": y_alt,
        "VITESSE": y_vit,
        'TEMPS': x
    }

    return Pos

    # =================================== #
    # ========== MACH ALTITUDE ========== #
    # =================================== #

def Get_MachAltitude(ThermoProperties_dict):
    xp_vit = np.array([0, 11, 22, 33, 44, 55, 66, 77, 88, 100, 125, 200])
    yp_vit = np.array([0, 55.55, 166.66, 222, 277.76, 353, 395.016, 512.5, 777, 1000, 2000, 2300])

    xp_alt = np.array([0, 25, 50, 75, 100, 125, 150, 175, 200])
    yp_alt = np.array([0, 2546, 5538, 15084, 26923, 42552, 61538, 86000, 107692])

    xp_alt_interp = np.linspace(xp_alt.min(), xp_alt.max(), 1000)
    yp_alt_interp = np.interp(xp_alt_interp, xp_alt, yp_alt)

    B = np.linspace(0, 200, 1000)

    altitude = np.zeros_like(B)
    Nbr_mach = np.zeros_like(B)
    dynamique_pressure = np.zeros_like(B)

    for i, b in enumerate(B):
        y_vit = np.interp(b, xp_vit, yp_vit)
        y_alt = np.interp(b, xp_alt, yp_alt)
        altitude[i] = y_alt
        
        T = np.interp(y_alt, yp_alt_interp, ThermoProperties_dict['TEMPERATURE'])
        a = np.interp(y_alt, yp_alt_interp, ThermoProperties_dict['VITESSE DU SON'])
        P = np.interp(y_alt, yp_alt_interp, ThermoProperties_dict['PRESSION'])
        rho_air = np.interp(y_alt, yp_alt_interp, ThermoProperties_dict['MASSE VOLUMIQUE'])
        
        Nbr_mach[i] = y_vit / a
        dynamique_pressure[i] = 0.5 * rho_air * y_vit**2

    fig, ax1 = plt.subplots(figsize=(10, 5))

    temps = B
    ax1.plot(temps, Nbr_mach, label="Mach", color="red")
    ax1.fill_between(temps, Nbr_mach, 5, where=Nbr_mach >= 5, color='purple', alpha=0.3, label="Hypersonique")
    ax1.fill_between(temps, Nbr_mach, 1, where=(Nbr_mach >= 1) & (Nbr_mach <= 5), color='orange', alpha=0.3, label="Supersonique")
    ax1.fill_between(temps, Nbr_mach, 0.1, where=(Nbr_mach <= 1), color='blue', alpha=0.3, label="Subsonique compressible")
    ax1.fill_between(temps, Nbr_mach, 0, where=(Nbr_mach <= 0.1), color='red', alpha=0.3, label="Subsonique incompressible")
    ax1.axhline(y=1, color='b', linestyle='-')
    ax1.axhline(y=5, color='b', linestyle='-')
    ax1.axhline(y=0.1, color='b', linestyle='-')
    ax1.set_xlabel("Temps (s)")
    ax1.set_ylabel("Nombre de Mach", color='red')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.legend(loc="upper left")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(temps, altitude, label="Altitude (m)", color="yellow")
    ax2.set_ylabel("Altitude (m)", color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')
    ax2.legend(loc="upper right")

    plt.title("Graphique représentant le nombre de Mach et l'altitude en fonction du temps")
    plt.show()

    return temps, Nbr_mach, altitude, dynamique_pressure

def Sutherland(T):

    return 1.458*1e-6 * ((T**(3/2))/(110.4 + T))