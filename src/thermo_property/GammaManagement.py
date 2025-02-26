def calculate_gamma_rarefied(M_infty, T_infty, gamma_0=1.4, T_0=300, M_0=1, a=0.005, b=0.01, c=0.001, d=0.005, e=0.001):
    """
    Calculate the specific heat ratio (gamma) for a rarefied atmosphere using an empirical model.

    Parameters:
    M_infty (float): Free-stream Mach number (should be >= 3)
    T_infty (float): Free-stream temperature in Kelvin
    gamma_0 (float): Reference specific heat ratio
    T_0 (float): Reference temperature in Kelvin
    M_0 (float): Reference Mach number
    a, b, c, d, e (float): Empirical coefficients

    Returns:
    float: Calculated specific heat ratio (gamma)
    """
    if M_infty < 1:
        raise ValueError("Mach number should be 3 or greater for supersonic/hypersonic flow.")

    # Adjust gamma to ensure it remains within a physically plausible range
    gamma = max(1.05, gamma_0 - a * (T_infty / T_0) - b * (M_infty / M_0) -
                 c * (T_infty / T_0)**2 - d * (M_infty / M_0)**2 -
                 e * (T_infty / T_0) * (M_infty / M_0))

    return gamma