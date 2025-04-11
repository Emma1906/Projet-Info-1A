#Quel est le classement des écuries à l’issue de la saison 2023 ?

#importer la table constructors et constructors_standings
#les joindre
#importer races
#grouper par années
#ne garder que les raceId les plus grandes pour chaque année
#sélectionner final position dans constructors_standings pour chaque raceId conservée

import pandas as pd
import os

constructors = pd.read_csv(os.path.join("donnees_formule_un", "constructors.csv"))
constructors.columns = constructors.columns.str.strip()
constructors_standings = pd.read_csv(os.path.join("donnees_formule_un", "constructors_standings.csv"))
constructors_standings.columns = constructors_standings.columns.str.strip()
print(constructors_standings.columns)
print(constructors.columns)
races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()

