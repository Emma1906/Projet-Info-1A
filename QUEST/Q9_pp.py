import os
import csv

# Chemin vers les fichiers
chemin_dossier = "donnees_formule_un"
fichier_races = os.path.join(chemin_dossier, "races.csv")
fichier_circuits = os.path.join(chemin_dossier, "circuits.csv")

# afficher le nom des attributs de circuits.csv
with open(fichier_circuits, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(header)


# Étape 1 : Charger circuits.csv dans un dictionnaire : circuitId → nom du circuit
circuits = {}
with open(fichier_circuits, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = [col.strip() for col in next(reader)]
    circuitId_index = header.index("circuitId")
    circuitRef_index = header.index("circuitRef")
    name_index = header.index("name")
    location_index = header.index("location")
    country_index = header.index("country")
    lat_index = header.index("lat")
    lng_index = header.index("lng")
    alt_index = header.index("alt")
    url_index = header.index("url")

    for row in reader:
        circuit_id = row[circuitId_index]
        circuit_ref = row[circuitRef_index]
        location = row[location_index]
        country = row[country_index]
        lat = row[lat_index]
        lng = row[lng_index]
        alt = row[alt_index]
        url = row[url_index]
        #circuits[circuit_id] = circuit_name

# étape 2 : Faire de même pour races

# Étape 3 : Compter combien de fois chaque circuitId apparaît dans races.csv
compteur_circuits = {}

with open(fichier_races, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = [col.strip() for col in next(reader)]
    circuit_index = header.index("circuitId")

    for row in reader:
        circuit_id = row[circuit_index]
        if circuit_id in compteur_circuits:
            compteur_circuits[circuit_id] += 1
        else:
            compteur_circuits[circuit_id] = 1

# Étape 3 : Trouver le circuit avec le plus grand nombre de courses
max_circuit_id = None
max_count = 0

for cid in compteur_circuits:
    if compteur_circuits[cid] > max_count:
        max_count = compteur_circuits[cid]
        max_circuit_id = cid

# Résultat final
nom_circuit = circuits.get(max_circuit_id, "Nom inconnu")
print(f"Le circuit le plus souvent utilisé est : {nom_circuit} ({max_count} fois)")
