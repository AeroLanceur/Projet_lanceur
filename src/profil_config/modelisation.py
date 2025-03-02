import numpy as np

def AoA_Effect(x_arr, y_arr, AoA):
    """
    Applique un angle d'attaque (AoA) à un profil et calcule l'angle de déviation local.

    Cette fonction effectue une rotation du profil autour de l'origine en fonction de l'angle d'attaque donné, 
    puis détermine l'angle de déviation local en fonction de la pente du profil après rotation.

    Paramètres :
    ------------
    x_arr : array-like
        Coordonnées x du profil avant rotation.
    y_arr : array-like
        Coordonnées y du profil avant rotation.
    AoA : float
        Angle d'attaque en degrés.

    Retourne :
    ----------
    x_AoA : array-like
        Coordonnées x du profil après application de l'angle d'attaque.
    y_AoA : array-like
        Coordonnées y du profil après application de l'angle d'attaque.
    dev_angle : array-like
        Angle de déviation local du profil après rotation.

    Remarque :
    ----------
    - La rotation est effectuée dans le sens trigonométrique.
    - Si des valeurs NaN apparaissent dans `dev_angle`, elles sont remplacées par la dernière valeur valide précédente.
    """
    AoA_rad = np.radians(AoA)
    
    x_AoA = x_arr * np.cos(AoA_rad) - y_arr * np.sin(AoA_rad)
    y_AoA = x_arr * np.sin(AoA_rad) + y_arr * np.cos(AoA_rad)

    dy_dx = np.gradient(y_AoA, x_AoA)
    dev_angle = np.arctan(dy_dx)

    index_nan = np.where(np.isnan(dev_angle))[0]
    for idx in index_nan:
        if idx > 0:
            dev_angle[idx] = dev_angle[idx - 1]

    return x_AoA, y_AoA, dev_angle

def Get_Local_Velocity(v_inf, EffectiveAngle):
    """
    Calcule la composante locale de la vitesse en fonction de l'angle effectif.

    Paramètres :
    ------------
    v_inf : float
        Vitesse de l'écoulement libre.
    EffectiveAngle : array-like
        Angle effectif local en radians.

    Retourne :
    ----------
    v_local : array-like
        Composante locale de la vitesse.

    Remarque :
    ----------
    - La vitesse locale est calculée en projetant la vitesse de l'écoulement libre sur la direction de l'angle effectif.
    """
    return v_inf * np.cos(EffectiveAngle)

def curv(x_arr, y_arr):
    """
    Calcule la longueur de l'arc le long du profil.

    Paramètres :
    ------------
    x_arr : array-like
        Coordonnées x du profil.
    y_arr : array-like
        Coordonnées y du profil.

    Retourne :
    ----------
    ds_x : array-like
        Éléments différentiels de la longueur de l'arc le long du profil.
    s_x : array-like
        Longueur cumulée de l'arc le long du profil.

    Remarque :
    ----------
    - La longueur de l'arc est calculée en utilisant la norme du gradient de `y_arr` par rapport à `x_arr`.
    - La fonction `np.cumsum(ds_x)` est utilisée pour obtenir la longueur totale accumulée.
    """
    dy_dx = np.gradient(y_arr, x_arr)
    dx = np.gradient(x_arr)

    ds_x = np.sqrt(1 + (dy_dx)**2) * dx

    return ds_x, np.cumsum(ds_x)