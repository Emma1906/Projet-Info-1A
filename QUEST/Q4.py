import pandas as pd
import os

# Question 4 : quels sont les meilleurs temps d'un tour de circuit pour
# chaque circuit sur l'année 2023 ?

# charger et fusionner les tables
laps = pd.read_csv(os.path.join("donnees_formule_un", "lap_times.csv"))
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
fusion = pd.merge(laps, races, on='raceId')

print(fusion.columns)

# Extraire les années des courses
annees_courses = fusion[[' year', 'raceId', ' name                           ']].drop_duplicates()

# Extraire le temps le plus rapide
meilleur_temps_tour_par_course =\
    fusion.groupby(['raceId', ' year'])[' milliseconds'].min().reset_index()

# Fusionner à nouveau pour inclure la colonne 'name' (nom de la course)
meilleur_temps_tour_par_course =\
    pd.merge(meilleur_temps_tour_par_course, fusion[['raceId', ' name                           ']], on='raceId',
             how='left').drop_duplicates()

# Filtrer sur une année
meilleur_temps_tour_par_course_2023 =\
    meilleur_temps_tour_par_course[meilleur_temps_tour_par_course[' year'] == 2023]

# Afficher le temps le plus rapide
print("\nMeilleur temps d'un tour par course en 2023 :")
print(meilleur_temps_tour_par_course_2023[[' name                           ', ' year', ' milliseconds']])
