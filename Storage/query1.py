import pymongo
import json
import matplotlib.pyplot as plt

# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"
collection_name = "2013"
collection_name1 = "2014"

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]
collection = db[collection_name]
collection1 = db[collection_name1]

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
query = {}
cursor = collection.find(query)
cursor1 = collection1.find(query)

# Creazione del dizionario per i dati dei piloti e tempi per ogni GP
data_2013 = {}
data_2014 = {}

# Cicla sui piloti e sui Gran Premi (GP) per ottenere il tempo minimo tra Q1, Q2 e Q3 delle qualifiche per l'anno 2013
for document in cursor:
    for driver, race_data in document.items():
        if isinstance(race_data, dict):
            for gp, qualifying_data in race_data.items():
                if gp != "_id":
                    if "Qualifying" in qualifying_data:
                        if qualifying_data.get("Qualifying").get("Weather Condition") == "sun":
                            qualifying_times = qualifying_data["Qualifying"]
                            q1_time = min(qualifying_times.get("Q1 Time", [])) if qualifying_times.get("Q1 Time") else None
                            q2_time = min(qualifying_times.get("Q2 Time", [])) if qualifying_times.get("Q2 Time") else None
                            q3_time = min(qualifying_times.get("Q3 Time", [])) if qualifying_times.get("Q3 Time") else None
                            min_time = min(filter(None, [q1_time, q2_time, q3_time])) if any([q1_time, q2_time, q3_time]) else None
                            min_time_seconds = convert_to_seconds(min_time)
                            if gp in data_2013:
                                data_2013[gp].append((driver, min_time_seconds))
                            else:
                                data_2013[gp] = [(driver, min_time_seconds)]
for document in cursor1:
    for driver, race_data in document.items():
        if isinstance(race_data, dict):
            for gp, qualifying_data in race_data.items():
                if gp != "_id":
                    if "Qualifying" in qualifying_data:
                        if qualifying_data.get("Qualifying").get("Weather Condition") == "sun":
                            qualifying_times = qualifying_data["Qualifying"]
                            q1_time = min(qualifying_times.get("Q1 Time", [])) if qualifying_times.get("Q1 Time") else None
                            q2_time = min(qualifying_times.get("Q2 Time", [])) if qualifying_times.get("Q2 Time") else None
                            q3_time = min(qualifying_times.get("Q3 Time", [])) if qualifying_times.get("Q3 Time") else None
                            min_time = min(filter(None, [q1_time, q2_time, q3_time])) if any([q1_time, q2_time, q3_time]) else None
                            min_time_seconds = convert_to_seconds(min_time)

                            if gp in data_2014:
                                data_2014[gp].append((driver, min_time_seconds))
                            else:
                                data_2014[gp] = [(driver, min_time_seconds)]

# Chiudi la connessione
client.close()

# Creazione dei grafici per ogni GP
for gp, data in data_2013.items():
    drivers_2013, times_2013 = zip(*data)
    drivers_2014 = []
    times_2014 = []
    lines = [] 
    for driver, time_2013 in zip(drivers_2013, times_2013):
        for driver_2014, time_2014 in data_2014.get(gp, []):
            if driver == driver_2014:
                drivers_2014.append(driver)
                times_2014.append(time_2014)
                if time_2013 is not None and time_2014 is not None:
                    lines.append((driver, time_2013, time_2014))
                break

    fig, ax = plt.subplots(figsize=(10, 8))  # Set the figure size (adjust as needed)

    ax.scatter(drivers_2013, times_2013, color='blue', label='2013')
    ax.scatter(drivers_2014, times_2014, color='red', label='2014')

    ax.set_xlabel('Piloti')
    ax.set_ylabel('Tempo (secondi)')
    ax.set_title(f'Qualifiche {gp}')
    ax.legend()

    # Rotate the x-axis tick labels for better readability
    plt.xticks(rotation=90)

 # Traccia le linee solo per i piloti con tempi validi
    for driver, time_2013, time_2014 in lines:
        ax.vlines(driver, time_2013, time_2014, colors='gray', linestyles='dashed', linewidth=1)

    plt.tight_layout() 
    plt.show()

import pymongo
import json
import matplotlib.pyplot as plt

# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"
collection_name = "2013"
collection_name1 = "2014"

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]
collection = db[collection_name]
collection1 = db[collection_name1]


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
query = {}
cursor = collection.find(query)
cursor1 = collection1.find(query)

# Creazione del dizionario per i dati dei piloti e tempi per ogni GP
data_2013 = {}
data_2014 = {}

