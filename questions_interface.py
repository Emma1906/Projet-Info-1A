# Questions Formule Un

# Librairies
import pandas as pd
import os
from datetime import datetime


# Chargement des tables utiles
constructors = pd.read_csv(os.path.join("donnees_formule_un", "constructors.csv"))
constructors.columns = constructors.columns.str.strip()

constructors_standings = pd.read_csv(
    os.path.join("donnees_formule_un", "constructor_standings.csv"))
constructors_standings.columns = constructors_standings.columns.str.strip()

laps = pd.read_csv(os.path.join("donnees_formule_un", "lap_times.csv"))
laps.columns = laps.columns.str.strip()

races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()
races['name'] = races['name'].str.replace('"', '').str.strip()

drivers = pd.read_csv(
    os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()
drivers["forename"] = drivers["forename"].str.replace('"', '').str.strip()
drivers["surname"] = drivers["surname"].str.replace('"', '').str.strip()
drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]

results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
results.columns = results.columns.str.strip()

pit = pd.read_csv(os.path.join("donnees_formule_un", "pit_stops.csv"))
pit.columns = pit.columns.str.strip()


# Quentions utilisées pour l'interface graphique

# Question 1 : Quels pilotes ont remporté au moins 30 courses ?

def nom_pilotes_30_victoires(results, drivers):
    """
    Retourne la liste des pilotes ayant remporté au moins 30 courses et leur nombre de
    victoires. Ils sont classés par ordre décroissant du nombre de victoires.

    Parameters
    ----------
    results : DataFrame
        Données sur les résultats des courses.

    drivers : DataFrame
        Informations sur les pilotes.

    Returns
    -------
    str
        Liste des pilotes ayant au moins 30 victoires, avec leur nombre de victoires.
    """

    # Comptage des victoires (position 1)
    victoires = results[results['positionOrder'] == 1].groupby('driverId').size()
    pilotes_filtrés = victoires[victoires >= 30]

    if pilotes_filtrés.empty:
        return "Aucun pilote n’a remporté au moins 30 victoires."

    # Fusion avec les noms
    infos_pilotes = drivers[drivers['driverId'].isin(pilotes_filtrés.index)].copy()
    infos_pilotes['victoires'] = infos_pilotes['driverId'].map(pilotes_filtrés)
    infos_pilotes = infos_pilotes.sort_values(by='victoires', ascending=False)

    # Affichage
    lignes = infos_pilotes.apply(
        lambda row: (
            f"- {row['forename']} {row['surname']} "
            f"({row['victoires']} victoires)"
        ),
        axis=1
    ).tolist()

    return "Les pilotes ayant au moins 30 victoires sont :\n" + "\n".join(lignes)


# Question 2 : Quel est le classement des pilotes à l'issu de la saison 2023 ?

def classement_pilote_2023(races, results, drivers):
    """
    Retourne un tableau du classement des pilotes à la fin de l'année 2023.

    Ce classement prend en compte le nombre de points opur chaque pilote à la fin de la
    saison 2023. En cas d'égalité, les pilotes sont départagés par leur nombre de
    première place, puis de seconde place, etc.

    Parameters:
    ------------
    races : Dataframe
        Informations sur les courses.

    results : Dataframe
        Informations sur le résultat des courses.

    drivers : Dataframe
        Informations sur les pilotes.

    Returns:
    ------------
    Dataframe
        Tableau de classement des pilotes à la fin de la saison 2023

    """
    # Fusion des données
    races_results = pd.merge(races, results, on='raceId')
    races_results = pd.merge(
        races_results, drivers[['driverId', 'nom_complet']], on='driverId')
    # Filtrer sur l'année 2023
    races_results_2023 = races_results[races_results['year'] == 2023]
    # Calcul des points totaux
    points_totals = races_results_2023.groupby('driverId')['points'].sum().reset_index()
    # Comptage des positions (1ère, 2ème, etc.)
    positions_counts = races_results_2023.groupby(
        ['driverId', 'positionOrder']).size().unstack(fill_value=0)

    # Fusion avec les noms
    classement = pd.merge(
        points_totals, drivers[['driverId', 'nom_complet']], on='driverId')
    classement = pd.merge(classement, positions_counts, on='driverId', how='left')

    # Remplacer les colonnes vides par 0 si certaines positions ne sont pas occupées
    for pos in range(1, 21):
        if pos not in classement.columns:
            classement[pos] = 0

    # Tri : d'abord par points, puis 1res places, 2des places, etc.
    tri = ['points'] + list(range(1, 21))
    classement = classement.sort_values(
        by=tri, ascending=[False] + [False]*20).reset_index(drop=True)

    # Affichage final
    colonnes_a_afficher = ['nom_complet', 'points']
    return classement[colonnes_a_afficher]


