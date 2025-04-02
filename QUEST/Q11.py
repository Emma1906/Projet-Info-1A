import pandas as pd
import os

# Question 11 : Quel est le nombre de victoires par nation, entre 1950 et 2024 ?

# 1 : Jointure des tables
drivers = pd.read_csv("C:/Users/User/Desktop/PROJET INFO/donnees_formule_un/donnees_formule_un/drivers.csv")
drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]
"""print(drivers.columns)"""

results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
results.rename(columns={' driverId': 'driverId'}, inplace=True)
"""print(results.columns)"""

fusion = pd.merge(drivers, results, on="driverId")
"""print(fusion.columns)"""

# 2 : Filtrer les victoires
victoire = fusion[fusion[' positionOrder'] == 1]
"""print(victoire.head())
print(victoire.columns)"""

# 3 : On regrouper par nation et on compte le nombre de victoire
victoire_nation = (
    victoire.groupby('nationality')
    .size()
    .reset_index(name="Nombre de victoires par nation")
    .sort_values(by="Nombre de victoires par nation", ascending=False)
)

print(victoire_nation)