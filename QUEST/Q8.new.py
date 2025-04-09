import pandas as pd
import os

# Question 8 : Quel est le temps moyen des pit stop en 2023 et en 2013 ?
# (On ne dispose pas de la durée des pit stop avant 2011)

# Chargement et fusion des tables
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
pit = pd.read_csv(os.path.join("donnees_formule_un", "pit_stops.csv"))
fusion = pd.merge(races, pit, on='raceId')
fusion.columns = fusion.columns.str.strip()

pit_2023 = fusion[fusion['year'] == 2023]
pit_2020 = fusion[fusion['year'] == 2020]
pit_2016 = fusion[fusion['year'] == 2016]
pit_2013 = fusion[fusion['year'] == 2013]


# Filtre pour retirer les temps abérrants, des valeurs extrêmes
def filtrer_pit_stops(df):
    q1 = df['milliseconds'].quantile(0.01)
    q99 = df['milliseconds'].quantile(0.99)
    limite_superieure = min(q99, 30000)  # max 30 sec (ce qui est déjà très élevé, pour s'assurer de filtrer les valeurs extrêmes)
    return df[(df['milliseconds'] >= q1) & (df['milliseconds'] <= limite_superieure)]


pit_2023_filtre = filtrer_pit_stops(pit_2023)
pit_2020_filtre = filtrer_pit_stops(pit_2020)
pit_2016_filtre = filtrer_pit_stops(pit_2016)
pit_2013_filtre = filtrer_pit_stops(pit_2013)

# Calcul des moyennes filtrées
moy_2023_filtre = pit_2023_filtre['milliseconds'].mean()
moy_2020_filtre = pit_2020_filtre['milliseconds'].mean()
moy_2016_filtre = pit_2016_filtre['milliseconds'].mean()
moy_2013_filtre = pit_2013_filtre['milliseconds'].mean()

print(f"Temps moyen (filtré) des pit stops en 2023 : {moy_2023_filtre:.0f} ms")
print(f"Temps moyen (filtré) des pit stops en 2020 : {moy_2020_filtre:.0f} ms")
print(f"Temps moyen (filtré) des pit stops en 2016 : {moy_2016_filtre:.0f} ms")
print(f"Temps moyen (filtré) des pit stops en 2013 : {moy_2013_filtre:.0f} ms")
