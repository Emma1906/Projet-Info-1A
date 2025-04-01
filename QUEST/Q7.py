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

chemin_fichier_consresults = (
    r"C:\Users\djoud\OneDrive\Bureau\ENSAI\1A\projet\Projet info\Projet-Info-1A"
    r"\donnees_formule_un\constructor_results.csv"
)
df_consresults = read_csv(chemin_fichier_consresults)
print(df_consresults.columns)
print(pints)

chemin_fichier_constructors = (
    r"C:\Users\djoud\OneDrive\Bureau\ENSAI\1A\projet\Projet info\Projet-Info-1A"
    r"\donnees_formule_un\constructors.csv"
)
read_csv(chemin_fichier_constructors)
df_constructors = read_csv(chemin_fichier_constructors)


