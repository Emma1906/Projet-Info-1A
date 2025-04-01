import pandas as pd

# Question 6 : Qui a remporté le plus de fois le circuit de Spa-Francorchamps,
# entre 1950 et 2024 ?

# ## chargement modification et fusion des tables
drivers = pd.read_csv("C:/Users/User/Desktop/PROJET INFO/donnees_formule_un/donnees_formule_un/drivers.csv")
drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]

results = pd.read_csv("C:/Users/User/Desktop/PROJET INFO/donnees_formule_un/donnees_formule_un/results.csv")
races = pd.read_csv("C:/Users/User/Desktop/PROJET INFO/donnees_formule_un/donnees_formule_un/races.csv")

fusion = pd.merge(results, races, on='raceId')
spa_gagnant = pd.merge(drivers, fusion, on='driverId')
print(spa_gagnant.columns)

# ## tri de la table :
# garder que les courses sur le circuit Spa-Francorchamps
spa_gagnant = spa_gagnant[spa_gagnant['circuitId'] == 13]
# garder que les gagants de la course de Spa_Francorchamps
spa_gagnant = spa_gagnant[spa_gagnant['positionOrder'] == 1]

# on regroupe par pilote et on compte le nombre de victoire
spa_gagnant = (
    spa_gagnant.groupby('nom_complet')
    .size()
    .reset_index(name="Nombre de victoires")  # Renommer la colonne de comptage
    .sort_values(by="Nombre de victoires", ascending=False)  # Trier par nombre de victoires décroissant
)

print(spa_gagnant.head())
