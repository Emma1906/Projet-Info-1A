import pandas as pd
import os

# Question 9 : Quel circuit a été le plus de fois concouru, depuis 1950 ?

# 1 : Chargement et jointure des tables
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
"""print(races.columns)"""
circuits = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
"""print(circuits.columns)"""
fusion = pd.merge(races, circuits, on='raceId')
"""print(fusion.columns)"""

# 2 : On regroupe par circuit et on compte le nombre de fois où il a était concurru
nb_fois_circuit = (
    fusion.groupby(' name                           _x')
    .size()
    .reset_index(name="Nombre de fois où le circuit a été concurru")
    .sort_values(by="Nombre de fois où le circuit a été concurru", ascending=False)
)

print(nb_fois_circuit.head())