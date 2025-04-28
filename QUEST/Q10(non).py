import pandas as pd
import os

# Charger les données
df_results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))


# Afficher les colonnes pour vérifier leur nom
print(df_results.columns)

# Nettoyage des colonnes
df_results.columns = df_results.columns.str.strip()
df_results["fastestLapTime"] = (
    df_results["fastestLapTime"].astype(str).str.strip().str.replace('"', "")
)

# Suppression des valeurs non renseignées ou incorrectes
df_results = df_results[
    df_results["fastestLapTime"].str.match(r"^\d{1,2}:\d+\.\d+$", na=False)
]


# Fonction pour convertir "MM:SS.sss" en secondes
def time_to_seconds(time_str):
    minutes, seconds = map(float, time_str.split(":"))
    return minutes * 60 + seconds


# Appliquer la conversion
df_results["fastestLapTime_sec"] = df_results["fastestLapTime"].apply(time_to_seconds)

# Grouper par raceId et calculer le min et le max pour chaque course
grouped = (
    df_results.groupby("raceId")
    .agg(
        min_time_sec=("fastestLapTime_sec", "min"),
        max_time_sec=("fastestLapTime_sec", "max"),
    )
    .reset_index()
)

# Ajouter les temps min et max au format original
grouped["min_time"] = grouped["min_time_sec"].apply(
    lambda x: df_results.loc[
        df_results["fastestLapTime_sec"] == x, "fastestLapTime"
    ].values[0]
)
grouped["max_time"] = grouped["max_time_sec"].apply(
    lambda x: df_results.loc[
        df_results["fastestLapTime_sec"] == x, "fastestLapTime"
    ].values[0]
)

# Ajouter une colonne pour la différence entre max_time_sec et min_time_sec
grouped["différence en seconde"] = grouped["max_time_sec"] - grouped["min_time_sec"]


# Afficher les résultats
print(grouped)
print("la course avec le plus grand écart de temps entre le premier et le dernier :",
      max(grouped["différence en seconde"]))
print("la course avec le plus petit écart de temps entre le premier et le dernier :",
      min(grouped["différence en seconde"]))
print("la course avec le plus petit temps de tour rapide :", min(grouped["min_time"]))
