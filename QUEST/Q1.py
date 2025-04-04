import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import seaborn as sns


#1 pilotes qui ont gagné au moins 30 courses


chemin_fichier_results = "C:/Users/emmag/OneDrive/Bureau/Documents/Projet info 1A/Projet-Info-1A/donnees_formule_un/results.csv"

# Lire le fichier CSV avec Pandas
results = pd.read_csv(chemin_fichier_results)

def pilotes_30_victoires(results):
    # Compter le nombre de victoires par pilote
    victoires = results[results['positionOrder'] == 1].groupby('driverId').size()
    
    # Filtrer les pilotes ayant gagné au moins 30 courses
    pilotes_30_victoires = victoires[victoires >= 30].index
    
    return pilotes_30_victoires

chemin_fichier_drivers = "C:\\Users\\emmag\\OneDrive\\Bureau\\Documents\\Projet info 1A\\Projet-Info-1A\\donnees_formule_un\\drivers.csv"

# Lire le fichier CSV avec Pandas
drivers = pd.read_csv(chemin_fichier_drivers)

#cherchons le nom des pilotes qui ont gagné au moins 30 courses

def nom_pilotes_30_victoires(results, drivers):
    pilotes_30_victoire = pilotes_30_victoires(results)
    
    # Filtrer le DataFrame des pilotes pour obtenir les noms
    pilotes_info = drivers[drivers['driverId'].isin(pilotes_30_victoire)]\
        [['forename','surname', 'driverId']]
    victoires = results[results['positionOrder'] == 1].groupby('driverId').size()
    pilotes_info['victoires'] = pilotes_info['driverId'].map(victoires)
    noms_pilotes_victoires = pilotes_info.apply(
        lambda row: f"{row['forename']} {row['surname']} ({row['victoires']} victoires)", axis=1
    ).tolist()
    
    return noms_pilotes_victoires

nom_30_victoires = nom_pilotes_30_victoires(results, drivers)
print (nom_30_victoires)