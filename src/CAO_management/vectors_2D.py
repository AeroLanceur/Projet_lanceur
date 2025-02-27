import numpy as np

shape_params = {

    "COIFFE" : {
        "RADIUS": 2.7,
        "X_START": 0.0,
        "X_END": 7.67,
        "Y_START": 0.0,
        "Y_END": 2.7
    },

    "MAIN_FUSELAGE" : {
        "X_START": 7.67,
        "X_END": 15.39427,
        "Y": 2.7
    },
    
    "TRANSITION" : {
        "RADIUS": 0.83775,
        "X_START": 15.39427,
        "X_END": 16.23202,
        "Y_START": 2.7,
        "Y_END": 3.53775,
    },

    "PENTE": {
        "X_START": 16.23202,
        "X_END": 19.86872,
        "Y_START": 3.53775,
        "Y_END": 5.75,
    },

    "BOOSTER_FUSELAGE": {
        "X_START": 19.86872,
        "X_END": 49.670,
        "Y": 5.75
    }
}

def Get_2D_vectors():

    x_cover = np.linspace(shape_params["COIFFE"]["X_START"], shape_params["COIFFE"]["X_END"], 1000)
    theta_cover = np.arccos(1 - 2*x_cover/x_cover[-1])
    y_cover = shape_params["COIFFE"]["RADIUS"] * np.sqrt(theta_cover - 0.5*np.sin(2*theta_cover) + (1/3)*np.sin(theta_cover)**3) / np.sqrt(np.pi)

    # --> fuselage principal Ariane V
    x_fuselage = np.linspace(shape_params["MAIN_FUSELAGE"]["X_START"], shape_params["MAIN_FUSELAGE"]["X_END"], 1000)
    y_fuselage = np.full(shape=len(x_fuselage), fill_value=shape_params["MAIN_FUSELAGE"]["Y"])

    # --> transition fuselage - booster
    theta_transition = np.linspace(np.pi, np.pi/2, 200) 
    x_transition = shape_params["TRANSITION"]["RADIUS"] * np.cos(theta_transition) + shape_params["PENTE"]["X_START"]
    y_transition = shape_params["TRANSITION"]["RADIUS"] * np.sin(theta_transition) + shape_params["COIFFE"]["RADIUS"]

    # --> pente booster
    slope = (shape_params["PENTE"]["Y_END"] - shape_params["PENTE"]["Y_START"]) / (shape_params["PENTE"]["X_END"] - shape_params["PENTE"]["X_START"]) 
    b_slope = shape_params["PENTE"]["Y_START"] - slope * shape_params["PENTE"]["X_START"]
    x_slope = np.linspace(shape_params["PENTE"]["X_START"], shape_params["PENTE"]["X_END"], 800)
    y_slope = slope * x_slope + b_slope

    # --> fuselage booster
    x_booster = np.linspace(shape_params["BOOSTER_FUSELAGE"]["X_START"], shape_params["BOOSTER_FUSELAGE"]["X_END"], 1000)
    y_booster = np.full(shape=len(x_booster), fill_value=shape_params["BOOSTER_FUSELAGE"]["Y"])

    x_shape = np.concatenate([x_cover, x_fuselage, x_transition, x_slope, x_booster])
    y_upper_ = np.concatenate([y_cover, y_fuselage, y_transition, y_slope, y_booster])
    y_lower_ = - y_upper_

    return x_shape, y_upper_, y_lower_