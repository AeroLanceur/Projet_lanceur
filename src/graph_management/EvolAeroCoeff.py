import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def Show_AeroCoeff(cst_dict, DragCoeff, LiftCoeff, x_shape, DragComponent):

    # arguments manager
            # --> constante de la simulation
    Mach_inf = cst_dict["INF_CST"]["MACH"]
    AoA = cst_dict["AoA"]
    inf_cst = cst_dict["INF_CST"]

        # --> coefficient de traînée
            # --> face supérieure
    Cd_frott_upper = DragCoeff["UPPER"]["FROTTEMENT"]
    Cd_press_upper = DragCoeff["UPPER"]["PRESSION"]
    Cd_wave_upper = DragCoeff["UPPER"]["ONDE"]
            # --> face inférieure
    Cd_frott_lower = DragCoeff["LOWER"]["FROTTEMENT"]
    Cd_press_lower = DragCoeff["LOWER"]["PRESSION"]
    Cd_wave_lower = DragCoeff["LOWER"]["ONDE"]
            # traînée totale
    Cd_tot_frott = DragCoeff["TOTAL"]["FROTTEMENT"]
    Cd_tot_pression = DragCoeff["TOTAL"]["PRESSION"]
    Cd_tot_wave = DragCoeff["TOTAL"]["ONDE"]
    Cd_tot = DragCoeff["TOTAL"]["ALL"]

        # --> coefficient de portance
    Cl_x_upper = LiftCoeff["UPPER"]
    Cl_x_lower = LiftCoeff["LOWER"]
    CL_x = LiftCoeff["TOTAL"]

        # --> composition de la traînée de frottement
            # --> face supérieure
    Cf_upper = DragComponent["UPPER"]["CF"]
    tau_w_upper = DragComponent["UPPER"]["TAU_W"]
    Re_upper = DragComponent["UPPER"]["RE"]
            # --> face inférieure
    Cf_lower = DragComponent["LOWER"]["CF"]
    tau_w_lower = DragComponent["LOWER"]["TAU_W"]
    Re_lower = DragComponent["LOWER"]["RE"]

    fig = plt.figure(figsize=(18, 15))
    fig.suptitle(f"Évolution des coefficients aérodynamiques (AoA = {np.rad2deg(AoA):.2f}°, Mach = {Mach_inf:.2f} et Z = {inf_cst['ALTITUDE']*1e-3:.4f} km)", fontsize=20)
    gs = GridSpec(4, 3, figure=fig)

    merged_ax = fig.add_subplot(gs[1, :])
    Drag_ax = fig.add_subplot(gs[2, :])#, sharex=merged_ax)
    Lift_ax = fig.add_subplot(gs[3, :])#, sharex=merged_ax)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x_shape, Cf_upper, 'r-.', label="Face inférieure")
    ax1.plot(x_shape, Cf_lower, 'b--', label="Face supérieure")
    ax1.grid('on', alpha=0.75, linestyle='-.')
    ax1.set_xlabel("Hauteur [m]", fontsize=14)
    ax1.set_ylabel(r"Coefficient de frottement $C_f$", fontsize=14)
    ax1.legend(loc="best")

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(x_shape, tau_w_upper, 'r-.', label="Fasce inférieure")
    ax2.plot(x_shape, tau_w_lower, 'b--', label="Face supérieure")
    ax2.grid('on', alpha=0.75, linestyle='-.')
    ax2.set_xlabel("Hauteur [m]", fontsize=14)
    ax2.set_ylabel(r"Contrainte pariétale $\tau_\omega$", fontsize=14)
    ax2.legend(loc="best")

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(x_shape, Re_upper, 'r-.', label=r"$Re_x$ face supérieure")
    ax3.plot(x_shape, Re_lower, 'b--', label=r"$Re_x$ face inférieure")
    ax3.set_xlabel("Hauteur [m]", fontsize=14)
    ax3.set_ylabel("Reynolds", fontsize=14)
    ax3.grid('on', alpha=0.75, linestyle='-.')
    ax3.set_yscale('log')
    ax3.legend()

    merged_ax.plot(x_shape, Cd_frott_upper, 'r-.', label=r"$C_{frottement}$ face supérieure")
    merged_ax.plot(x_shape, Cd_frott_lower, 'b-.', label=r"$C_{frottement}$ face inférieure")

    merged_ax.plot(x_shape[::50], Cd_press_upper[::50], c='orange', linestyle=':', marker='*', fillstyle='none', markersize=10, label=r"$C_{pression}$ face supérieure")
    merged_ax.plot(x_shape[::50], Cd_press_lower[::50], c='green', linestyle=':', marker='d', fillstyle='none', markersize=10, label=r"$C_{pression}$ face inférieure")

    merged_ax.plot(x_shape[::50], Cd_wave_upper[::50], c='purple', linestyle=':', marker='v', fillstyle='none', markersize=10, label=r"$C_{onde}$ face supérieure")
    merged_ax.plot(x_shape[::50], Cd_wave_lower[::50], c='olive', linestyle=':', marker='>', fillstyle='none', markersize=10, label=r"$C_{onde}$ face inférieure")

    merged_ax.set_ylabel("Coefficient de traînée", fontsize=14)
    merged_ax.grid('on', alpha=0.75, linestyle='-.')
    merged_ax.legend(loc="best", ncol=2)

    Drag_ax.plot(x_shape[::50], Cd_tot[::50], 'r', linestyle=':', marker='*', fillstyle='none', markersize=10, label=r"Traînée totale")
    Drag_ax.plot(x_shape, Cd_tot_frott, 'b', label=r"Traînée frottement")
    Drag_ax.plot(x_shape, Cd_tot_pression, 'orange', label=r"Traînée pression")
    Drag_ax.plot(x_shape, Cd_tot_wave, 'purple', label=r"Traînée onde")
    Drag_ax.set_ylabel("Coefficient de traînée totale", fontsize=14)
    Drag_ax.grid('on', alpha=0.75, linestyle='-.')
    Drag_ax.legend(loc="best", ncol=2)

    Lift_ax.plot(x_shape[::50], Cl_x_upper[::50], 'r', linestyle='-.', marker='*', fillstyle='none', markersize=15, label=r"$C_{L}$ face supérieure")
    Lift_ax.plot(x_shape[::50], Cl_x_lower[::50], 'b', linestyle=':', marker='d', fillstyle='none', markersize=10, label=r"$C_{L}$ face inférieure")
    Lift_ax.plot(x_shape[::50], CL_x[::50], 'k', linestyle='--', marker='p', fillstyle='none', markersize=10, label=r"$C_{L}$ total")
    Lift_ax.set_xlabel("Hauteur [m]", fontsize=14)
    Lift_ax.set_ylabel("Coefficient de portance totale", fontsize=14)
    Lift_ax.grid('on', alpha=0.75, linestyle='-.')
    Lift_ax.legend(loc="best")

    plt.tight_layout()
    plt.show()