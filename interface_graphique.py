import tkinter as tk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from questions_interface import (
    nom_pilotes_30_victoires,
    classement_pilote_2023,
    podium_ecuries,
    meilleur_temps_tour_2023,
    nb_best_lap_time_pilote_2023,
    nb_victoires_spa,
    temps_moyen_pit_stop_an,
    circuit_plus_concouru,
    victoires_par_nation,
    age_moyen_annee,
    course_plus_serrée,
    pilote_plus_accidents
)

# === Chargement des données ===
constructors = pd.read_csv(os.path.join("donnees_formule_un", "constructors.csv"))
constructors.columns = constructors.columns.str.strip()

constructors_standings =\
    pd.read_csv(os.path.join("donnees_formule_un", "constructor_standings.csv"))
constructors_standings.columns = constructors_standings.columns.str.strip()

laps = pd.read_csv(os.path.join("donnees_formule_un", "lap_times.csv"))
laps.columns = laps.columns.str.strip()

races = pd.read_csv(os.path.join("donnees_formule_un", "races.csv"))
races.columns = races.columns.str.strip()
races['name'] = races['name'].str.replace('"', '').str.strip()

drivers =\
    pd.read_csv(os.path.join("donnees_formule_un", "drivers.csv"), on_bad_lines='skip')
drivers.columns = drivers.columns.str.strip()
drivers["forename"] = drivers["forename"].str.replace('"', '').str.strip()
drivers["surname"] = drivers["surname"].str.replace('"', '').str.strip()
drivers["nom_complet"] = drivers["forename"] + " " + drivers["surname"]

results = pd.read_csv(os.path.join("donnees_formule_un", "results.csv"))
results.columns = results.columns.str.strip()

pit = pd.read_csv(os.path.join("donnees_formule_un", "pit_stops.csv"))
pit.columns = pit.columns.str.strip()

status = pd.read_csv(os.path.join("donnees_formule_un", "status.csv"))
status.columns = status.columns.str.strip()


# ======== Fonctions associées aux questions ===========

def repondre_q1():
    """Retourn la réponse à la question 1"""
    return nom_pilotes_30_victoires(results, drivers)


def repondre_q2():
    """Retourn la réponse à la question 2"""
    return classement_pilote_2023(races, results, drivers)


def repondre_q3():
    """Retourn la réponse à la question 3"""
    return podium_ecuries(constructors_standings, races, constructors)


def repondre_q4():
    """Retourn la réponse à la question 4"""
    return meilleur_temps_tour_2023(laps, races)


def repondre_q5():
    """Retourn la réponse à la question 5"""
    return nb_best_lap_time_pilote_2023(laps, races, drivers)


def repondre_q6():
    """Retourn la réponse à la question 6"""
    return nb_victoires_spa(results, races, drivers)


def repondre_q7():
    """Retourn la réponse à la question 7"""
    return pilote_plus_accidents(results, status)


def repondre_q8():
    """Retourn la réponse à la question 8"""
    return temps_moyen_pit_stop_an(races, pit)


def repondre_q9():
    """Retourn la réponse à la question 9"""
    return circuit_plus_concouru(races)


def repondre_q10():
    """Retourn la réponse à la question 10"""
    return course_plus_serrée(results, races, drivers)


def repondre_q11():
    """Retourn la réponse à la question 11"""
    return victoires_par_nation(drivers, results)


def repondre_q12():
    """Retourn la réponse à la question 12"""
    return age_moyen_annee(drivers, results, races)


