import pymongo
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"
# List of collection names
collection_names = ["2013", "2014", "2021", "2022"]

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]

# Funzione di conversione del tempo in secondi
def convert_to_seconds(time_str):
    if time_str is None:
        return None

    time_parts = time_str.split(':')
    minutes = int(time_parts[0])
    seconds_parts = time_parts[1].split('.')
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1])

    total_seconds = minutes * 60 + seconds + milliseconds / 1000
    return total_seconds

# Esegui la query per trovare tutti i documenti che hanno la struttura desiderata
for collection_name in collection_names:
    # Access the collection
    collection = db[collection_name]

    # Query documents from the collection
    query = {}
    cursor = collection.find(query)

    print(f'\n{collection_name} \n')

    # Rest of your code
    for document in cursor:
        driver_car = {}
        gps = []
        results_qual = []
        results_laps = []
        results_circuit = []
        qtime = {}
        laps_data = {}
        circuit_data = {}
        wq_dict = {}
        speed_dict = {}
        print(f'DRIVER CHECK')
        print(f'Number of drivers: {len(document) - 1}\n')
        for driver, driver_data in document.items():
            if isinstance(driver_data, dict):
                num_gps = len(driver_data) - 1
                if num_gps not in gps:
                    gps.append(num_gps)
                if "Car" in driver_data:
                    driver_car[driver] = driver_data["Car"]
                    qual = 0
                    notqual = 0
                    laps = 0
                    notlaps = 0
                    circ = 0
                    notcirc = 0

                    for gp, gp_data in driver_data.items():
                        if gp != "_id" and gp != "Car":
                            if not "Qualifying" in gp_data:
                                notqual += 1
                            else:
                                qual += 1
                            if not "Laps" in gp_data:
                                notlaps += 1
                            else:
                                laps += 1
                            if not "Circuit" in gp_data:
                                notcirc += 1
                            else:
                                circ += 1
                            if "Qualifying" in gp_data:

                                if not ("Q1 Time" or "Q2 Time" or "Q3 Time") in gp_data["Qualifying"]:
                                    print(f'{driver}, {gp}, not ok')
                                if "Q1 Time" and "Q2 Time" and "Q3 Time" in gp_data["Qualifying"]:
                                    if gp_data["Qualifying"]["Q1 Time"]:

                                        if gp not in qtime:
                                            qtime[gp] = {"Q1": 1, "Q2": 0, "Q3": 0, "NQT": 0}
                                        else:
                                            qtime[gp]["Q1"] += 1

                                    if gp_data["Qualifying"]["Q2 Time"]:
                                        qtime[gp]["Q2"] += 1

                                    if gp_data["Qualifying"]["Q3 Time"]:
                                        qtime[gp]["Q3"] += 1

                                    if gp_data["Qualifying"]["Q1 Time"] == [] and gp_data["Qualifying"][
                                        "Q2 Time"] == [] and gp_data["Qualifying"]["Q3 Time"] == []:
                                        if gp in qtime:
                                            qtime[gp]["NQT"] += 1
                                        else:
                                            qtime[gp] = {"Q1": 0, "Q2": 0, "Q3": 0, "NQT": 1}

                                    if gp_data["Qualifying"]["Q1 Time"] == [] and gp_data["Qualifying"][
                                        "Q2 Time"] == [] and gp_data["Qualifying"]["Q3 Time"] != []:
                                        print(f'{driver}, {gp}, error Q3')

                                    if gp_data["Qualifying"]["Q1 Time"] == [] and gp_data["Qualifying"][
                                        "Q2 Time"] != [] and gp_data["Qualifying"]["Q3 Time"] != []:
                                        print(f'{driver}, {gp}, error Q2 Q3')

                                if gp_data["Qualifying"]["Weather Condition"] and (
                                        gp_data["Qualifying"]["Weather Condition"] == "rain" or gp_data["Qualifying"][
                                    "Weather Condition"] == "sun"):
                                    if gp not in wq_dict:
                                        wq_dict[gp] = {"number of wq": 1, "number of wr": 0}
                                    else:
                                        wq_dict[gp]["number of wq"] += 1

                            if "Laps" in gp_data:
                                if len(gp_data["Laps"]) == len(gp_data["Laps"].values()):
                                    if driver not in laps_data:
                                        laps_data[driver] = {}
                                    if gp not in laps_data[driver]:
                                        laps_data[driver][gp] = len(gp_data["Laps"])
                                else:
                                    print(f'{driver}, {gp}, {len(gp_data["Laps"])}, {len(gp_data["Laps"].values())}')

                                if gp_data["Laps"]["Weather Condition"] and (
                                        gp_data["Laps"]["Weather Condition"] == "rain" or gp_data["Laps"][
                                    "Weather Condition"] == "sun"):
                                    if gp not in wq_dict:
                                        wq_dict[gp] = {"number of wq": wq_dict[gp]["number of wq"], "number of wr": 1}
                                    else:
                                        wq_dict[gp]["number of wr"] += 1

                            if "Laps" not in gp_data:
                                if driver not in laps_data:
                                    laps_data[driver] = {}
                                if gp not in laps_data[driver]:
                                    laps_data[driver][gp] = 0

                            if "Circuit" in gp_data:
                                if len(gp_data["Circuit"]) == len(gp_data["Circuit"].values()):
                                    if driver not in circuit_data:
                                        circuit_data[driver] = {}
                                    if gp not in circuit_data[driver]:
                                        circuit_data[driver][gp] = len(gp_data["Circuit"])
                                else:
                                    print(
                                        f'{driver}, {gp}, {len(gp_data["Circuit"])}, {len(gp_data["Circuit"].values())}')
                        if "km/h" in gp_data:
                            if gp_data["km/h"]:
                                if gp not in speed_dict:
                                    speed_dict[gp] = {"number of speed data": 1}
                                else:
                                    speed_dict[gp]["number of speed data"] += 1

                    result_qual = {
                        "Driver": driver,
                        "Q": qual,
                        "NQ": notqual,
                        "L": laps,
                        "NL": notlaps,
                        "C": circ,
                        "NC": notcirc,
                    }

                    results_qual.append(result_qual)

        # GP field
        print(f'GPs NUMBER CHECK')
        if len(gps) == 1:
            print(f'Number of GPs for each driver: {gps[0]}\n')
        # Car field
        print(f'CAR FIELD CHECK')
        print(
            f'Number of "Car" fields: {len(driver_car)}, number of "Car" values: {len(driver_car.values())}\n')

        print(f'QUALIFYING, LAPS AND CIRCUIT FIELDS CHECK')
        # Crea un DataFrame da results
        df_qual = pd.DataFrame(results_qual)
        total_row_qual = {
            "Driver": "Tot",
            "Q": df_qual["Q"].sum(),
            "NQ": df_qual["NQ"].sum(),
            "L": df_qual["L"].sum(),
            "NL": df_qual["NL"].sum(),
            "C": df_qual["C"].sum(),
            "NC": df_qual["NC"].sum()
        }

        # Creazione di un DataFrame per la riga "Tot"
        total_df_qual = pd.DataFrame(total_row_qual, index=[
            len(df_qual)])  # L'indice viene impostato per far corrispondere le dimensioni

        # Unione dei DataFrame
        df_qual = pd.concat([df_qual, total_df_qual])

        print(f'{df_qual}\n')

        print(f'SPEED CHECK')

        df_speed = pd.DataFrame(speed_dict).transpose()
        print(df_speed)

        print(f'\nQ1, Q2, Q3 CHECK')

        df_qtime = pd.DataFrame(qtime).transpose()

        print(f'{df_qtime}\n')

        print(f'NUMBER OF LAPS CHECK')
        # Creazione del DataFrame
        df_laps = pd.DataFrame(laps_data).transpose()

        # Trasponi il DataFrame in modo che i nomi dei gruppi siano sulla colonna

        print(df_laps.to_string())

        print(f'\nWEATHER CONDITION QUALIFYING CHECK')

        df_weather = pd.DataFrame(wq_dict).transpose()
        print(df_weather)

        print(f'\nCIRCUIT NAME, CIRCUIT LENGTH AND CIRCUIT TURNS CHECK')
        df_circ = pd.DataFrame(circuit_data).transpose()

        # Stampa il DataFrame aggiornato
        print(df_circ.to_string())