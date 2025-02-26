import numpy as np
from scipy.optimize import fsolve

def ShockAngleEquation(beta, Mach_inf, theta, gamma):
    """
    Équation permettant de déterminer l'angle de choc β pour un écoulement supersonique.

    Cette équation relie l'angle d'onde de choc β, l'angle de déviation θ et le nombre de Mach en amont 
    pour un choc oblique.

    Paramètres :
    ------------
    beta : float
        Angle d'onde de choc β (en radians).
    Mach_inf : float
        Nombre de Mach de l'écoulement en amont.
    theta : float
        Angle de déviation θ (en radians).
    gamma : float
        Rapport des capacités thermiques (Cp/Cv) du gaz.

    Retourne :
    ----------
    float
        Différence entre les deux côtés de l'équation du choc oblique.
        Cette valeur doit être minimisée pour obtenir l'angle de choc β correct.
    """
    left_side = np.tan(theta)
    right_side = 2 * ((Mach_inf * np.sin(beta))**2 - 1) / (np.tan(beta) * (2 + Mach_inf**2 * (gamma + np.cos(2 * beta))))
    return left_side - right_side


def Get_ShockAngle_Vectorized(Mach_inf, theta_array, gamma=1.4):
    """
    Calcule l'angle de choc β pour un tableau d'angles de déviation θ.

    Cette fonction utilise la méthode `fsolve` pour résoudre l'équation de l'angle de choc 
    pour chaque valeur de θ dans un tableau.

    Paramètres :
    ------------
    Mach_inf : float
        Nombre de Mach de l'écoulement en amont.
    theta_array : array_like
        Tableau contenant les valeurs d'angle de déviation θ (en radians).
    gamma : float, optionnel
        Rapport des capacités thermiques (Cp/Cv) du gaz. Valeur par défaut : 1.4.

    Retourne :
    ----------
    numpy.ndarray
        Tableau contenant les angles de choc β (en radians) correspondant à chaque θ donné.
        Si la solution dépasse 90 degrés ou est inférieure à 0 degré, elle est remplacée par 90 degrés.
    """
    beta_init = np.radians(30)  # Valeur initiale pour la résolution de l'équation

    beta_solutions = np.array([
        fsolve(ShockAngleEquation, beta_init, args=(Mach_inf, theta, gamma))[0] for theta in theta_array
    ])
    
    # Correction des valeurs aberrantes
    beta_solutions[(beta_solutions > np.radians(90)) | (beta_solutions < np.radians(0))] = np.radians(90)

    return beta_solutions


def Correct_Beta_Vector(beta_vector):
    """
    Corrige les discontinuités dans un vecteur d'angles de choc β.

    Lorsque l'onde de choc passe d'un choc attaché à un choc détaché, il peut y avoir une 
    discontinuité dans le calcul de β. Cette fonction détecte une éventuelle discontinuité 
    et ajuste les valeurs après cette discontinuité pour assurer une transition fluide.

    Paramètres :
    ------------
    beta_vector : numpy.ndarray
        Tableau contenant les angles de choc β (en degrés).

    Retourne :
    ----------
    numpy.ndarray
        Tableau corrigé des angles de choc β, avec des valeurs ajustées après une discontinuité.
    """
    indices_90 = np.where(beta_vector == 90)[0]  # Indices où β = 90 degrés
    index_jump = None

    # Détecter la première discontinuité dans la séquence des indices à 90 degrés
    for k in range(1, len(indices_90)):
        if indices_90[k] != indices_90[k-1] + 1:
            index_jump = indices_90[k] - 1
            break

    # Correction des valeurs après la discontinuité
    if index_jump is not None:
        for idx in indices_90:
            if idx > index_jump:
                beta_vector[idx] = beta_vector[index_jump]

    return beta_vector