qa_functions = {
    "Quels pilotes ont remporté au moins 30 courses ?": repondre_q1,
    "Quel est le classement des pilotes à l'issu de la saison 2023 ?": repondre_q2,
    "Quel est le podium des écuries à la fin de chaque saison ?": repondre_q3,
    "Quel est le meilleur temps d'un tour de circuit par course en 2023 ?": repondre_q4,
    "Quel est le nombre de best lap time par pilote en 2023 ?": repondre_q5,
    "Quels pilotes ont remporté le plus de fois le circuit de Spa-Francorchamps \
depuis 1950 ?": repondre_q6,
    "Quel est le pilote qui a eu le plus d'accidents par saison ?": repondre_q7,
    "Quel est le temps moyen des pit stop par an ?": repondre_q8,
    "Quels circuits ont été le plus de fois concourus ? ": repondre_q9,
    "Quelle a été la course la plus sérrée ?": repondre_q10,
    "Quel est le nombre de victiores par nation depuis 1950 ?": repondre_q11,
    "Quel est l'âge moyen des pilote en fonction des années ?": repondre_q12
}

# ================= Interface Graphique =================
root = tk.Tk()
root.title("Questions Formule 1")
root.geometry("800x600")
root.configure(bg="#1e1e2f")


# ============ Fonction pour changer de page ==============
def show_frame(frame):
    """
    Affiche le frame donné et le plaçant au premier plan dans l'interface Tkinter.

    Paramètres :
    ------------
    frame : tk.Frame
    """
    frame.tkraise()


# ============= Page Menu Principal ====================
page_menu = tk.Frame(root, bg="#1e1e2f")
page_menu.place(relwidth=1, relheight=1)
tk.Label(page_menu, text="Choisis une question :", bg="#1e1e2f", fg="white", font=("Arial", 16)).pack(pady=20)

pages = {}


# ====== Fonctions qui créent les pages à la demande (show_page) =======

def show_page_podium_ecuries():
    """ Affiche la page du podium des écuries."""
    if "podium" not in pages:
        pages["podium"] = create_page_podium_ecuries()
    show_frame(pages["podium"])


def show_page_pilote_accidents():
    """ Affiche la page du pilote avec le plus d'accidents."""
    if "accidents" not in pages:
        pages["accidents"] = create_page_pilote_accidents()
    show_frame(pages["accidents"])


def show_page_age_moyen():
    """Affiche la page de l'âge moyen des pilotes par année."""
    if "age" not in pages:
        pages["age"] = create_page_age_moyen()
    show_frame(pages["age"])


def show_page_pit_stop():
    """Affiche la page du temps moyen des pit stop par années."""
    if "pit_stop" not in pages:
        pages["pit_stop"] = create_page_temps_moyen_pit_stop_an()
    show_frame(pages["pit_stop"])


def show_page_classement():
    """Affiche la page du classement des pilotes à la fin de la saison 2023."""
    if "classement" not in pages:
        pages["classement"] = create_page_classement_pilote_2023()
    show_frame(pages["classement"])


def show_page_victoires_nation():
    """Affiche la page du nombre de victoires par nation depuis 1950."""
    if "nation" not in pages:
        pages["nation"] = create_page_victoires_par_nation()
    show_frame(pages["nation"])


def show_page_static(question):
    """Affiche la page correspondant à une des questions de la liste qa_functions"""
    if question not in pages:
        pages[question] = create_static_page(qa_functions[question]())
    show_frame(pages[question])


# ======== Pages ==========

def create_static_page(text):
    """
    Crée une page statique dans l'interface Tkinter pour afficher un texte donné.

    Parameters :
    ------------
    text : str
        Le contenu textuel à afficher dans la page.

    Returns :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant le texte fourni
        et un bouton "Retour" pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    reponse_text = tk.Text(frame, height=25, width=90, bg="white", fg="black", wrap=tk.WORD)
    reponse_text.pack(pady=20)
    reponse_text.insert(tk.END, text)

    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#444", fg="white").pack(pady=10)
    return frame


def create_page_classement_pilote_2023():
    """
    Crée une page Tkinter qui affiche un graphique du classement des pilotes
    pour la saison 2023.

    Returns :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant un graphique du classement des pilotes en 2023
        ainsi qu’un bouton pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    # Récupérer les données
    df = classement_pilote_2023(races, results, drivers)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['nom_complet'], df['points'], color="#007acc")
    ax.set_xlabel('Points')
    ax.set_title("Classement des pilotes - Saison 2023")
    ax.invert_yaxis()
    fig.tight_layout()

    # Intégration dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    # Bouton retour
    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#444", fg="white").pack(pady=10)

    return frame


