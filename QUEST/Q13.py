#Quel pilote a eu le plus d'accidents en fonction des années ?

#importer status, et results
#les joindre grace à statusId
#importer races 
#joindre grâce à raceId
#grouper par année et pilote
#compter le nombre d'accidents pour chaque pilote
#trier par année et nombre d'accidents
#importer drivers et merge pour avoir leur nom 

import pandas as pd
import os



status = pd.read_csv(os.path.join("donnees_formule_un", "status.csv"))
status.columns = status.columns.str.strip()


results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))    
results.columns = results.columns.str.strip()

races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()


drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()

drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]




fusion = pd.merge(results, status, on='statusId')
fusion.columns = fusion.columns.str.strip()



fusion_now = pd.merge(fusion, races, on='raceId')
fusion_now.columns = fusion_now.columns.str.strip()

fusion_v2 = pd.merge(fusion_now, drivers[['driverId', 'nom_complet']], on='driverId')
fusion_v2.columns = fusion_v2.columns.str.strip()



#compter le nombre d'accidents pour chaque pilote, status = Accident
fusion_v2['status'] = fusion_v2['status'].str.strip().str.replace('"', '')
fusion_v2 = fusion_v2[fusion_v2['status'] == "Accident"]


# Compter le nombre d'accidents par pilote et par année
accidents_par_pilote = fusion_v2.groupby(['year', 'driverId']).size().reset_index(name='nb_accidents')

# Garder le pilote avec le plus d'accidents par année
accidents_max = accidents_par_pilote.loc[accidents_par_pilote.groupby('year')['nb_accidents'].idxmax()]

# Ajouter le nom du pilote
accidents_max = accidents_max.merge(drivers[['driverId', 'nom_complet']], on='driverId', how='left')

# Garder les colonnes finales
accidents_max = accidents_max[['year', 'nom_complet', 'nb_accidents']]

# Afficher
print(accidents_max.sort_values('year'))