# Question 3 : Quel est le podium des écuries à la fin de chaque saison ?

def podium_ecuries(constructors_standings, races, constructors, annee):
    """
    Retourne le podium des écuries à la fin de chaque saison.

    Parameters:
    -------------
    constructors_standings : Dataframe
        Informations sur le classement final du championnat des constructeurs.

    races : Dataframe
        Informations sur les courses

    constructors : Dataframe
        Information sur les écuries (constructeurs automobiles).

    annee : int
        Année choisie par l'utilisateur.

    Returns:
    -----------
     str
        Une chaîne de caractères formatée présentant le podium des écuries pour
        l'année spécifiée.


    Exemples :
    ------------
    "Podium des écuries en 2004 :
        1. Ferrari (262.0 points)
        2. BAR (119.0 points)
        3. Renault (105.0 points)"

    """
    # Fusion des tables
    fusion = pd.merge(constructors_standings, races, on='raceId')
    fusion = fusion[['raceId', 'constructorId', 'points', 'position', 'year']]
    fusion_now = pd.merge(fusion, constructors, on='constructorId')

    # Trouver le dernier raceId (la dernière course) pour chaque année
    dernieres_courses = fusion_now.groupby('year')['raceId'].max().reset_index()

    # Filtrer pour ne garder que les lignes correspondant à ces dernières courses
    fusion_finale = pd.merge(fusion_now, dernieres_courses, on=['year', 'raceId'])

    # Garder uniquement les positions 1, 2, 3
    fusion_finale = fusion_finale[fusion_finale['position'].isin([1, 2, 3])]
    fusion_finale = fusion_finale[['year', 'name', 'points', 'position']]
    fusion_finale['name'] = fusion_finale['name'].str.replace('"', '').str.strip()
    fusion_finale = fusion_finale.sort_values(by='position')

    podium = fusion_finale[fusion_finale['year'] == annee]

    lignes = []
    for pos in [1, 2, 3]:
        equipe = podium[podium['position'] == pos].iloc[0]
        lignes.append(f"{pos}. {equipe['name']} ({equipe['points']} points)")

    return f"Podium des écuries en {annee} :\n" + "\n".join(lignes)


# Question 4 : Quel est le meilleur temps d'un tour de circuit par course en 2023 ?

def meilleur_temps_tour_2023(laps, races):
    """
    Retourne le meilleur temps d'un tour de circuit pour chaque circuit de l'année 2023.

    Parameters :
    -------------
    laps : Dataframe
        Information sur les lap time (temps d'un tour de circuit)

    races : Dataframe
        Informations sur les courses

    Returns:
    ----------
    str
        Une chaîne de caractères listant le meilleur temps au tour (en millisecondes)
    pour chaque circuit de l'année 2023.


    """
    # Fusion des tables
    fusion = pd.merge(laps, races, on='raceId')
    fusion.columns = fusion.columns.str.strip()
    fusion['name'] = fusion["name"].str.replace('"', '').str.strip()

    # Extraire les années des courses
    # annees_courses = fusion[['year', 'raceId', 'name']].drop_duplicates()

    # Extraire le temps le plus rapide
    meilleur_temps_tour_par_course = fusion.groupby(
        ['raceId', 'year'])['milliseconds'].min().reset_index()

    # Fusionner pour inclure le nom de la course
    meilleur_temps_tour_par_course = pd.merge(
        meilleur_temps_tour_par_course,
        fusion[['raceId', 'name']],
        on='raceId',
        how='left'
    ).drop_duplicates()

    # Filtrer sur l'année 2023
    meilleur_temps_2023 = meilleur_temps_tour_par_course[
        meilleur_temps_tour_par_course['year'] == 2023
    ]

    # Formatage pour l'affichage dans l'interface
    lignes = []
    for _, row in meilleur_temps_2023.iterrows():
        lignes.append(f"{row['name']} : {row['milliseconds']} ms")

    if not lignes:
        return "Aucun temps trouvé pour l'année 2023."

    return (
        "Voici les meilleurs temps d'un tour de circuit par course en 2023:\n"
        + "\n".join(lignes)
    )