def create_page_victoires_par_nation():
    """
    Crée une page Tkinter qui affiche un graphique du nombre de victoires par nation
    depuis 1950.

    Returns :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant un graphique du nombre de victoires par nation
    depuis 1950 ainsi qu’un bouton pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    # Récupérer les données sous forme de DataFrame
    df = victoires_par_nation(drivers, results)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['nationality'], df['Nombre de victoires par nation'], color="#0066cc")
    ax.set_xlabel('Nombre de victoires par nation')
    ax.set_title('Nombre de victoires par nation depuis 1950.')
    ax.invert_yaxis()
    fig.tight_layout()

    # Intégration du graphique dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    # Bouton retour
    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#ddd", fg="black").pack(pady=10)

    return frame


def create_page_podium_ecuries():
    """
    Crée une page Tkinter permettant d’afficher le podium des écuries pour une année
    donnée.

    Return :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant :
        - un champ de saisie pour entrer une année (entre 1958 et 2023),
        - un bouton pour valider l’entrée et afficher le podium correspondant,
        - un bouton retour pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text="Entrez une année entre 1958 et 2023 :", fg="white", bg="#1e1e2f")
    label.pack(pady=10)
    entry = tk.Entry(frame)
    entry.pack()
    text = tk.Text(frame, height=25, width=90, bg="white", fg="black", wrap=tk.WORD)
    text.pack(pady=10)

    def valider():
        """
        Vérifie et traite l’année saisie par l’utilisateur.
            - Récupère l’année entrée dans le champ de saisie.
            - Vérifie que cette année est un entier compris entre 1958 et 2023.
            - Si l’année est valide, appelle la fonction pour récupérer les résultats.
            - Sinon, affiche un message d’erreur dans la zone de texte.
        """
        try:
            annee = int(entry.get())
            if 1958 <= annee <= 2023:
                reponse = podium_ecuries(constructors_standings, races, constructors, annee)
            else:
                reponse = "Année invalide."
        except ValueError:
            reponse = "Entrée invalide."
        text.delete("1.0", tk.END)
        text.insert(tk.END, reponse)

    tk.Button(frame, text="Valider", command=valider, bg="#0066cc", fg="white").pack(pady=5)
    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#444", fg="white").pack(pady=10)
    return frame


