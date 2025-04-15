#Quel est le classement des écuries à l’issue de la saison 2023 ?

#importer la table constructors et constructors_standings
#les joindre
#importer races
#grouper par années
#ne garder que les raceId les plus grandes pour chaque année
#sélectionner final position dans constructors_standings pour chaque raceId conservée

import pandas as pd
import os

#importer les tables
constructors = pd.read_csv(os.path.join("donnees_formule_un", "constructors.csv"))
constructors.columns = constructors.columns.str.strip()
constructors_standings = pd.read_csv(os.path.join("donnees_formule_un", "constructor_standings.csv"))
constructors_standings.columns = constructors_standings.columns.str.strip()
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()


#fusion des tables
fusion = pd.merge(constructors_standings, races, on='raceId')
fusion = fusion[['raceId', 'constructorId', 'points', 'position', 'year']]
fusion_now = pd.merge(fusion, constructors, on='constructorId')
print(fusion_now.columns)



# Trouver le dernier raceId (la dernière course) pour chaque année
dernieres_courses = fusion_now.groupby('year')['raceId'].max().reset_index()

# Filtrer pour ne garder que les lignes correspondant à ces dernières courses
fusion_finale = pd.merge(fusion_now, dernieres_courses, on=['year', 'raceId'])

fusion_finale = fusion_finale[fusion_finale['position'].isin([1,2,3]) ]
fusion_finale = fusion_finale[['year', 'constructorId', 'name', 'points', 'position']]
fusion_finale = fusion_finale.sort_values(by=['year', 'position'])

print(fusion_finale)