# Question 5 : Quel est le nombre de best lap time par pilote en 2023 ?

def nb_best_lap_time_pilote_2023(laps, races, drivers):
    """
    Retourne le nombre de best lap time (meilleur temps au tour) par pilote en 2023.

    Parameters :
    -------------
    laps : Dataframe
        Information sur les lap time (temps d'un tour de circuit)

    races : Dataframe
        Informations sur les courses

    drivers : Dataframe
        Informations sur les pilotes.


    Returns:
    ---------
    str
        Chaîne de carcatères listant le nombre de meilleurs temps au tout par pilote.
    """
    # Fusion des tables
    fusion = pd.merge(laps, races, on='raceId')
    fusion.columns = fusion.columns.str.strip()
    fusionnow = pd.merge(fusion, drivers[['driverId', 'nom_complet']], on='driverId')

    # Extraire les meilleurs temps par course
    meilleur_temps_tour_par_course = (
        fusionnow.loc[fusionnow.groupby(['raceId', 'year'])['milliseconds'].idxmin()]
    )

    # Filtrer sur l'année 2023
    meilleur_temps_tour_par_course_2023 = meilleur_temps_tour_par_course[
        meilleur_temps_tour_par_course['year'] == 2023
    ]

    # regroupe par pilote
    meilleur_temps_par_pilote = (
        meilleur_temps_tour_par_course_2023.groupby('nom_complet').size()
        .reset_index(name='Nombre de meilleurs temps')
        .sort_values(by='Nombre de meilleurs temps', ascending=False)
    )

    # Formatage pour l'affichage dans l'interface
    lignes = []
    for _, row in meilleur_temps_par_pilote.iterrows():
        lignes.append(f"{row['nom_complet']} : {row['Nombre de meilleurs temps']}")

    if not lignes:
        return "Aucun temps trouvé pour l'année 2023."

    return "\n".join(lignes)


# Question 6 : Quels pilotes ont remporté le plus de fois le circuit
# de Spa-Francorchamps, depuis 1950 ?

def nb_victoires_spa(results, races, drivers):
    """
    Retourne les deux pilotes qui ont gagné le plus de fois le circuit de
    Spa-Francorchamps. La fonction retourne également leur nombre de victoires sur ce
    circuit.


    Parameters:
    ------------
    results : Dataframe
        Informations sur le résultat des courses.

    races : Dataframe
        Informations sur les courses.

    drivers : Dataframe
        Informations sur les pilotes.


    Returns:
    -----------
    str
        Liste des piloes ayant le plus de victoires sur la course Spa-Francorchamps
        ainsi que leur nombre de victoires.
    """
    # Fusion des tables
    fusion = pd.merge(results, races, on='raceId')
    spa_gagnant = pd.merge(drivers, fusion, on='driverId')

    # Filtrer la table
    spa_gagnant = spa_gagnant[
        spa_gagnant['circuitId'] == 13]
    spa_gagnant = spa_gagnant[spa_gagnant['positionOrder'] == 1]

    spa_gagnant = (
        spa_gagnant.groupby('nom_complet')
        .size()
        .reset_index(name="Nombre de victoires")
        .sort_values(by="Nombre de victoires", ascending=False)
    )

    top2 = spa_gagnant.head(2)

    # Formatage pour l'affichage dans l'interface
    lignes = []
    for _, row in top2.iterrows():
        lignes.append(f"{row['nom_complet']} : {row['Nombre de victoires']}")

    if not lignes:
        return "Il ne fait pas partie des pilotes ayant le plus de victoires sur ce circuit."

    # Ajout de la phrase d'introduction
    phrase = "Les pilotes ayant remporté le plus de fois le circuit de Spa-Francorchamps sont :"
    return phrase + "\n" + "\n".join(lignes)


# Question 7 : Quel est le pilote qui a eu le plus d'accidents par saisons ?

