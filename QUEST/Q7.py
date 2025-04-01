# 7 temps moyen des pits stop en fonction des écuries en 2023 ?
from pandas import read_csv
import pandas as pd

# On va faire un groupby sur le nom de l'écurie
chemin_fichier_ps = (
    r"C:\Users\djoud\OneDrive\Bureau\ENSAI\1A\projet\Projet info\Projet-Info-1A"
    r"\donnees_formule_un\pit_stops.csv"
)
read_csv(chemin_fichier_ps)
df_pits_stops = read_csv(chemin_fichier_ps)


chemin_fichier_races = (
    r"C:\Users\djoud\OneDrive\Bureau\ENSAI\1A\projet\Projet info\Projet-Info-1A"
    r"\donnees_formule_un\races.csv"
)
read_csv(chemin_fichier_races)
df_races = read_csv(chemin_fichier_races)

chemin_fichier_consresults = (
    r"C:\Users\djoud\OneDrive\Bureau\ENSAI\1A\projet\Projet info\Projet-Info-1A"
    r"\donnees_formule_un\constructor_results.csv"
)
read_csv(chemin_fichier_consresults)
df_consresults = read_csv(chemin_fichier_consresults)

chemin_fichier_constructors = (
    r"C:\Users\djoud\OneDrive\Bureau\ENSAI\1A\projet\Projet info\Projet-Info-1A"
    r"\donnees_formule_un\constructors.csv"
)
read_csv(chemin_fichier_constructors)
df_constructors = read_csv(chemin_fichier_constructors)


df_pits_stops_races = pd.merge(df_pits_stops, df_races, on="raceId")
df_pits_stops_consresults = pd.merge(df_pits_stops_races, df_consresults, on="raceId")
df_pits_stops_constructors = pd.merge(
    df_pits_stops_consresults, df_constructors, on="constructorId"
)
# df_pits_stop_races est la jointure de :
# pit_stop + races + constructor_results + constructors


df_pits_stops_constructors_2023 = df_pits_stops_constructors[
    df_pits_stops_constructors["year"] == 2023
]

print(df_pits_stops_constructors_2023.head())
# On va faire la moyenne sur le temps des pits stop en fonction de l'écurie
