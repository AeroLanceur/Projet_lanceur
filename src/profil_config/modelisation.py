import numpy as np

def AoA_Effect(x_arr, y_arr, AoA):

    x_AoA = x_arr * np.cos(AoA) - y_arr * np.sin(AoA)
    y_AoA = x_arr * np.sin(AoA) + y_arr * np.cos(AoA)

    dev_angle = np.arctan(np.gradient(y_AoA, x_AoA))

    return x_AoA, y_AoA, dev_angle

def Get_Local_Velocity(v_inf, EffectiveAngle):

    return v_inf * np.cos(EffectiveAngle)

def curv(x_arr, y_arr):

    dy_dx = np.gradient(y_arr, x_arr)
    dx = np.gradient(x_arr)

    ds_x = np.sqrt(1 + (dy_dx)**2) * dx

    return ds_x, np.cumsum(ds_x)