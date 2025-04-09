import pandas as pd
import os

#1 pilotes qui ont gagné au moins 30 courses


# Lire le fichier CSV avec Pandas
results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
results.columns = results.columns.str.strip()

def pilotes_30_victoires(results):
    # Compter le nombre de victoires par pilote
    victoires = results[results['positionOrder'] == 1].groupby('driverId').size()

    # Filtrer les pilotes ayant gagné au moins 30 courses
    pilotes_30_victoires = victoires[victoires >= 30].index

    return pilotes_30_victoires


# Lire le fichier CSV avec Pandas

drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"))

drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()
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
print(nom_30_victoires)