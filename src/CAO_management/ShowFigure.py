
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.gridspec import GridSpec

def ShowLaunchersFigure(trianglesLauncher, segmentsLauncher):
    """
    Affiche les visualisations 3D et 2D d'un lanceur à partir d'un maillage STL converti.

    Cette fonction affiche deux figures :
    1. **Une vue 3D** du lanceur, générée à partir des triangles du maillage.
    2. **Une coupe 2D dans le plan XZ**, obtenue en extrayant les segments intersectant un plan donné.

    **Paramètres** :
        - `trianglesLauncher` (list) : Liste des triangles définissant le maillage 3D du lanceur.
          Chaque triangle est une liste de trois sommets `[S1, S2, S3]`, où `S1, S2, S3` sont des coordonnées (X, Y, Z).
        - `segmentsLauncher` (list) : Liste des segments obtenus après intersection avec un plan donné.
          Chaque segment est une liste de deux points `[P1, P2]`, où `P1` et `P2` sont des coordonnées (X, Z).

    **Visualisation générée** :
        - Une **vue 3D** avec `Poly3DCollection` pour afficher le lanceur en volume.
        - Une **vue 2D** avec `matplotlib` pour afficher la coupe dans le plan XZ.
        - Un **tracé final (X, Z)** affichant les contours du lanceur en 2D.

    **Retourne** :
        - `X_launcher` (numpy.ndarray) : Tableau contenant les coordonnées X des points du profil 2D.
        - `Z_launcher` (numpy.ndarray) : Tableau contenant les coordonnées Z des points du profil 2D.
    """
    
    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec(2, 1, figure=fig)

    ax_3D = fig.add_subplot(gs[0, :], projection='3d') 
    poly3d = Poly3DCollection(trianglesLauncher, alpha=0.6, facecolor="lightblue", edgecolor="k", linewidths=0.2)
    ax_3D.add_collection3d(poly3d)

    all_points = np.array(trianglesLauncher).reshape(-1, 3)
    ax_3D.set_xlim([all_points[:, 0].min(), all_points[:, 0].max()])
    ax_3D.set_ylim([all_points[:, 1].min(), all_points[:, 1].max()])
    ax_3D.set_zlim([all_points[:, 2].min(), all_points[:, 2].max()])

    ax_3D.set_xlabel('Hauteur [m]')
    ax_3D.set_ylabel('Diamètre [m]')
    ax_3D.set_zlabel('Diamètre [m]')
    ax_3D.set_title("Visualisation 3D à partir de la CAO", fontsize=20)
    ax_3D.view_init(elev=20, azim=70)
    ax_3D.set_box_aspect([8, 3, 3])  

    ax_2D = fig.add_subplot(gs[1, :]) 
    for seg in segmentsLauncher:
        ax_2D.plot([seg[0][1], seg[1][1]], [seg[0][0], seg[1][0]], c='navy')

    ax_2D.set_xlabel('Hauteur [m]')
    ax_2D.set_ylabel('Diamètre [m]')
    ax_2D.set_title(f"Visualisation 2D à partir de la CAO, plan XZ", fontsize=20)
    ax_2D.grid(True)

    plt.tight_layout()
    plt.show()

    X_launcher = np.array(segmentsLauncher)[:, :, 0].ravel()
    Z_launcher = np.array(segmentsLauncher)[:, :, 1].ravel()

    fig, axs = plt.subplots(1, 1, figsize=(20, 6))
    axs.set_title("Visualisation du profil 2D après aplatissement des vecteurs X et Z", fontsize=20)
    axs.plot(Z_launcher, X_launcher, c='navy')
    axs.grid('on', alpha=0.75, linestyle='-.')
    axs.set_xlabel('Hauteur [m]')
    axs.set_ylabel('Diamètre [m]')

    return X_launcher, Z_launcher