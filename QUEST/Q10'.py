import pandas as pd
import os

# Charger les données
df_results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))


# Nettoyage des colonnes
df_results.columns = df_results.columns.str.strip()

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

print(df_results_new.columns)

# Nettoyer les espaces autour des valeurs dans les colonnes "time_with_plus" et "time_without_plus"
df_results_new["time_with_plus"] = df_results_new["time_with_plus"].str.strip()
df_results_new["time_without_plus"] = df_results_new["time_without_plus"].str.strip()