def create_page_age_moyen():
    """
    Crée une page Tkinter permettant d’afficher l'âge moyen des pilotes pour une année
    donnée.

    Return :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant :
        - un champ de saisie pour entrer une année (entre 1950 et 2023),
        - un bouton pour valider l’entrée et afficher le podium correspondant,
        - un bouton retour pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text="Entrez une année entre 1950 et 2023 :", fg="white", bg="#1e1e2f")
    label.pack(pady=10)
    entry = tk.Entry(frame)
    entry.pack()
    text = tk.Text(frame, height=25, width=90, bg="white", fg="black", wrap=tk.WORD)
    text.pack(pady=10)

    def valider():
        """
        Vérifie et traite l’année saisie par l’utilisateur.
            - Récupère l’année entrée dans le champ de saisie.
            - Vérifie que cette année est un entier compris entre 1950 et 2023.
            - Si l’année est valide, appelle la fonction pour récupérer les résultats.
            - Sinon, affiche un message d’erreur dans la zone de texte.
        """
        try:
            annee = int(entry.get())
            if 1950 <= annee <= 2023:
                reponse = age_moyen_annee(drivers, results, races, annee)
            else:
                reponse = "Année invalide."
        except ValueError:
            reponse = "Entrée invalide."
        text.delete("1.0", tk.END)
        text.insert(tk.END, reponse)

    tk.Button(frame, text="Valider", command=valider, bg="#0066cc", fg="white").pack(pady=5)
    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#444", fg="white").pack(pady=10)
    return frame


def create_page_temps_moyen_pit_stop_an():
    """
    Crée une page Tkinter permettant d’afficher le temps moyen des pit stop
    pour une année donnée.

    Return :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant :
        - un champ de saisie pour entrer une année (entre 2011 et 2023),
        - un bouton pour valider l’entrée et afficher le podium correspondant,
        - un bouton retour pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text="Entrez une année entre 2011 et 2023 :", fg="white", bg="#1e1e2f")
    label.pack(pady=10)
    entry = tk.Entry(frame)
    entry.pack()
    text = tk.Text(frame, height=25, width=90, bg="white", fg="black", wrap=tk.WORD)
    text.pack(pady=10)

    def valider():
        """
        Vérifie et traite l’année saisie par l’utilisateur.
            - Récupère l’année entrée dans le champ de saisie.
            - Vérifie que cette année est un entier compris entre 2011 et 2023.
            - Si l’année est valide, appelle la fonction pour récupérer les résultats.
            - Sinon, affiche un message d’erreur dans la zone de texte.
        """
        try:
            annee = int(entry.get())
            if 2011 <= annee <= 2023:
                reponse = temps_moyen_pit_stop_an(races, pit, annee)
            else:
                reponse = "Année invalide."
        except ValueError:
            reponse = "Entrée invalide."
        text.delete("1.0", tk.END)
        text.insert(tk.END, reponse)

    tk.Button(frame, text="Valider", command=valider, bg="#0066cc", fg="white").pack(pady=5)
    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#444", fg="white").pack(pady=10)
    return frame


