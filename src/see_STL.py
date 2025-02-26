import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.gridspec import GridSpec
from stl import mesh
import csv
import os

## ===== CONVERSION FICHIER .STL VERS FICHIER .CSV ===== ##

current_dir = os.getcwd()
stl_dir = os.path.join(current_dir, "docs", "STL_files")
stl_file = os.path.join(stl_dir, "ArianeV.stl")

if not os.path.exists(stl_file):
    raise FileNotFoundError(f"Le fichier STL n'existe pas : {stl_file}")

mesh_data = mesh.Mesh.from_file(stl_file)

csv_dir = os.path.join(current_dir, "docs", "CSV_files")
csv_file = os.path.join(csv_dir, "ArianeV.csv")

with open(csv_file, mode="w", newline="") as file:
    
    writer = csv.writer(file)

    writer.writerow(["Normale X", "Normale Y", "Normale Z", 
                     "S1 X", "S1 Y", "S1 Z",
                     "S2 X", "S2 Y", "S2 Z",
                     "S3 X", "S3 Y", "S3 Z"])
    
    for i in range(len(mesh_data.normals)):
        normale = mesh_data.normals[i]
        sommet1 = mesh_data.vectors[i][0]
        sommet2 = mesh_data.vectors[i][1]
        sommet3 = mesh_data.vectors[i][2]
        writer.writerow([*normale, *sommet1, *sommet2, *sommet3])
        
print(f"Conversion terminée ! Fichier enregistré sous {csv_file}")

## ===== EXTRACTION DES TRIANGLES POUR LE PROFIL 3D ===== ##

Y_FIXE = 0.0
df = pd.read_csv(csv_file)
triangles = []
for index, row in df.iterrows():
    sommet1 = [row["S1 X"], row["S1 Y"], row["S1 Z"]]
    sommet2 = [row["S2 X"], row["S2 Y"], row["S2 Z"]]
    sommet3 = [row["S3 X"], row["S3 Y"], row["S3 Z"]]
    triangles.append([sommet1, sommet2, sommet3])

## ===== EXTRACTION DES SEGMENTS POUR LE PROFIL 2D ===== ##

def intersection_plan_y(p1, p2, y_fixe):
    if (p1[1] < y_fixe and p2[1] > y_fixe) or (p1[1] > y_fixe and p2[1] < y_fixe):
        t = (y_fixe - p1[1]) / (p2[1] - p1[1])
        x_inter = p1[0] + t * (p2[0] - p1[0])
        z_inter = p1[2] + t * (p2[2] - p1[2])
        return np.array([x_inter, z_inter])
    return None

segments = []
for tri in triangles:
    points_inter = []
    for i in range(3):
        p1, p2 = tri[i], tri[(i + 1) % 3]
        inter = intersection_plan_y(p1, p2, Y_FIXE)
        if inter is not None:
            points_inter.append(inter)
    
    if len(points_inter) == 2:
        segments.append(points_inter)

## ===== TRACER DES FIGURES 3D ET 2D ===== ##

fig = plt.figure(figsize=(20, 12))
gs = GridSpec(2, 1, figure=fig)

    # --> FIGURE 3D
ax_3D = fig.add_subplot(gs[0, :], projection='3d') 
poly3d = Poly3DCollection(triangles, alpha=1.0, facecolor="cyan", edgecolor="k")
all_points = np.array(triangles).reshape(-1, 3)
ax_3D.add_collection3d(poly3d)
ax_3D.set_xlim([all_points[:, 0].min(), all_points[:, 0].max()])
ax_3D.set_ylim([all_points[:, 1].min(), all_points[:, 1].max()])
ax_3D.set_zlim([all_points[:, 2].min(), all_points[:, 2].max()])

ax_3D.set_xlabel("X")
ax_3D.set_ylabel("Y")
ax_3D.set_zlabel("Z")
ax_3D.set_title("Visualisation du modèle 3D à partir du CSV")
ax_3D.view_init(elev=0, azim=45)
ax_3D.set_box_aspect([1.25, 1.25, 4])  

    # --> FIGURE 2D
ax_2D = fig.add_subplot(gs[1, :]) 
for seg in segments:
    ax_2D.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], 'k-')

ax_2D.set_xlabel("X")
ax_2D.set_ylabel("Z")
ax_2D.set_title(f"Coupe 2D du modèle dans le plan ZX à Y = {Y_FIXE}")
ax_2D.axis("equal")
ax_2D.grid(True)

plt.show()