import pandas as pd
import os

# Charger les données
df_results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))

df_races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))

df_circuits = pd.read_csv(os.path.join("donnees_formule_un", "circuits.csv"), on_bad_lines='skip')

df_drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')

# Nettoyage des colonnes
df_results.columns = df_results.columns.str.strip()

df_races.columns = df_races.columns.str.strip()

df_circuits.columns = df_circuits.columns.str.strip()

df_drivers.columns = df_drivers.columns.str.strip()

# Ajouter deux colonnes pour séparer les données de "time"
df_results["time_with_plus"] = df_results["time"].where(
    df_results["time"].astype(str).str.contains(r"\+"), None
)
df_results["time_without_plus"] = df_results["time"].where(
    ~df_results["time"].astype(str).str.contains(r"\+"), None
)

df_results_new = df_results.loc[
    :, ["raceId", "driverId", "time_with_plus", "time_without_plus"]
]

# Nettoyer les espaces autour des valeurs dans les colonnes "time_with_plus" et "time_without_plus"
df_results_new["time_with_plus"] = df_results_new["time_with_plus"].str.strip()
df_results_new["time_without_plus"] = df_results_new["time_without_plus"].str.strip()

# Replace string '\N' with actual NaN
df_results_new["time_without_plus"].replace("\\N", pd.NA, inplace=True)

# Filter rows where either column has a value (not null)
st_anne = df_results_new[
    df_results_new["time_with_plus"].notna()
    | df_results_new["time_without_plus"].notna()
]

# Filtrer les valeurs non nulles avant d'utiliser min()
filtered_time_with_plus = st_anne["time_with_plus"].dropna()

# Trouver la valeur minimale
min_time_with_plus = min(filtered_time_with_plus.astype(str))

# Afficher la ligne complète associée à cette valeur minimale
min_time_row = st_anne[st_anne["time_with_plus"] == min_time_with_plus]

# Ajouter la valeur de "time_without_plus" du premier ayant le même "raceId"
# dans une nouvelle colonne "best_time"

race_id = min_time_row["raceId"].values[0]
best_time = st_anne.loc[
    (st_anne["raceId"] == race_id) & st_anne["time_without_plus"].notna(),
    "time_without_plus"
].values[0]

min_time_row["best_time"] = best_time

# Charger à nouveau si nécessaire (ou s'assurer qu'on a toutes les colonnes dans df_results)
df_results_full = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
df_results_full.columns = df_results_full.columns.str.strip()

# Convertir raceId et positionOrder en entiers au cas où
df_results_full["raceId"] = df_results_full["raceId"].astype(int)
df_results_full["positionOrder"] = pd.to_numeric(df_results_full["positionOrder"], errors='coerce')

# Extraire le driverId du gagnant pour ce raceId
winner_driver_id = df_results_full[
    (df_results_full["raceId"] == race_id) & 
    (df_results_full["positionOrder"] == 1)
]["driverId"].values[0]

# Ajouter cette valeur à la ligne existante
min_time_row["driverId_Winner"] = winner_driver_id

# Extraire le raceId de min_time_row
race_id = min_time_row["raceId"].values[0]

# Filtrer pour obtenir les informations de la course
race_info = df_races[df_races["raceId"] == race_id][["name", "date", "circuitId"]]

# Récupérer circuitId et nom du GP (on a déjà race_info)
circuit_id = race_info["circuitId"].values[0]
nom_GP = race_info["name"].values[0]
date_GP = race_info["date"].values[0]

# Nom du circuit
nom_de_circuit = df_circuits[df_circuits["circuitId"] == circuit_id]["name"].values[0]

# Récupérer noms des pilotes
driver_id_winner = min_time_row["driverId_Winner"].values[0]
driver_id_second = min_time_row["driverId"].values[0]

# Nom du pilote gagnant
pilote_1er = df_drivers[df_drivers["driverId"] == driver_id_winner]
nom_du_pilote_1er = pilote_1er["forename"].values[0] + " " + pilote_1er["surname"].values[0]

# Nom du deuxième pilote
pilote_2eme = df_drivers[df_drivers["driverId"] == driver_id_second]
nom_du_pilote_2eme = pilote_2eme["forename"].values[0] + " " + pilote_2eme["surname"].values[0]

# Temps
temps_premier = min_time_row["best_time"].values[0]
ecart = min_time_row["time_with_plus"].values[0]

# Créer la table résultat
resultat = pd.DataFrame([{
    "nom_GP": nom_GP,
    "nom_de_circuit": nom_de_circuit,
    "date": date_GP,
    "nom_du_pilote_1er": nom_du_pilote_1er,
    "nom_du_pilote_2eme": nom_du_pilote_2eme,
    "temps_premier": temps_premier,
    "ecart": ecart
}])

# Afficher le résultat
phrase = (
    f"Lors du Grand Prix {nom_GP} disputé le {date_GP} sur le circuit de {nom_de_circuit}, "
    f"le pilote {nom_du_pilote_1er} a remporté la course avec un temps de {temps_premier}, "
    f"devançant {nom_du_pilote_2eme} de {ecart} secondes."
)

print(phrase)

