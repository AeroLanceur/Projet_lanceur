import numpy as np
import pandas as pd

def TransformCSV(csv_file: str, Y_FIXE: float):
    """
    Transforme un fichier CSV contenant un maillage 3D en une structure exploitable pour l'affichage 3D et 2D.

    Cette fonction lit un fichier CSV contenant les informations d'un maillage STL converti. 
    Elle extrait les triangles définissant le maillage, applique une transformation d'échange des axes (X ↔ Z) 
    et calcule les intersections avec le plan `Y = Y_FIXE` pour obtenir une coupe 2D du modèle.

    **Paramètres** :
        - `csv_file` (str) : Chemin du fichier CSV contenant le maillage 3D.
        - `Y_FIXE` (float) : Valeur de Y pour laquelle la coupe 2D sera extraite.

    **Traitements effectués** :
        1. **Lecture du fichier CSV** et extraction des coordonnées des triangles (S1, S2, S3).
        2. **Conversion en mètres** (multiplication par `1e-3` si les données sont en millimètres).
        3. **Échange des axes X et Z** pour adapter à la convention de tracé.
        4. **Détermination des segments d'intersection avec le plan `Y = Y_FIXE`** :
           - Chaque arête des triangles est testée pour voir si elle coupe ce plan.
           - Si oui, le point d'intersection est calculé.
           - Si un triangle coupe le plan en deux points, un segment est enregistré.

    **Retourne** :
        - `triangles` (list) : Liste des triangles du maillage 3D sous forme de listes de trois sommets `[S1, S2, S3]`.
        - `segments` (list) : Liste des segments 2D résultant de la coupe du modèle dans le plan `Y = Y_FIXE`.
    """

    df = pd.read_csv(csv_file)

    Z_max = max(df["S1 Z"].max(), df["S2 Z"].max(), df["S3 Z"].max())
    df["S1 Z"] = Z_max - df["S1 Z"]
    df["S2 Z"] = Z_max - df["S2 Z"]
    df["S3 Z"] = Z_max - df["S3 Z"]

    triangles = []
    for index, row in df.iterrows():
        sommet1 = np.array([row["S1 X"], row["S1 Y"], row["S1 Z"]]) * 1e-3
        sommet2 = np.array([row["S2 X"], row["S2 Y"], row["S2 Z"]]) * 1e-3
        sommet3 = np.array([row["S3 X"], row["S3 Y"], row["S3 Z"]]) * 1e-3
        triangles.append([sommet1, sommet2, sommet3])

    for i in range(len(triangles)):
        for j in range(3):
            triangles[i][j][0], triangles[i][j][2] = triangles[i][j][2], triangles[i][j][0]


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

    for i in range(len(segments)):
        for j in range(2): 
            segments[i][j][0], segments[i][j][1] = segments[i][j][1], segments[i][j][0]

    return triangles, segments