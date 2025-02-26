import numpy as np

def AfterShock_var(mach_n, P_down, T_down, rho_down, gamma):
    """
    Calcule les variables thermodynamiques et le nombre de Mach après un choc oblique.

    Cette fonction détermine la pression, la température, la masse volumique et le nombre de Mach
    normalisé après un choc oblique à partir des conditions en aval et du nombre de Mach normal en amont.

    Paramètres :
    ------------
    mach_n : float
        Nombre de Mach normal de l'écoulement avant le choc.
    P_down : float
        Pression en aval du choc (Pa).
    T_down : float
        Température en aval du choc (K).
    rho_down : float
        Masse volumique en aval du choc (kg/m³).
    gamma : float
        Rapport des capacités thermiques (Cp/Cv) du gaz.

    Retourne :
    ----------
    dict
        Dictionnaire contenant les variables thermodynamiques après le choc :
        - `"PRESSION"` : Pression après le choc (Pa).
        - `"TEMPERATURE"` : Température après le choc (K).
        - `"MASSE VOLUMIQUE"` : Masse volumique après le choc (kg/m³).
        - `"MACH"` : Nombre de Mach normalisé après le choc.
    """

    # --> Nombre de Mach après le choc
    mach_after_shock_n = np.sqrt((2 + (gamma - 1) * mach_n**2) / (2 * gamma * mach_n**2 + (1 - gamma)))

    # --> Rapport de pression
    pression_ratio = ((2 * gamma) / (gamma + 1)) * mach_n**2 - ((gamma - 1) / (gamma + 1))
    P_shock = pression_ratio * P_down

    # --> Rapport de température
    temperature_ratio = (1 + 0.5 * (gamma - 1) * mach_n**2) / (1 + 0.5 * (gamma - 1) * mach_after_shock_n**2)
    T_shock = temperature_ratio * T_down

    # --> Rapport de masse volumique
    rho_ratio = ((gamma + 1) * mach_n**2) / (2 + (gamma - 1) * mach_n**2)
    rho_shock = rho_ratio * rho_down

    # Dictionnaire contenant les valeurs après le choc
    AfterShock = {
        "PRESSION": P_shock,
        "TEMPERATURE": T_shock,
        "MASSE VOLUMIQUE": rho_shock,
        "MACH": mach_after_shock_n
    }

    return AfterShock
