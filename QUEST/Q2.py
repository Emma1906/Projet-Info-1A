#2 classements des pilotes à l'issue de la saison 2023

#choisir year=2023 dans le dossier races.csv
#prendre la raceId également présent dans results.csv
#additionner les points pour chaque drivers pour chaque course
#faire un classement par points pour chaque pilote

#importation des librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os


races = pd.read_csv(os.path.join("donnees_formule_un","races.csv"))






# Lire le fichier CSV avec Pandas
results = pd.read_csv(os.path.join("donnees_formule_un","results.csv"))
results.rename(columns={' raceId': 'raceId'}, inplace=True)
print(results.columns)

races_results = pd.merge(races, results, on='raceId')


print(races_results.columns)

races_results.rename(columns={' driverId': 'driverId'}, inplace=True)

print(races_results.columns)

# Lire le fichier CSV des pilotes avec Pandas (en ignorant les lignes incorrectes si nécessaire)
drivers = pd.read_csv(
    os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')

# Enlever les espaces autour des noms de colonnes
drivers.columns = drivers.columns.str.strip()

drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]
races_results = pd.merge(races_results, drivers, on='driverId')
print(races_results.columns)
print(races_results.head())

races_results_2023 = races_results[races_results[' year'] == 2023]

points_totals = races_results_2023.groupby('driverId')[' points'].sum().reset_index()

# Fusionner les points totaux avec les noms complets des pilotes
points_totals = pd.merge(points_totals, drivers[['driverId', 'nom_complet']], on='driverId')

# Trier les pilotes par nombre de points, du plus grand au plus petit
classement = points_totals.sort_values(by=' points', ascending=False).reset_index(drop=True)

# Afficher les pilotes et leurs points
print(classement[['nom_complet', ' points']])


