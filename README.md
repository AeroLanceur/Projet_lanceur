# 🚀 Projet d'Aérodynamique Hypersonique

## 👨‍💻 Auteur
**Pierre Lambin**

## 📌 Description
Ce projet vise à étudier l'aérodynamique hypersonique d'un lanceur spatial en utilisant différentes approches, notamment l'analyse géométrique, l'estimation des coefficients aérodynamiques et la gestion des propriétés thermodynamiques.

## 📂 Structure du Projet
Le projet est organisé en plusieurs modules :

### 1. 🏗 **CAO Management**
   - `STL_to_CSV.py` : Conversion de fichiers STL en fichiers CSV.
   - `ShowFigure.py` : Visualisation des figures.
   - `TriangleAndSegment.py` : Gestion des triangles et segments.
   - `vectors_2D.py` : Manipulation des vecteurs 2D.

### 2. 🌬 **Aéro Property**
   - `DragCoeff.py` : Calcul du coefficient de traînée.
   - `LiftCoeff.py` : Calcul du coefficient de portance.
   - `PressureCoeff.py` : Calcul du coefficient de pression.

### 3. 📊 **Graph Management**
   - `EvolAeroCoeff.py` : Évolution des coefficients aérodynamiques.
   - `EvolThermoParams.py` : Évolution des paramètres thermodynamiques.

### 4. ✏ **Profil Configuration**
   - `modelisation.py` : Modélisation du profil étudié.

### 5. 💥 **Gestion des Chocs**
   - `Expansion.py` : Analyse des zones d'expansion.
   - `Oblique.py` : Gestion des chocs obliques.

### 6. 🔥 **Propriétés Thermodynamiques**
   - `AfterShocProperties.py` : Propriétés après un choc.
   - `GammaManagement.py` : Gestion du coefficient gamma.
   - `LocalThermoProperties.py` : Propriétés thermodynamiques locales.
   - `thermo_properties.py` : Gestion générale des propriétés thermodynamiques.

### 7. 📜 **Autres fichiers**
   - `aero_launcher.ipynb` : Notebook pour le calcul aéro.
   - `main_aero.ipynb` : Notebook principal d'analyse aérodynamique.
   - `see_STL.py` : Visualisation des fichiers STL.

## 🔧 Prérequis
- Python 3.x
- Bibliothèques : NumPy, Matplotlib, SciPy, Pandas

## 🏎 Utilisation
Exécuter le fichier principal ou utiliser les notebooks pour explorer les analyses :
```bash
python main_aero.py
```

## 📜 Licence
Projet sous licence libre. Toute utilisation ou modification doit mentionner l'auteur original.