def create_page_pilote_accidents():
    """
    Crée une page Tkinter permettant d’afficher le pilote ayant eu le plus d'accident
    pour une année donnée.

    Return :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant :
        - un champ de saisie pour entrer une année (entre 1950 et 2023),
        - un bouton pour valider l’entrée et afficher le podium correspondant,
        - un bouton retour pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(
        frame, text="Entrez une année entre 1950 et 2023 :", fg="white", bg="#1e1e2f")
    label.pack(pady=10)
    entry = tk.Entry(frame)
    entry.pack()
    text = tk.Text(frame, height=25, width=90, bg="white", fg="black", wrap=tk.WORD)
    text.pack(pady=10)

    def valider():
        """
        Vérifie et traite l’année saisie par l’utilisateur.
            - Récupère l’année entrée dans le champ de saisie.
            - Vérifie que cette année est un entier compris entre 1950 et 2023.
            - Si l’année est valide, appelle la fonction pour récupérer les résultats.
            - Sinon, affiche un message d’erreur dans la zone de texte.
        """
        try:
            annee = int(entry.get())
            if 1950 <= annee <= 2023:
                reponse = pilote_plus_accidents(results, status, annee)
            else:
                reponse = "Année invalide."
        except ValueError:
            reponse = "Entrée invalide."
        text.delete("1.0", tk.END)
        text.insert(tk.END, reponse)

    tk.Button(
        frame, text="Valider", command=valider, bg="#0066cc", fg="white").pack(pady=5)
    tk.Button(
        frame, text="Retour", command=lambda: show_frame(
            page_menu), bg="#444", fg="white").pack(pady=10)
    return frame


def create_page_best_lap_time_2023():
    """
    Crée une page Tkinter qui affiche un graphique du nombre de best lap time par pilote
    lors de la saison 2023.

    Returns :
    --------
    frame : tk.Frame
        Un cadre Tkinter contenant un graphique du nombre de best lap time par pilote
    lors de la saison 2023 ainsi qu’un bouton pour revenir au menu principal.
    """
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.place(relwidth=1, relheight=1)

    # Recalculer les données
    fusion = pd.merge(laps, races, on='raceId')
    fusion.columns = fusion.columns.str.strip()
    fusionnow = pd.merge(fusion, drivers[['driverId', 'nom_complet']], on='driverId')

    meilleur_temps_tour_par_course = (
        fusionnow.loc[fusionnow.groupby(['raceId', 'year'])['milliseconds'].idxmin()]
    )
    meilleur_temps_tour_par_course_2023 = meilleur_temps_tour_par_course[
        meilleur_temps_tour_par_course['year'] == 2023
    ]
    meilleur_temps_par_pilote = (
        meilleur_temps_tour_par_course_2023.groupby('nom_complet').size()
        .reset_index(name='Nombre de meilleurs temps')
        .sort_values(by='Nombre de meilleurs temps', ascending=False)
    )

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(meilleur_temps_par_pilote['nom_complet'], meilleur_temps_par_pilote['Nombre de meilleurs temps'], color="#cc6600")
    ax.set_ylabel('Nombre de meilleurs temps')
    ax.set_title('Best Lap Time par Pilote - Saison 2023')
    ax.set_xticks(range(len(meilleur_temps_par_pilote)))
    ax.set_xticklabels(meilleur_temps_par_pilote['nom_complet'], rotation=45, ha='right')
    fig.tight_layout()

    # Intégration dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    # Bouton retour
    tk.Button(frame, text="Retour", command=lambda: show_frame(page_menu), bg="#444", fg="white").pack(pady=10)

    return frame


# ======= Boutons dynamiques (créés à la demande) ========
tk.Button(page_menu, text="Quel est le podium des écuries à la fin de chaque saison ?",
          command=show_page_podium_ecuries, bg="#0066cc", fg="white", width=90,
          height=2, wraplength=700).pack(pady=5)

tk.Button(page_menu,
          text="Quel est le classement des pilotes à l'issu de la saison 2023 ?",
          command=show_page_classement, bg="#0066cc", fg="white", width=90, height=2,
          wraplength=700).pack(pady=5)

tk.Button(page_menu, text="Quel est le temps moyen des pit stop par an ?",
          command=show_page_pit_stop, bg="#0066cc", fg="white", width=90, height=2,
          wraplength=700).pack(pady=5)

tk.Button(page_menu,
          text="Quel est le pilote qui a eu le plus d'accident en fonction\
              des saisons ?",
          command=show_page_pilote_accidents, bg="#0066cc", fg="white", width=90,
          height=2, wraplength=700).pack(pady=5)

tk.Button(page_menu, text="Quel est le nombre de victoires par nation depuis 1950 ?",
          command=show_page_victoires_nation, bg="#0066cc", fg="white", width=90,
          height=2, wraplength=700).pack(pady=5)

tk.Button(page_menu, text="Quel est l'âge moyen des pilote en fonction des années ?",
          command=show_page_age_moyen, bg="#0066cc", fg="white", width=90, height=2,
          wraplength=700).pack(pady=5)

tk.Button(page_menu, text="Quel est le nombre de best lap time par pilote en 2023 ?",
          command=create_page_best_lap_time_2023, bg="#0066cc", fg="white", width=90,
          height=2, wraplength=700).pack(pady=5)


# ======== Boutons statiques =======
questions_dynamiques = {
    "Quel est le podium des écuries à la fin de chaque saison ?",
    "Quel est le pilote qui a eu le plus d'accidents par saison ?",
    "Quel est l'âge moyen des pilote en fonction des années ?",
    "Quel est le temps moyen des pit stop par an ?",
    "Quel est le classement des pilotes à l'issu de la saison 2023 ?",
    "Quel est le nombre de best lap time par pilote en 2023 ?",
    "Quel est le nombre de victiores par nation depuis 1950 ?"
}

for question in qa_functions:
    if question not in questions_dynamiques:
        tk.Button(page_menu, text=question,
                  command=lambda q=question: show_page_static(q),
                  bg="#0066cc", fg="white", width=90, height=2,
                  wraplength=700).pack(pady=5)


# ======== Démarrage de l'application ========
show_frame(page_menu)
root.mainloop()
