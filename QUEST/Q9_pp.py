import os
import csv

# Chemin vers les fichiers
chemin_dossier = "donnees_formule_un"
fichier_races = os.path.join(chemin_dossier, "races.csv")
fichier_circuits = os.path.join(chemin_dossier, "circuits.csv")

# Étape 1 : Charger circuits.csv dans un dictionnaire : circuitId → nom du circuit
circuits = {}
with open(fichier_circuits, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = [col.strip() for col in next(reader)]
    circuitId_index = header.index("circuitId")
    name_index = header.index("name")

    for row in reader:
        circuit_id = row[circuitId_index].strip()
        circuit_name = row[name_index].strip()
        circuits[circuit_id] = circuit_name

# Étape 2 : Compter combien de fois chaque circuitId apparaît dans races.csv
compteur_circuits = {}

with open(fichier_races, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = [col.strip() for col in next(reader)]
    circuit_index = header.index("circuitId")

    for row in reader:
        circuit_id = row[circuit_index].strip()  # assure que c'est bien une chaîne nettoyée
        if circuit_id in compteur_circuits:
            compteur_circuits[circuit_id] += 1
        else:
            compteur_circuits[circuit_id] = 1

# Étape 3 : Trouver le circuit avec le plus grand nombre de courses
max_circuit_id = None
max_count = 0

for cid, count in compteur_circuits.items():
    if count > max_count:
        max_count = count
        max_circuit_id = cid



# Résultat final
nom_circuit = circuits.get(max_circuit_id, "Nom inconnu")
print(f"Le circuit le plus souvent utilisé est : {nom_circuit} ({max_count} fois)")
