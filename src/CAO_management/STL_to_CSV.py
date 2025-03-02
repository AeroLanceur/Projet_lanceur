from stl import mesh
import csv
import os


def Get_CSV(stl_name: str, csv_name: str):
    """
    Convertit un fichier STL en fichier CSV contenant les informations des triangles du maillage.

    Cette fonction prend un fichier STL en entrée, extrait les normales et les sommets de chaque triangle 
    composant le maillage, puis enregistre ces informations dans un fichier CSV.

    **Paramètres** :
        - `stl_name` (str) : Nom du fichier STL à convertir (doit être présent dans `docs/STL_files`).
        - `csv_name` (str) : Nom du fichier CSV de sortie (enregistré dans `docs/CSV_files`).

    **Structure du fichier CSV généré** :
        - Colonne "Normale X, Normale Y, Normale Z" : Composantes du vecteur normal du triangle.
        - Colonnes "S1 X, S1 Y, S1 Z" : Coordonnées du premier sommet du triangle.
        - Colonnes "S2 X, S2 Y, S2 Z" : Coordonnées du deuxième sommet du triangle.
        - Colonnes "S3 X, S3 Y, S3 Z" : Coordonnées du troisième sommet du triangle.

    **Conditions et gestion des erreurs** :
        - Vérifie si le fichier STL existe avant de tenter la conversion.
        - Lève une `FileNotFoundError` si le fichier STL est introuvable.

    **Retourne** :
        - `str` : Chemin du fichier CSV généré.
    """
    
    current_dir = os.getcwd()
    stl_dir = os.path.join(current_dir, "..\docs", "STL_files")
    stl_file = os.path.join(stl_dir, stl_name)

    if not os.path.exists(stl_file):
        raise FileNotFoundError(f"Le fichier STL n'existe pas : {stl_file}")

    mesh_data = mesh.Mesh.from_file(stl_file)

    csv_dir = os.path.join(current_dir, "../docs", "CSV_files")
    csv_file = os.path.join(csv_dir, csv_name)

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

    return csv_file