def pilote_plus_accidents(results, status, annee):
    """
    Retourne le nom du pilote ayant eu le plus d'accident en fonction de l'année
    sélectionnée par l'utilisateur.
    Retourne également le nombre d'accidents correspondant.

    Parameters:
    ------------
    results : Dataframe
        Informations sur le résultat des courses.

    status : Dataframe
        Informations sur les différents status, les différentes manières de finir
        la course. Contient notamment des informations sur les accidents.

    annee : int
        Année choisie par l'utilisateur.


    Returns:
    ----------
    str
        Une chaîne de caractères indiquant le nom du pilote ayant eu le plus
        d'accidents sur l'année sélectionnée, ainsi que le nombre d'accidents


    Exemples :
    ----------
    "Le pilote ayant eu le plus d'accidents en 1962 est Jack Brabham
    avec 2 accident(s)."

    """
    fusion = pd.merge(results, status, on='statusId')
    fusion.columns = fusion.columns.str.strip()
    fusion_now = pd.merge(fusion, races, on='raceId')
    fusion_now.columns = fusion_now.columns.str.strip()
    fusion_v2 =\
        pd.merge(fusion_now, drivers[['driverId', 'nom_complet']], on='driverId')
    fusion_v2.columns = fusion_v2.columns.str.strip()
    # Compter le nombre d'accidents pour chaque pilote, status = Accident
    fusion_v2['status'] = fusion_v2['status'].str.strip().str.replace('"', '')
    fusion_v2 = fusion_v2[fusion_v2['status'] == "Accident"]
    # Compter le nombre d'accidents par pilote et par année
    accidents_par_pilote =\
        fusion_v2.groupby(['year', 'driverId']).size().reset_index(name='nb_accidents')
    # Garder le pilote avec le plus d'accidents par année
    accidents_max = accidents_par_pilote.loc[
            accidents_par_pilote.groupby('year')['nb_accidents'].idxmax()]
    # Ajouter le nom du pilote
    accidents_max = accidents_max.merge(
        drivers[['driverId', 'nom_complet']], on='driverId', how='left')
    # Garder les colonnes finales
    accidents_max = accidents_max[accidents_max['year'] == annee]

    # Afficher
    if accidents_max.empty:
        return f"Aucun accident enregistré en {annee}."
    pilote = accidents_max.iloc[0]
    return (
        f"Le pilote ayant eu le plus d'accidents en {annee} est "
        f"{pilote['nom_complet']} avec {pilote['nb_accidents']} accident(s)."
        )


# Question 8 : Quel est le temps moyen des pit stop par an ?

def filtrer_pit_stops(df):
    """
    Permet de filtrer les pit stops en retirant les valeurs extrêmes ou aberrantes,
    en se basant sur les percentiles 1% et 99% des durées,
    avec une limite maximale fixée à 30 secondes.

    Parameters :
    ------------
    df : Dataframe
        Dataframe contenant les données de pit stops, avec au moins une colonne
        'milliseconds' représentant la durée du pit stop en millisecondes.

    Returns:
    -------------
    Dataframe
        Un DataFrame filtré, ne contenant que les pit stops dont la durée est comprise
        entre le 1er percentile et le minimum entre le 99e percentile
        et 30 000 millisecondes.

    """
    q1 = df['milliseconds'].quantile(0.01)
    q99 = df['milliseconds'].quantile(0.99)
    limite_superieure = min(q99, 30000)
    return df[(df['milliseconds'] >= q1) & (df['milliseconds'] <= limite_superieure)]


def temps_moyen_pit_stop_an(races, pit, annee):
    """
    Retourne le temps moyen d'un pit stop (en millisecondes) en fonction de l'année
    sélectionnée par l'utilisateur.

    L'année doit être comprise entre 2011 et 2023, nous ne disposons pas des données
    pour les années avant 2011.

    Parameters:
    ------------
    races : Dataframe
        Informations sur les courses.

    pit : Dataframe
        Informations sur les pits stop.

    annee : int
        Année choisie par l'utilisateur.


    Returns:
    ----------
    str
        Une chaîne de caractères indiquant le temps moyen d'un pit stop
        pour l'année sélectionnée,


    Examples :
    ----------
    "Le temps moyen des pit stop en 2015 est de 24035 ms."

    """
    # Fusion des tables
    fusion = pd.merge(races, pit, on='raceId')
    fusion.columns = fusion.columns.str.strip()

    pit_annee = fusion[fusion['year'] == annee]
    pit_annee_filtre = filtrer_pit_stops(pit_annee)

    if not pit_annee_filtre.empty:
        moyenne = pit_annee_filtre['milliseconds'].mean()
        return f"Le temps moyen des pit stop en {annee} est de {moyenne:.0f} ms."
    else:
        return f"Aucune donnée de pit stop trouvée pour l'année {annee}."


