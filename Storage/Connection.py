import pymongo
import json
import matplotlib.pyplot as plt

# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"
collection_name = "2022"
collection_name1 = "2014"

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]
collection = db[collection_name]

# Lista di tuple per tenere traccia dei piloti e del GP corrispondente senza dati di Qualifying
pilots_without_qualifying = []
pilots_disqualified = []

# Lista di tuple per tenere traccia dei piloti e del GP corrispondente senza dati di Laps
pilots_without_laps = []
pilots_disqualified_laps = []

# Lista di tuple per tenere traccia dei piloti e del GP corrispondente senza dati di Qualifying e Laps
pilots_without_qualifying_laps = []

# Cicla sui documenti nella collezione
for document in collection.find():
    for driver, races in document.items():
        if driver != "_id":
            for race, data in races.items():
                if isinstance(data, dict):
                    if "Qualifying" in data:
                        qualifying_times = data["Qualifying"]
                        if all(not qualifying_times[time] for time in ["Q1 Time", "Q2 Time", "Q3 Time"]):
                            # Aggiungi una tupla (pilota, GP) alla lista pilots_without_qualifying
                            pilots_without_qualifying.append((driver, race))
                    else:
                        # Aggiungi una tupla (pilota, GP) alla lista pilots_disqualified
                        pilots_disqualified.append((driver, race))

                    if "Laps" in data:
                        laps_data = data["Laps"]
                        if not laps_data or not any(laps_data.values()):
                            # Aggiungi una tupla (pilota, GP) alla lista pilots_without_laps
                            pilots_without_laps.append((driver, race))
                    else:
                        # Aggiungi una tupla (pilota, GP) alla lista pilots_disqualified_laps
                        pilots_disqualified_laps.append((driver, race))

                    if "Qualifying" not in data and "Laps" not in data:
                        # Aggiungi una tupla (pilota, GP) alla lista pilots_without_qualifying_laps
                        pilots_without_qualifying_laps.append((driver, race))

# Stampa i risultati
print("Piloti senza dati di Qualifying:")
for driver, race in pilots_without_qualifying:
    print(f"Pilota: {driver}, GP: {race}")

print("\nPiloti con dati di Qualifying mancanti:")
for driver, race in pilots_disqualified:
    print(f"Pilota: {driver}, GP: {race}")

print("\nPiloti senza dati di Laps:")
for driver, race in pilots_without_laps:
    print(f"Pilota: {driver}, GP: {race}, Dati di Laps mancanti")

print("\nPiloti con dati di Laps mancanti:")
for driver, race in pilots_disqualified_laps:
    print(f"Pilota: {driver}, GP: {race}, Dati di Laps mancanti")

print("\nPiloti senza dati di Qualifying e Laps:")
for driver, race in pilots_without_qualifying_laps:
    print(f"Pilota: {driver}, GP: {race}, Dati di Qualifying e Laps mancanti")