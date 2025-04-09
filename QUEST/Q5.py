import pandas as pd
import os

# Charger et fusionner les tables
laps = pd.read_csv(os.path.join("donnees_formule_un", "lap_times.csv"))
laps.columns = laps.columns.str.strip()
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()
fusion = pd.merge(laps, races, on='raceId')

# Correction des noms de colonnes si nécessaire
fusion.rename(columns={' driverId': 'driverId'}, inplace=True)
fusion.rename(columns={' name                           ': 'name'}, inplace=True)
fusion.rename(columns={' milliseconds': 'milliseconds'}, inplace=True)
fusion.rename(columns={' year': 'year'}, inplace=True)

drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()
drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]

# Fusionner les données avec les pilotes
fusionnow = pd.merge(fusion, drivers[['driverId', 'nom_complet']], on='driverId')

# Extraire les meilleurs temps par course
meilleur_temps_tour_par_course = (
    fusionnow.loc[fusionnow.groupby(['raceId', 'year'])['milliseconds'].idxmin()]
)

# Filtrer sur l'année 2023
meilleur_temps_tour_par_course_2023 = meilleur_temps_tour_par_course[
    meilleur_temps_tour_par_course['year'] == 2023
]
# regroupe par pilote
meilleur_temps_par_pilote = (
    meilleur_temps_tour_par_course_2023.groupby('nom_complet').size().reset_index(name='Nombre de meilleurs temps')
    .sort_values(by='Nombre de meilleurs temps', ascending=False)
)

print("\nNombre de meilleurs temps par pilote en 2023 :")
print(meilleur_temps_par_pilote)