# Question 9 : Quels circuits ont été le plus de fois concourrus ?

def circuit_plus_concouru(races):
    """
    Retourne le nom des circuits ayant été le plus de fois concourrus.
    retourne égalment le nombre de fois où les circuits ont été concourrus.

    Parameters:
    ------------
    races : Dataframe
        Informations sur les courses.

    Returns:
    -------------
    str
        Chaîne de caractères listant les 5 circuits les plus souvent utilisés,
        avec le nombre de fois où ils ont été concourus.
    """
    # On regroupe par circuit et on compte le nombre de fois où il a été concurru
    nb_fois_circuit = (
        races.groupby('name')
        .size()
        .reset_index(name="Nombre de fois où le circuit a été concuru")
        .sort_values(by="Nombre de fois où le circuit a été concuru", ascending=False)
        .head(5)  # ne garder que les 5 premiers
    )

    # Formatage pour l'affichage dans l'interface
    lignes = []
    for _, row in nb_fois_circuit.iterrows():
        lignes.append(
            f"{row['name']} : {row['Nombre de fois où le circuit a été concuru']}")

    if not lignes:
        return "Aucun circuit trouvé."

    return "Les circuits les plus de fois concourus sont :\n" + "\n".join(lignes)


# Question 10 : Quelle a été la course le plus serrée ?

def course_plus_serrée(results, races, drivers):
    """
    Retourne le nom de la course qui a été la plus serrée, c'est-a-dire où l'écart
    de temps entre le remier et le second pilote a été le plus faible.

    Cette fonction retourne le nom de la course, sa date, le nom des deux pilotes et
    l'écart de temps entre les deux pilotes.

    Parameters:
    ------------
    results : Dataframe
        Informations sur le résultat des courses.

    races : Dataframe
        Informations sur les courses.

    drivers : Dataframe
        Informations sur les pilotes.


    Returns:
    -----------
    str
        Chaîne de caractère qui retourne le nom de la course la plus sérrée avec
        sa date, le nom des pilotes et l'écart de temps.
    """

    # Séparer les temps avec et sans "+"
    results["time_with_plus"] =\
        results["time"].where(results["time"].astype(str).str.contains(r"\+"))
    results["time_without_plus"] =\
        results["time"].where(~results["time"].astype(str).str.contains(r"\+"))

    # Nettoyage
    results["time_with_plus"] = results["time_with_plus"].astype(str).str.strip()
    results["time_without_plus"] = results["time_without_plus"].astype(str).str.strip()
    results["time_without_plus"] = results["time_without_plus"].replace("\\N", pd.NA)

    # Lignes valides
    valid = results[results["time_with_plus"].notna() |
                    results["time_without_plus"].notna()].copy()
    if valid.empty:
        return "Aucune course avec des écarts de temps valides n'a été trouvée."

    # Écart minimal
    min_time_with_plus = valid["time_with_plus"].dropna().min()
    min_time_row = valid[valid["time_with_plus"] == min_time_with_plus].copy()
    if min_time_row.empty:
        return "Impossible d'identifier la course la plus serrée."

    race_id = min_time_row["raceId"].values[0]

    # Temps du vainqueur
    best_time = valid.loc[
        (valid["raceId"] == race_id) & valid["time_without_plus"].notna(),
        "time_without_plus"
    ].values[0]
    min_time_row["best_time"] = best_time

    # Charger tous les résultats (vainqueur)
    df_results_full = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
    df_results_full.columns = df_results_full.columns.str.strip()
    df_results_full["raceId"] = df_results_full["raceId"].astype(int)
    df_results_full["positionOrder"] = pd.to_numeric(df_results_full["positionOrder"], errors='coerce')

    winner_row = df_results_full[
        (df_results_full["raceId"] == race_id) & (df_results_full["positionOrder"] == 1)
    ]
    if winner_row.empty:
        return "Vainqueur introuvable pour cette course."

    winner_driver_id = winner_row["driverId"].values[0]
    min_time_row["driverId_Winner"] = winner_driver_id

    # Infos sur la course
    race_info = races[races["raceId"] == race_id][["name", "date"]].iloc[0]
    nom_GP = race_info["name"]
    date_GP = race_info["date"]

    # Infos pilotes
    driver_id_winner = min_time_row["driverId_Winner"].values[0]
    driver_id_second = min_time_row["driverId"].values[0]

    pilote_1er = drivers[drivers["driverId"] == driver_id_winner].iloc[0]
    pilote_2eme = drivers[drivers["driverId"] == driver_id_second].iloc[0]

    nom_du_pilote_1er = f"{pilote_1er['forename'].strip()} {pilote_1er['surname'].strip()}"
    nom_du_pilote_2eme = f"{pilote_2eme['forename'].strip()} {pilote_2eme['surname'].strip()}"

    # Temps
    temps_premier = min_time_row["best_time"].values[0]
    ecart = min_time_row["time_with_plus"].values[0]

    # Phrase finale
    phrase = (
        f"La course la plus serrée a eu lieu lors du Grand Prix {nom_GP.strip()} disputé le {date_GP.strip()}. "
        f"Le pilote {nom_du_pilote_1er} a remporté la course avec un temps de {temps_premier.strip()}, "
        f"devançant {nom_du_pilote_2eme} de {ecart.strip()} secondes."
    )

    return phrase