# Cicla sui piloti e sui Gran Premi (GP) per ottenere il tempo minimo tra Q1, Q2 e Q3 delle qualifiche per l'anno 2013
for document in cursor:
    for driver, race_data in document.items():
        if isinstance(race_data, dict):
            for gp, qualifying_data in race_data.items():
                if gp != "_id":
                    if "Qualifying" in qualifying_data:
                        qualifying_times = qualifying_data["Qualifying"]
                        q1_time = min(qualifying_times.get("Q1 Time", [])) if qualifying_times.get("Q1 Time") else None
                        q2_time = min(qualifying_times.get("Q2 Time", [])) if qualifying_times.get("Q2 Time") else None
                        q3_time = min(qualifying_times.get("Q3 Time", [])) if qualifying_times.get("Q3 Time") else None
                        min_time = min(filter(None, [q1_time, q2_time, q3_time])) if any(
                            [q1_time, q2_time, q3_time]) else None
                        min_time_seconds = convert_to_seconds(min_time)

                        # Aggiungi i dati al dizionario data_2013
                        if gp in data_2013:
                            data_2013[gp].append({driver: {"Time": min_time_seconds, "Car": race_data["Car"]}})
                        else:
                            data_2013[gp] = [{driver: {"Time": min_time_seconds, "Car": race_data["Car"]}}]

# Cicla sui piloti e sui Gran Premi (GP) per ottenere il tempo minimo tra Q1, Q2 e Q3 delle qualifiche per l'anno 2014
for document in cursor1:
    for driver, race_data in document.items():
        if isinstance(race_data, dict):
            for gp, qualifying_data in race_data.items():
                if gp != "_id":
                    if "Qualifying" in qualifying_data:
                        qualifying_times = qualifying_data["Qualifying"]
                        q1_time = min(qualifying_times.get("Q1 Time", [])) if qualifying_times.get("Q1 Time") else None
                        q2_time = min(qualifying_times.get("Q2 Time", [])) if qualifying_times.get("Q2 Time") else None
                        q3_time = min(qualifying_times.get("Q3 Time", [])) if qualifying_times.get("Q3 Time") else None
                        min_time = min(filter(None, [q1_time, q2_time, q3_time])) if any(
                            [q1_time, q2_time, q3_time]) else None
                        min_time_seconds = convert_to_seconds(min_time)

                        # Aggiungi i dati al dizionario data_2014
                        if gp in data_2014:
                            data_2014[gp].append({driver: {"Time": min_time_seconds, "Car": race_data["Car"]}})
                        else:
                            data_2014[gp] = [{driver: {"Time": min_time_seconds, "Car": race_data["Car"]}}]


# Dizionario per i dati aggregati del 2013
aggregated_data_2013 = {}

# Dizionario per i dati aggregati del 2014
aggregated_data_2014 = {}

# Groupby e calcolo della media dei min_time per l'anno 2013
for gp, driver_data in data_2013.items():
    for driver_info in driver_data:
        driver = next(iter(driver_info))
        min_time = driver_info[driver]["Time"]
        car = driver_info[driver]["Car"]
        if car in aggregated_data_2013:
            aggregated_data_2013[car].append(min_time)
        else:
            aggregated_data_2013[car] = [min_time]

# Groupby e calcolo della media dei min_time per l'anno 2014
for gp, driver_data in data_2014.items():
    for driver_info in driver_data:
        driver = next(iter(driver_info))
        min_time = driver_info[driver]["Time"]
        car = driver_info[driver]["Car"]
        if car in aggregated_data_2014:
            aggregated_data_2014[car].append(min_time)
        else:
            aggregated_data_2014[car] = [min_time]



# Calcolo della media per ogni "Car" per l'anno 2013
average_data_2013 = {}
for car, min_times in aggregated_data_2013.items():
    # Filtra i valori None dalla lista min_times
    min_times_filtered = [time for time in min_times if time is not None]
    if min_times_filtered:
        average_time = sum(min_times_filtered) / len(min_times_filtered)
    else:
        average_time = None
    average_data_2013[car] = average_time

print(average_data_2013)

# Calcolo della media per ogni "Car" per l'anno 2014
average_data_2014 = {}
for car, min_times in aggregated_data_2014.items():
    # Filtra i valori None dalla lista min_times
    min_times_filtered = [time for time in min_times if time is not None]
    if min_times_filtered:
        average_time = sum(min_times_filtered) / len(min_times_filtered)
    else:
        average_time = None
    average_data_2014[car] = average_time

print(average_data_2014)
# Chiudi la connessione
client.close()

# Controllo delle scuderie che compaiono in entrambi gli anni
common_teams = set(average_data_2013.keys()) & set(average_data_2014.keys())

# Creazione dello scatterplot
x = []
y_2013 = []
y_2014 = []

for team in common_teams:
    x.append(team)
    y_2013.append(average_data_2013[team])
    y_2014.append(average_data_2014[team])

plt.scatter(x, y_2013, color='blue', label='2013')
plt.scatter(x, y_2014, color='red', label='2014')

plt.xlabel('Scuderia')
plt.ylabel('Secondi')
plt.title('Tempi medi di qualifica per scuderia (2013 vs 2014)')
plt.legend()
plt.xticks(rotation=45)
# Aggiunta delle linee tratteggiate grigie che collegano i punti
for i in range(len(x)):
    plt.plot([x[i], x[i]], [y_2013[i], y_2014[i]], color='gray', linestyle='dotted')


plt.show()