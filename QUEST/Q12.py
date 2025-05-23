import pandas as pd
import os
from datetime import datetime

# 1 : Chargement et fusion des tables
drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
results.columns = results.columns.str.strip()
fusion_1 = pd.merge(drivers, results, on='driverId')

races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()
fusion_2 = pd.merge(fusion_1, races, on='raceId')

# 2 : Vérifier les doublons
drivers_unique = fusion_2.drop_duplicates(subset=["driverId"])
"""print(drivers_unique.duplicated(subset=["driverId"]).sum())"""

# 3 : Filtrer sur l'année 2023
driver_unique_2023 = drivers_unique[drivers_unique['year'] == 2023].copy()
driver_unique_2023.columns = driver_unique_2023.columns.str.strip()
"""print(driver_unique_2023.columns)"""

# 4 : Convertir la date de naissance en format datetime
driver_unique_2023['dob'] = driver_unique_2023['dob'].str.strip().str.replace('"', '')
driver_unique_2023['dob'] = pd.to_datetime(driver_unique_2023['dob'], format='%Y-%m-%d', errors='coerce')
driver_unique_2023.loc[:, 'dob'] = pd.to_datetime(driver_unique_2023['dob'])
driver_unique_2023[driver_unique_2023['dob'].isna()]


# 5 : Calcul de l'âge
aujourdhui = datetime.now()
driver_unique_2023.loc[:, 'age'] = driver_unique_2023['dob'].apply(
    lambda x: aujourdhui.year - x.year - ((aujourdhui.month, aujourdhui.day) < (x.month, x.day))
)

# 6 : Calcul de l'âge moyen
age_moyen = driver_unique_2023['age'].mean()
print(f"L'âge moyen des pilotes en 2023 est de {age_moyen:.2f} ans")


# Idem pour l'année 2000 :
driver_unique_2000 = drivers_unique[drivers_unique['year'] == 2000].copy()
driver_unique_2000.columns = driver_unique_2000.columns.str.strip()
driver_unique_2000['dob'] = driver_unique_2000['dob'].str.strip().str.replace('"', '')
driver_unique_2000['dob'] = pd.to_datetime(driver_unique_2000['dob'], format='%Y-%m-%d', errors='coerce')
driver_unique_2000.loc[:, 'dob'] = pd.to_datetime(driver_unique_2000['dob'])
driver_unique_2000[driver_unique_2000['dob'].isna()]
aujourdhui_2000 = datetime(2000, 1, 1)  # Date du 1er janvier 2000
driver_unique_2000.loc[:, 'age'] = driver_unique_2000['dob'].apply(
    lambda x: aujourdhui_2000.year - x.year - ((aujourdhui.month, aujourdhui.day) < (x.month, x.day))
)
age_moyen = driver_unique_2000['age'].mean()
print(f"L'âge moyen des pilotes en 2000 est de {age_moyen:.2f} ans")


# Idem pour l'année 1980 :
driver_unique_1980 = drivers_unique[drivers_unique['year'] == 1980].copy()
driver_unique_1980.columns = driver_unique_1980.columns.str.strip()
driver_unique_1980['dob'] = driver_unique_1980['dob'].str.strip().str.replace('"', '')
driver_unique_1980['dob'] = pd.to_datetime(driver_unique_1980['dob'], format='%Y-%m-%d', errors='coerce')
driver_unique_1980.loc[:, 'dob'] = pd.to_datetime(driver_unique_1980['dob'])
driver_unique_1980[driver_unique_1980['dob'].isna()]
aujourdhui_1980 = datetime(1980, 1, 1)  # Date du 1er janvier 1980
driver_unique_1980.loc[:, 'age'] = driver_unique_1980['dob'].apply(
    lambda x: aujourdhui_1980.year - x.year - ((aujourdhui.month, aujourdhui.day) < (x.month, x.day))
)
age_moyen = driver_unique_1980['age'].mean()
print(f"L'âge moyen des pilotes en 1980 est de {age_moyen:.2f} ans")

# Idem pour l'année 1950 :
driver_unique_1950 = drivers_unique[drivers_unique['year'] == 1950].copy()
driver_unique_1950.columns = driver_unique_1950.columns.str.strip()
driver_unique_1950['dob'] = driver_unique_1950['dob'].str.strip().str.replace('"', '')
driver_unique_1950['dob'] = pd.to_datetime(driver_unique_1950['dob'], format='%Y-%m-%d', errors='coerce')
driver_unique_1950.loc[:, 'dob'] = pd.to_datetime(driver_unique_1950['dob'])
driver_unique_1950[driver_unique_1950['dob'].isna()]
aujourdhui_1950 = datetime(1950, 1, 1)  # Date du 1er janvier 1950
driver_unique_1950.loc[:, 'age'] = driver_unique_1950['dob'].apply(
    lambda x: aujourdhui_1950.year - x.year - ((aujourdhui.month, aujourdhui.day) < (x.month, x.day))
)
age_moyen = driver_unique_1950['age'].mean()
print(f"L'âge moyen des pilotes en 1950 est de {age_moyen:.2f} ans")