# Question 11 : Quel est le nombre de victoires par nation depuis 1950 ?

def victoires_par_nation(drivers, results):
    """
    Retourne le nombre de victoires par nation depuis 1950.

    Parameters:
    ------------
    drivers : Dataframe
        Informations sur les pilotes.

    results : Dataframe
        Informations sur le résultat des courses.


    Returns:
    -----------
    DataFrame
        Tableau contenant deux colonnes :
        - 'nationality' : la nationalité des pilotes
        - 'Nombre de victoires par nation' : le nombre total de victoires associées
        à chaque nationalité, trié par ordre décroissant.
    """
    fusion = pd.merge(drivers, results, on="driverId")
    fusion['nationality'] = fusion["nationality"].str.replace('"', '').str.strip()
    victoire = fusion[fusion['positionOrder'] == 1]

    victoire_nation = (
        victoire.groupby('nationality')
        .size()
        .reset_index(name="Nombre de victoires par nation")
        .sort_values(by="Nombre de victoires par nation", ascending=False)
    )

    return victoire_nation


# Question 12 : Quel est l'âge moyen des pilotes en fonction des années ?

def age_moyen_annee(drivers, results, races, annee):
    """
    Retourne l'âge moyen des pilotes en fonction de l'âge sélectionnée
    par l'utilisateur.

    Parameters:
    ------------
    drivers : Dataframe
        Informations sur les pilotes.

    results : Dataframe
        Informations sur le résultat des courses.

    races : Dataframe
        Informations sur les courses.

    annee : int
        Année choisie par l'utilisateur.


    Returns:
    ----------
    str
        Une chaîne de caractères indiquant :
        - l'âge moyen des pilotes pour l'année sélectionnée, s'il est disponible ;
        - un message d'information si aucune donnée n'est disponible ou si les âges
        ne sont pas exploitables.

    Examples :
    ----------
    "L'âge moyen des pilotes en 1978 est de 29.70 ans"

    """
    # Fusion des tables
    fusion = pd.merge(drivers, results, on='driverId')
    fusion = pd.merge(fusion, races, on='raceId')
    fusion.columns = fusion.columns.str.strip()
    # Nettoyage de la colonne 'dob'
    fusion['dob'] = fusion['dob'].str.strip().str.replace('"', '', regex=False)
    fusion['dob'] = pd.to_datetime(fusion['dob'], format='%Y-%m-%d', errors='coerce')

    # Filtrage de l'année demandée
    fusion_annee =\
        fusion[fusion['year'] == annee].drop_duplicates(subset=['driverId']).copy()
    if fusion_annee.empty:
        return f"Aucune donnée disponible pour l'année {annee}."

    date_reference = datetime(annee, 1, 1)
    fusion_annee['age'] = fusion_annee['dob'].apply(
        lambda x: date_reference.year - x.year - (
            (date_reference.month, date_reference.day) < (x.month, x.day))
        if pd.notnull(x) else None
    )
    age_moyen = fusion_annee['age'].mean()

    if pd.isnull(age_moyen):
        return f"Aucun âge valide trouvé pour l'année {annee}."

    return f"L'âge moyen des pilotes en {annee} est de {age_moyen:.2f} ans."
