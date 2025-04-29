import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer




drivers = pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv")\
    , on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()
drivers["forename"] = drivers["forename"].str.replace('"', '').str.strip()
drivers["surname"] = drivers["surname"].str.replace('"', '').str.strip()
drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]

constructors = pd.read_csv(os.path.join("donnees_formule_un", "constructors.csv"))
constructors.columns = constructors.columns.str.strip()

results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
results.columns = results.columns.str.strip()

races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()

qualifying = pd.read_csv(os.path.join("donnees_formule_un", "qualifying.csv"))
qualifying.columns = qualifying.columns.str.strip()


table_1 = pd.merge(races, results, on= "raceId")
table_2 = pd.merge(table_1, constructors, on = "constructorId")
table_3 = pd.merge(table_2, qualifying, on = "driverId")
print(table_3.columns)
table = pd.merge(table_3, drivers, on = "driverId")


print(table.columns)
#sélectionner les variables dans la table
table = table[['raceId_x', 'year', 'name_x', 'nom_complet', 'name_y', 'positionOrder']]
# 1. Charger les données


# 2. Créer la cible
table['sur_podium'] = table['positionOrder'].apply(lambda x: 1 if x <= 3 else 0)

# 3. Feature Engineering
#df['rookie'] = df['experience_ans'].apply(lambda x: 1 if x < 2 else 0)

# 4. Gestion des valeurs manquantes
# Imputer la moyenne sur nb_victoires et nb_podiums
imputer = SimpleImputer(strategy='mean')

nb_victoires_2ans = table[table['positionOrder'] == 1].groupby('nom_complet').size()
df = pd.merge(table, nb_victoires_2ans, on='nom_complet', how='left')
print(df.columns)
df[['nb_victoires_2ans', 'nb_podiums_2ans']] = imputer.fit_transform(df[['nb_victoires_2ans', 'nb_podiums_2ans']])

# 5. Encodage des écuries
encoder = OneHotEncoder(drop='first')  # drop='first' pour éviter la colinéarité
ecuries_encoded = encoder.fit_transform(df[['ecurie_actuelle']]).toarray()
ecuries_encoded_df = pd.DataFrame(ecuries_encoded, columns=encoder.get_feature_names_out(['ecurie_actuelle']))

# 6. Assemblage des features
X = pd.concat([
    df[['position_championnat_actuel', 'nb_victoires_2ans', 'nb_podiums_2ans', 'grille_depart', 'rookie']],
    ecuries_encoded_df
], axis=1)

y = df['sur_podium']

# 7. Séparation en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 8. Modélisation
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 9. Prédiction et évaluation
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")
