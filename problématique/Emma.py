import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer

# 1. Charger les données


# 2. Créer la cible
df['sur_podium'] = df['positionOrder'].apply(lambda x: 1 if x <= 3 else 0)

# 3. Feature Engineering
#df['rookie'] = df['experience_ans'].apply(lambda x: 1 if x < 2 else 0)

# 4. Gestion des valeurs manquantes
# Imputer la moyenne sur nb_victoires et nb_podiums
imputer = SimpleImputer(strategy='mean')

first_places_counts = races_results_2023[races_results_2023['positionOrder'] == 1].groupby('driverId').size()
df = pd.merge(df, first_places_counts, on='driverId', how='left')
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
