# Projet-Info-1A
Notre projet utilise une base de donnée sur la Formule un afin de répondre à une série
de questions sur ce sport et de réaliser un modèle capable de prédire le podium
d'une course.

Commencez par installer l'ensemble des packages nécessaires pour que le code fonctionne.
Ils sont listés dans le fichier requirements.txt et peuvent être récupérés directement
en exécutant dans le terminal la commande pip install -r requirement.txt.

Les réponses à nos questions sont regroupées dans deux fichiers. Un fichier Python
dans lequel l'ensemble des questions sont traitées en Pandas : question_interface.py.
Et un Jupiter Notebook qui regroupe les trois questions traitées en Python pur :
Questions_Python_Pur.ipynb.

Le fichier interface_graphique.py permet d'ouvrir notre interface utilisateur et
d'accéder à l'ensemble des réponses aux questions.
La première page de notre interface regroupe la liste des questions. Il suffit de
cliquer sur l'une d'entre elles pour afficher la réponse sur une nouvelle page.
Ensuite, le bouton retour permet de revenir à la page principale. Certaines questions
demandent à l'utilisateur d'entrer l'année de son choix. Pour obtenir la réponse, il
suffit de cliquer sur le bouton valider une fois que l'année à été saisie.

Le fichier Problématique copy.ipynb permet de répondre à notre problématique. Pour
obtenir le résultat de notre régression logistique il suffit de run l'ensemble des zones
de code du fichier.

Enfin, le fichier resultats_sauvegarde.py permet de récupérer l'ensemble des sorties
de nos questions. Elles sont stockées dans le dossier resultats.
Les sorties du modèle de régression logistique sont sauvegardées dans le dossier
sorties_modele.
