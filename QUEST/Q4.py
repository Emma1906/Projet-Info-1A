import pandas as pd
import os
import csv

# Question 4 : Quels sont les meilleurs temps d'un tour de circuit (best lap time) pour
# chaque circuit sur l'année 2023 ?

# PANDA
# Charger et fusionner les tables
laps = pd.read_csv(os.path.join("donnees_formule_un", "lap_times.csv"))
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
fusion = pd.merge(laps, races, on='raceId')
fusion.columns = fusion.columns.str.strip()
# Extraire les années des courses
annees_courses = fusion[['year', 'raceId', 'name']].drop_duplicates()
# Extraire le temps le plus rapide
meilleur_temps_tour_par_course =\
    fusion.groupby(['raceId', 'year'])['milliseconds'].min().reset_index()
# Fusionner à nouveau pour inclure la colonne 'name' (nom de la course)
meilleur_temps_tour_par_course =\
    pd.merge(meilleur_temps_tour_par_course, fusion[['raceId', 'name']], on='raceId',
             how='left').drop_duplicates()
# Filtrer sur l'année 2023
meilleur_temps_tour_par_course_2023 =\
    meilleur_temps_tour_par_course[meilleur_temps_tour_par_course['year'] == 2023]
# Afficher le temps le plus rapide
print("\nMeilleur temps d'un tour par course en 2023 :")
print(meilleur_temps_tour_par_course_2023[['name', 'year', 'milliseconds']])




####### PYTHON PUR

# Lecture et stockage des données 
races_dict = {}
race_ids_2023 = set()

with open(os.path.join("donnees_formule_un", "races.csv"), 'r', encoding='utf-8') as races_file:
    reader = csv.reader(races_file)
    header_races = next(reader)  # lire l'en-tête

    for row in reader:
        try:
            raceId = row[0].strip()
            year = int(row[1].strip())  # Supposons que 'year' soit colonne 1
            if year == 2023:
                races_dict[raceId] = row
                race_ids_2023.add(raceId)
        except (IndexError, ValueError):
            continue  # sauter les lignes malformées

# Lire lap_times.csv et fusionner avec races.csv pour les courses de 2023
with open(os.path.join("donnees_formule_un", "lap_times.csv"), 'r', encoding='utf-8') as laps_file:
    reader = csv.reader(laps_file)
    header_laps = next(reader)

    # Créer un nouveau fichier fusionné
    with open("fusion_2023.csv", 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)

        # Écrire l'en-tête combiné
        writer.writerow(header_laps + header_races)

        for row in reader:
            try:
                raceId = row[0].strip()
                if raceId in race_ids_2023:
                    ligne_fusionnee = row + races_dict[raceId]
                    writer.writerow(ligne_fusionnee)
            except IndexError:
                continue

# Dictionnaire pour stocker le meilleur temps par nom de course
meilleurs_temps = {}  # nom_course -> temps_minimum

# Lire le fichier fusionné pour analyser les temps
with open("fusion_2023.csv", 'r', encoding='utf-8') as fusion_file:
    reader = csv.reader(fusion_file)
    header = next(reader)

    # Afficher un extrait des lignes pour déboguer
    for i, row in enumerate(reader):

        try:
            nom_course = row[10].strip()       # Supposons que le nom soit en colonne 3 (index 3)
            temps_ms = int(row[5].strip())    # Supposons que "milliseconds" soit en colonne 5 (index 5)

            if nom_course not in meilleurs_temps or temps_ms < meilleurs_temps[nom_course]:
                meilleurs_temps[nom_course] = temps_ms

        except (IndexError, ValueError):
            continue  # Ignorer les lignes malformées

# Affichage des résultats
print("Meilleurs temps par course en 2023 :\n")
for nom, temps in meilleurs_temps.items():
    print(f"{nom} : {temps} ms")




