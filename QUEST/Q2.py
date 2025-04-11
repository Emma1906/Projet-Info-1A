#2 classements des pilotes à l'issue de la saison 2023

#choisir year=2023 dans le dossier races.csv
#prendre la raceId également présent dans results.csv
#additionner les points pour chaque drivers pour chaque course
#faire un classement par points pour chaque pilote

#importation des librairies
import pandas as pd
import os


races = pd.read_csv(os.path.join("donnees_formule_un","races.csv"))
races.columns = races.columns.str.strip()





# Lire le fichier CSV avec Pandas
results = pd.read_csv(os.path.join("donnees_formule_un","results.csv"))
results.columns = results.columns.str.strip()


races_results = pd.merge(races, results, on='raceId')





# Lire le fichier CSV des pilotes avec Pandas (en ignorant les lignes incorrectes si nécessaire)
drivers = pd.read_csv(
    os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()
# Enlever les espaces autour des noms de colonnes


drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]

# Fusion des données
races_results = pd.merge(races, results, on='raceId')
races_results = pd.merge(races_results, drivers[['driverId', 'nom_complet']], on='driverId')

races_results_2023 = races_results[races_results['year'] == 2023]

# Calcul des points totaux
points_totals = races_results_2023.groupby('driverId')['points'].sum().reset_index()

# Comptage des positions (1ère, 2ème, etc.)
positions_counts = races_results_2023.groupby(['driverId', 'positionOrder']).size().unstack(fill_value=0)

# Fusion avec les noms
classement = pd.merge(points_totals, drivers[['driverId', 'nom_complet']], on='driverId')
classement = pd.merge(classement, positions_counts, on='driverId', how='left')

# Remplacer les colonnes vides par 0 si certaines positions ne sont pas occupées
for pos in range(1, 21):
    if pos not in classement.columns:
        classement[pos] = 0

# Tri : d'abord par points, puis 1res places, 2des places, etc.
tri = ['points'] + list(range(1, 21))
classement = classement.sort_values(by=tri, ascending=[False] + [False]*20).reset_index(drop=True)

# Affichage final
colonnes_a_afficher = ['nom_complet', 'points'] + list(range(1, 11))  # on peut afficher que les 10 premières places
print(classement[colonnes_a_afficher])