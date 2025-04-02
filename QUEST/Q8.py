import pandas as pd
import os

# Question 8 : Quel est le temps moyen des pit stop en 2023 et en 2013 ?
# (On ne dispose pas de la durée des pit stop avant 2011)

# 1 : Chargement et fusion des tables
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
pit = pd.read_csv(os.path.join("donnees_formule_un", "pit_stops.csv"))
fusion = pd.merge(races, pit, on='raceId')

# enlever les espaces dans les noms de colonnes
fusion.columns = fusion.columns.str.strip()

# 2 : Filtrer sur l'année 2023
pit_2023 = fusion[fusion['year'] == 2023]

# 3 : Faire la moyenne des temps des pit stop
moyen_2023 = pit_2023['milliseconds'].mean()
print(f"Le temps moyen des pit stops en 2023 est de {moyen_2023:.0f} millisecondes")

# Idem pour l'année 2013
pit_2013 = fusion[fusion['year'] == 2013]
moyen_2013 = pit_2013['milliseconds'].mean()
print(f"Le temps moyen des pit stops en 2013 est de {moyen_2013:.0f} millisecondes")
