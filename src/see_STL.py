import matplotlib.pyplot as plt

from CAO_management.vectors_2D import Get_2D_vectors
from CAO_management.STL_to_CSV import Get_CSV
from CAO_management.TriangleAndSegment import TransformCSV
from CAO_management.ShowFigure import ShowLaunchersFigure

csv_file = Get_CSV(stl_name="ArianeV.stl", csv_name="ArianeV.csv")
triangles_ArianeV, segments_ArianeV = TransformCSV(csv_file=csv_file, Y_FIXE=0.0)
Z_launcher, X_launcher = ShowLaunchersFigure(trianglesLauncher=triangles_ArianeV, segmentsLauncher=segments_ArianeV)

x_shape, y_upper_, y_lower_ = Get_2D_vectors()

fig, axs = plt.subplots(1, 1, figsize=(18, 4))

axs.plot(x_shape, y_upper_, 'r', label='Face supérieure')
axs.plot(x_shape, y_lower_, 'b', label="Face inférieure")
axs.grid('on', alpha=0.75, linestyle='-.')
axs.set_xlabel("Hauteur [m]")
axs.set_ylabel("Diamètre [m]")
axs.set_title("Profil 2D du lanceur Ariane V", fontsize=18)

plt.tight_layout()
plt.show()