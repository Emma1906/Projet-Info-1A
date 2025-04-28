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

print(df_results_new.head(10))

# Replace string '\N' with actual NaN
df_results_new["time_without_plus"].replace("\\N", pd.NA, inplace=True)

# Filter rows where either column has a value (not null)
st_anne = df_results_new[
    df_results_new["time_with_plus"].notna()
    | df_results_new["time_without_plus"].notna()
]

# tableau ne prenant que les lignes ou il y a une valeur dans une des deux colonnes
print(st_anne.head(10))

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
print(min_time_row)

