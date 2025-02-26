import numpy as np
from scipy.optimize import root_scalar, newton

def PrandtlMeyer(mach, gamma):
    """
    Calcule la fonction de Prandtl-Meyer pour un nombre de Mach donné.

    La fonction de Prandtl-Meyer permet de déterminer l'angle de déviation d'un écoulement supersonique 
    dans une expansion isentropique.

    Paramètres :
    ------------
    mach : float
        Nombre de Mach de l'écoulement.
    gamma : float
        Rapport des capacités thermiques (Cp/Cv) du gaz.

    Retourne :
    ----------
    float
        L'angle de Prandtl-Meyer (en radians).
    """
    return np.sqrt((gamma + 1) / (gamma - 1)) * np.arctan(np.sqrt(((gamma - 1) / (gamma + 1)) * (mach**2 - 1))) - np.arctan(np.sqrt(mach**2 - 1))

def inv_PrandtlMeyer(mach, gamma, nu):
    """
    Fonction résiduelle pour l'inversion de la fonction de Prandtl-Meyer.

    Cette fonction est utilisée pour trouver le nombre de Mach correspondant à un angle de Prandtl-Meyer donné.

    Paramètres :
    ------------
    mach : float
        Nombre de Mach de l'écoulement.
    gamma : float
        Rapport des capacités thermiques (Cp/Cv) du gaz.
    nu : float
        Angle de Prandtl-Meyer cible (en radians).

    Retourne :
    ----------
    float
        La différence entre la fonction de Prandtl-Meyer calculée et l'angle cible.
        Cette valeur doit être minimisée pour obtenir le nombre de Mach souhaité.
    """
    return PrandtlMeyer(mach, gamma) - nu

def safe_newton(f, x0, args, max_attempts=5):
    """
    Version sécurisée de la méthode de Newton avec gestion des échecs.

    Paramètres :
    ------------
    - f : fonction à annuler.
    - x0 : valeur initiale.
    - args : arguments de la fonction.
    - max_attempts : nombre maximal d'essais avant d'échouer.

    Retour :
    --------
    - Racine trouvée ou erreur si aucune solution trouvée.
    """
    for attempt in range(max_attempts):
        try:
            return newton(f, x0, args=args, maxiter=50, tol=1e-6)
        except RuntimeError:
            print(f"[WARN] Newton a échoué à l'itération {attempt+1}, changement de x0...")
            x0 *= 1.05  # Ajuste légèrement x0 pour retenter
            
    raise ValueError(f"Échec de convergence après {max_attempts} tentatives.")

def solve_mach_from_nu(nu_target, mach_guess, gamma):
    """
    Trouve le Mach correspondant à un angle de Prandtl-Meyer donné avec Newton sécurisé.

    Paramètres :
    ------------
    - nu_target : float -> Angle de Prandtl-Meyer cible (en radians).
    - mach_guess : float -> Estimation initiale du nombre de Mach.
    - gamma : float -> Rapport Cp/Cv du gaz.

    Retour :
    --------
    - Mach correspondant à l'angle de Prandtl-Meyer donné.
    """
    return safe_newton(inv_PrandtlMeyer, mach_guess, args=(gamma, nu_target))

def max_PrandtlMeyer_Mach(gamma, mach_max=20):
    """ 
    Calcule la valeur maximale de la fonction de Prandtl-Meyer pour un Mach donné.
    
    Paramètres :
    ------------
    - gamma : float -> Rapport Cp/Cv.
    - mach_max : float -> Valeur maximale de Mach considérée.

    Retour :
    --------
    - Valeur maximale atteignable de la fonction Prandtl-Meyer.
    """
    return PrandtlMeyer(mach_max, gamma)