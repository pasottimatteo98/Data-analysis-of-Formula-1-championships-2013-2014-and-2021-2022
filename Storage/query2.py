import pymongo
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import iqr

# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"
collection_name = "2013"
collection_name1 = "2014"
collection_name2 = "2021"
collection_name3 = "2022"

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]
collection = db[collection_name]
collection1 = db[collection_name1]
collection2 = db[collection_name2]
collection3 = db[collection_name3]


# Funzione di conversione del tempo in secondi
def convert_to_seconds(time_str):
    if time_str is None or time_str == "Weather Condition":
        return None

    time_parts = time_str.split(':')
    if len(time_parts) == 2:
        minutes = int(time_parts[0])
        seconds = float(time_parts[1])
    else:
        minutes = int(time_parts[0])
        seconds = float('.'.join(time_parts[1:]))

    total_seconds = minutes * 60 + seconds
    return total_seconds


# Funzione per rimuovere gli outliers dai dati
def remove_outliers(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr_value = iqr(data)
    lower_bound = q1 - 1.5 * iqr_value
    upper_bound = q3 + 1.5 * iqr_value
    return [x for x in data if lower_bound <= x <= upper_bound]


 


# Esegui la query per trovare tutti i documenti che hanno la struttura desiderata
query = {}
cursor = collection.find(query)
cursor1 = collection1.find(query)
cursor2 = collection2.find(query)
cursor3 = collection3.find(query)

#--------------------2013---------------------------------------

# Dizionario per memorizzare i dati dei laps per ogni pilota e GP
laps_data = {}
max_laps = {}
car = {}
# Cicla sui Gran Premi (GP)
for document in cursor:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get("Laps")
                        if laps:
                            driver_laps = {}
                            for lap_num, lap_time in laps.items():
                                if lap_num == "Weather Condition":
                                    continue
                                if lap_time == "sun":
                                    continue
                                lap_time_sec = convert_to_seconds(lap_time)
                                driver_laps[lap_num] = lap_time_sec

                            if driver not in laps_data:
                                laps_data[driver] = {}
                            laps_data[driver][gp] = driver_laps

                            if int(len(laps)-1) > max_laps.get(gp, 0):
                                max_laps[gp] = len(laps)-1
                car[driver] = driver_data.get("Car")


# Dizionario per memorizzare i dati filtrati dei laps per ogni pilota e GP
filtered_laps_data = {}

# Dizionario per memorizzare i valori di lap_num e lap_time_sec
lap_info_data = {}
# Genera i boxplot per ogni pilota in ogni Gran Premio e filtra gli outliers
for driver, driver_data in laps_data.items():
    for gp, laps in driver_data.items():
        # print(laps)
        # plt.figure()
        # plt.boxplot(laps.values())  # Utilizziamo solo i valori dei tempi dei giri per il boxplot
        # plt.title(f"Laps per il pilota {driver} nel Gran Premio {gp}")
        # plt.xlabel("Laps")
        # plt.ylabel("Tempo (secondi)")

        # Rimuovi gli outliers dai laps e aggiorna il dizionario dei dati filtrati
        filtered_laps = remove_outliers(list(laps.values()))
        filtered_laps_data.setdefault(driver, {})[gp] = filtered_laps

        # Print del dizionario dei dati filtrati per ogni pilota e GP
        #print(f"Dati filtrati per il pilota {driver}, Gran Premio {gp}:")
        for lap_num, lap_time_sec in laps.items():
            if lap_time_sec in filtered_laps:
                #print(f"Giro {lap_num}: {lap_time_sec} secondi")
                lap_info_data.setdefault(driver, {}).setdefault(gp, {})[lap_num] = lap_time_sec

        # plt.show()
# Utilizzo del dizionario dei valori di lap_num e lap_time_sec
# print("Informazioni sui giri per Fernando Alonso:")
# for gp, laps_info in lap_info_data.get("Fernando Alonso", {}).items():
#    print(f"Gran Premio {gp}:")
#    for lap_num, lap_time_sec in laps_info.items():
#        print(f"Giro {lap_num}: {lap_time_sec} secondi")

#--------------------2014---------------------------------------

# Dizionario per memorizzare i dati dei laps per ogni pilota e GP
laps_data1 = {}
max_laps1 = {}
car1 = {}
# Cicla sui Gran Premi (GP)
for document in cursor1:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get("Laps")
                        if laps:
                            driver_laps = {}
                            for lap_num, lap_time in laps.items():
                                if lap_num == "Weather Condition":
                                    continue
                                if lap_time == "sun":
                                    continue
                                lap_time_sec = convert_to_seconds(lap_time)
                                driver_laps[lap_num] = lap_time_sec

                            if driver not in laps_data1:
                                laps_data1[driver] = {}
                            laps_data1[driver][gp] = driver_laps

                            if int(len(laps)-1) > max_laps1.get(gp, 0):
                                max_laps1[gp] = len(laps)-1
                car1[driver] = driver_data.get("Car")


# Dizionario per memorizzare i dati filtrati dei laps per ogni pilota e GP
filtered_laps_data1 = {}

# Dizionario per memorizzare i valori di lap_num e lap_time_sec
lap_info_data1 = {}
# Genera i boxplot per ogni pilota in ogni Gran Premio e filtra gli outliers
for driver, driver_data in laps_data1.items():
    for gp, laps in driver_data.items():
        # print(laps)

        # plt.figure()
        # plt.boxplot(laps.values())  # Utilizziamo solo i valori dei tempi dei giri per il boxplot
        # plt.title(f"Laps per il pilota {driver} nel Gran Premio {gp}")
        # plt.xlabel("Laps")
        # plt.ylabel("Tempo (secondi)")

        # Rimuovi gli outliers dai laps e aggiorna il dizionario dei dati filtrati
        filtered_laps1 = remove_outliers(list(laps.values()))
        filtered_laps_data1.setdefault(driver, {})[gp] = filtered_laps1

        # Print del dizionario dei dati filtrati per ogni pilota e GP
        #print(f"Dati filtrati per il pilota {driver}, Gran Premio {gp}:")
        for lap_num, lap_time_sec in laps.items():
            if lap_time_sec in filtered_laps1:
                #print(f"Giro {lap_num}: {lap_time_sec} secondi")
                lap_info_data1.setdefault(driver, {}).setdefault(gp, {})[lap_num] = lap_time_sec

        # plt.show()

#--------------------2021---------------------------------------

# Dizionario per memorizzare i dati dei laps per ogni pilota e GP
laps_data2 = {}
max_laps2 = {}
car2 = {}
# Cicla sui Gran Premi (GP)
for document in cursor2:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get("Laps")
                        if laps:
                            driver_laps = {}
                            for lap_num, lap_time in laps.items():
                                if lap_num == "Weather Condition":
                                    continue
                                if lap_time == "sun":
                                    continue
                                lap_time_sec = convert_to_seconds(lap_time)
                                driver_laps[lap_num] = lap_time_sec

                            if driver not in laps_data2:
                                laps_data2[driver] = {}
                            laps_data2[driver][gp] = driver_laps

                            if int(len(laps)-1) > max_laps2.get(gp, 0):
                                max_laps2[gp] = len(laps)-1
                car2[driver] = driver_data.get("Car")


# Dizionario per memorizzare i dati filtrati dei laps per ogni pilota e GP
filtered_laps_data2 = {}

# Dizionario per memorizzare i valori di lap_num e lap_time_sec
lap_info_data2 = {}

# Genera i boxplot per ogni pilota in ogni Gran Premio e filtra gli outliers
for driver, driver_data in laps_data2.items():
    for gp, laps in driver_data.items():
        # print(laps)

        # plt.figure()
        # plt.boxplot(laps.values())  # Utilizziamo solo i valori dei tempi dei giri per il boxplot
        # plt.title(f"Laps per il pilota {driver} nel Gran Premio {gp}")
        # plt.xlabel("Laps")
        # plt.ylabel("Tempo (secondi)")

        # Rimuovi gli outliers dai laps e aggiorna il dizionario dei dati filtrati
        filtered_laps2 = remove_outliers(list(laps.values()))
        filtered_laps_data2.setdefault(driver, {})[gp] = filtered_laps2

        # Print del dizionario dei dati filtrati per ogni pilota e GP
        #print(f"Dati filtrati per il pilota {driver}, Gran Premio {gp}:")
        for lap_num, lap_time_sec in laps.items():
            if lap_time_sec in filtered_laps2:
                #print(f"Giro {lap_num}: {lap_time_sec} secondi")
                lap_info_data2.setdefault(driver, {}).setdefault(gp, {})[lap_num] = lap_time_sec

        # plt.show()

#--------------------2022---------------------------------------

# Dizionario per memorizzare i dati dei laps per ogni pilota e GP
laps_data3 = {}
max_laps3 = {}
car3 = {}
# Cicla sui Gran Premi (GP)
for document in cursor3:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get("Laps")
                        if laps:
                            driver_laps = {}
                            for lap_num, lap_time in laps.items():
                                if lap_num == "Weather Condition":
                                    continue
                                if lap_time == "sun":
                                    continue
                                lap_time_sec = convert_to_seconds(lap_time)
                                driver_laps[lap_num] = lap_time_sec

                            if driver not in laps_data3:
                                laps_data3[driver] = {}
                            laps_data3[driver][gp] = driver_laps

                            if int(len(laps)-1) > max_laps3.get(gp, 0):
                                max_laps3[gp] = len(laps)-1
                car3[driver] = driver_data.get("Car")


# Dizionario per memorizzare i dati filtrati dei laps per ogni pilota e GP
filtered_laps_data3 = {}

# Dizionario per memorizzare i valori di lap_num e lap_time_sec
lap_info_data3 = {}
# Genera i boxplot per ogni pilota in ogni Gran Premio e filtra gli outliers
for driver, driver_data in laps_data3.items():
    for gp, laps in driver_data.items():
        # print(laps)

        # plt.figure()
        # plt.boxplot(laps.values())  # Utilizziamo solo i valori dei tempi dei giri per il boxplot
        # plt.title(f"Laps per il pilota {driver} nel Gran Premio {gp}")
        # plt.xlabel("Laps")
        # plt.ylabel("Tempo (secondi)")

        # Rimuovi gli outliers dai laps e aggiorna il dizionario dei dati filtrati
        filtered_laps3 = remove_outliers(list(laps.values()))
        filtered_laps_data3.setdefault(driver, {})[gp] = filtered_laps3

        # Print del dizionario dei dati filtrati per ogni pilota e GP
        #print(f"Dati filtrati per il pilota {driver}, Gran Premio {gp}:")
        for lap_num, lap_time_sec in laps.items():
            if lap_time_sec in filtered_laps3:
                #print(f"Giro {lap_num}: {lap_time_sec} secondi")
                lap_info_data3.setdefault(driver, {}).setdefault(gp, {})[lap_num] = lap_time_sec

        # plt.show()
#----------------------------------------------------------------------
# Inizio seconda parte

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]
collection = db[collection_name]
collection1 = db[collection_name1]
collection2 = db[collection_name2]
collection3 = db[collection_name3]



# Funzione di conversione del tempo in secondi
def convert_to_seconds(time_str):
    if time_str is None or time_str == "Weather Condition":
        return None

    time_parts = time_str.split(':')
    if len(time_parts) == 2:
        minutes = int(time_parts[0])
        seconds = float(time_parts[1])
    else:
        minutes = int(time_parts[0])
        seconds = float('.'.join(time_parts[1:]))

    total_seconds = minutes * 60 + seconds
    return total_seconds


# Esegui la query per trovare tutti i documenti che hanno la struttura desiderata
query = {}
cursor = collection.find(query)
cursor1 = collection1.find(query)
cursor2 = collection2.find(query)
cursor3 = collection3.find(query)
# Dizionari per memorizzare i dati dei tempi medi delle sezioni per ogni pilota e GP
averages_2013 = {}
averages_2014 = {}
averages_2021 = {}
averages_2022 = {}

#---------------------------2013-------------------------------
# Cicla sui Gran Premi (GP) nel 2013
for document in cursor:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get(
                            "Laps")  # Usa il metodo get per gestire il caso in cui "Laps" non sia presente
                        if laps and laps.get("Weather Condition") == "sun":
                            max_laps_driver = max_laps[gp]
                            num_times_per_section = int(max_laps_driver) // 3
                            num_times_per_section3 = int(max_laps_driver) - 2 * int(num_times_per_section)
                            section_1 = []
                            section_2 = []
                            section_3 = []
                            # section_averages = []

                            # Verifica se il pilota e il Gran Premio sono presenti in lap_info_data
                            if driver in lap_info_data and gp in lap_info_data[driver]:
                                driver_laps_info = lap_info_data[driver][gp]


                                for lap_num, lap_time in laps.items():
                                    if lap_num == "Weather Condition":
                                        continue
                                    lap_time_sec = convert_to_seconds(lap_time)
                                    if int(lap_num) in range(1,
                                                             int(num_times_per_section) + 1) and lap_num in driver_laps_info:
                                        section_1.append(lap_time_sec)

                                    elif int(lap_num) in range(int(num_times_per_section) + 1,
                                                               2 * int(num_times_per_section) + 1) and lap_num in driver_laps_info:
                                        section_2.append(lap_time_sec)
                                    elif int(lap_num) in range(2 * int(num_times_per_section) + 1,
                                                               int(max_laps_driver) + 1) and lap_num in driver_laps_info:
                                        section_3.append(lap_time_sec)

                            section_averages_1_2013 = sum(section_1) / len(section_1) if section_1 else 0.0
                            section_averages_2_2013 = sum(section_2) / len(section_2) if section_2 else 0.0
                            section_averages_3_2013 = sum(section_3) / len(section_3) if section_3 else 0.0
                            # Memorizza i tempi medi delle sezioni per ogni pilota e GP nel dizionario
                            if gp not in averages_2013:
                                averages_2013[gp] = {}
                            averages_2013[gp][driver] = [section_averages_1_2013, section_averages_2_2013,
                                                         section_averages_3_2013]
                            #print("qui mi blocco")
                            #print("Gran Premio:", gp)
                            #print("Pilota con il maggior numero di laps percorsi:", max_laps_driver)
                            #print("Numero di tempi per sezione 1:", num_times_per_section)
                            #print("Numero di tempi per sezione 2:", num_times_per_section)
                            #print("Numero di tempi per sezione 3:", num_times_per_section3)
                            #print(f"Pilota: {driver}, Sezione 1: {section_averages_1_2013} secondi")
                            #print(f"Pilota: {driver}, Sezione 2: {section_averages_2_2013} secondi")
                            #print(f"Pilota: {driver}, Sezione 3: {section_averages_3_2013} secondi")
                            #print()


#----------------------------2014-----------------------------------------
# Cicla sui Gran Premi (GP) nel 2014

for document in cursor1:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get(
                            "Laps")  # Usa il metodo get per gestire il caso in cui "Laps" non sia presente
                        if laps and laps.get("Weather Condition") == "sun":
                            max_laps_driver = max_laps1[gp]
                            num_times_per_section = int(max_laps_driver) // 3
                            num_times_per_section3 = int(max_laps_driver) - 2 * int(num_times_per_section)
                            section_1 = []
                            section_2 = []
                            section_3 = []
                            # section_averages = []

                            # Verifica se il pilota e il Gran Premio sono presenti in lap_info_data
                            if driver in lap_info_data1 and gp in lap_info_data1[driver]:
                                driver_laps_info1 = lap_info_data1[driver][gp]

                                for lap_num, lap_time in laps.items():
                                    if lap_num == "Weather Condition":
                                        continue
                                    lap_time_sec = convert_to_seconds(lap_time)
                                    if int(lap_num) in range(1,
                                                             int(num_times_per_section) + 1) and lap_num in driver_laps_info1:
                                        section_1.append(lap_time_sec)

                                    elif int(lap_num) in range(int(num_times_per_section) + 1,
                                                               2 * int(num_times_per_section) + 1) and lap_num in driver_laps_info1:
                                        section_2.append(lap_time_sec)
                                    elif int(lap_num) in range(2 * int(num_times_per_section) + 1,
                                                               int(max_laps_driver) + 1) and lap_num in driver_laps_info1:
                                        section_3.append(lap_time_sec)


                            section_averages_1_2014 = sum(section_1) / len(section_1) if section_1 else 0.0
                            section_averages_2_2014 = sum(section_2) / len(section_2) if section_2 else 0.0
                            section_averages_3_2014 = sum(section_3) / len(section_3) if section_3 else 0.0
                            # Memorizza i tempi medi delle sezioni per ogni pilota e GP nel dizionario
                            if gp not in averages_2014:
                                averages_2014[gp] = {}
                            averages_2014[gp][driver] = [section_averages_1_2014, section_averages_2_2014,
                                                         section_averages_3_2014]

                            #print("Gran Premio:", gp)
                            #print("Pilota con il maggior numero di laps percorsi:", max_laps_driver)
                            #print("Numero di tempi per sezione 1:", num_times_per_section)
                            #print("Numero di tempi per sezione 2:", num_times_per_section)
                            #print("Numero di tempi per sezione 3:", num_times_per_section3)
                            #print(f"Pilota: {driver}, Sezione 1: {section_averages_1_2014} secondi")
                            #print(f"Pilota: {driver}, Sezione 2: {section_averages_2_2014} secondi")
                            #print(f"Pilota: {driver}, Sezione 3: {section_averages_3_2014} secondi")
                            #print()

#----------------------------2021-----------------------------
# Cicla sui Gran Premi (GP) nel 2021

for document in cursor2:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get(
                            "Laps")  # Usa il metodo get per gestire il caso in cui "Laps" non sia presente
                        if laps and laps.get("Weather Condition") == "sun":
                            max_laps_driver = max_laps2[gp]
                            num_times_per_section = int(max_laps_driver) // 3
                            num_times_per_section3 = int(max_laps_driver) - 2 * int(num_times_per_section)
                            section_1 = []
                            section_2 = []
                            section_3 = []
                            # section_averages = []

                            # Verifica se il pilota e il Gran Premio sono presenti in lap_info_data
                            if driver in lap_info_data2 and gp in lap_info_data2[driver]:
                                driver_laps_info2 = lap_info_data2[driver][gp]

                                for lap_num, lap_time in laps.items():
                                    if lap_num == "Weather Condition":
                                        continue
                                    lap_time_sec = convert_to_seconds(lap_time)
                                    if int(lap_num) in range(1,
                                                             int(num_times_per_section) + 1) and lap_num in driver_laps_info2:
                                        section_1.append(lap_time_sec)

                                    elif int(lap_num) in range(int(num_times_per_section) + 1,
                                                               2 * int(num_times_per_section) + 1) and lap_num in driver_laps_info2:
                                        section_2.append(lap_time_sec)
                                    elif int(lap_num) in range(2 * int(num_times_per_section) + 1,
                                                               int(max_laps_driver) + 1) and lap_num in driver_laps_info2:
                                        section_3.append(lap_time_sec)


                            section_averages_1_2021 = sum(section_1) / len(section_1) if section_1 else 0.0
                            section_averages_2_2021 = sum(section_2) / len(section_2) if section_2 else 0.0
                            section_averages_3_2021 = sum(section_3) / len(section_3) if section_3 else 0.0
                            # Memorizza i tempi medi delle sezioni per ogni pilota e GP nel dizionario
                            if gp not in averages_2021:
                                averages_2021[gp] = {}
                            averages_2021[gp][driver] = [section_averages_1_2021, section_averages_2_2021,
                                                         section_averages_3_2021]

                            #print("Gran Premio:", gp)
                            #print("Pilota con il maggior numero di laps percorsi:", max_laps_driver)
                            #print("Numero di tempi per sezione 1:", num_times_per_section)
                            #print("Numero di tempi per sezione 2:", num_times_per_section)
                            #print("Numero di tempi per sezione 3:", num_times_per_section3)
                            #print(f"Pilota: {driver}, Sezione 1: {section_averages_1_2014} secondi")
                            #print(f"Pilota: {driver}, Sezione 2: {section_averages_2_2014} secondi")
                            #print(f"Pilota: {driver}, Sezione 3: {section_averages_3_2014} secondi")
                            #print()
#----------------------------2022-----------------------------
# Cicla sui Gran Premi (GP) nel 2022

for document in cursor3:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get(
                            "Laps")  # Usa il metodo get per gestire il caso in cui "Laps" non sia presente
                        if laps and laps.get("Weather Condition") == "sun":
                            max_laps_driver = max_laps3[gp]
                            num_times_per_section = int(max_laps_driver) // 3
                            num_times_per_section3 = int(max_laps_driver) - 2 * int(num_times_per_section)
                            section_1 = []
                            section_2 = []
                            section_3 = []
                            # section_averages = []

                            # Verifica se il pilota e il Gran Premio sono presenti in lap_info_data
                            if driver in lap_info_data3 and gp in lap_info_data3[driver]:
                                driver_laps_info3= lap_info_data3[driver][gp]

                                for lap_num, lap_time in laps.items():
                                    if lap_num == "Weather Condition":
                                        continue
                                    lap_time_sec = convert_to_seconds(lap_time)
                                    if int(lap_num) in range(1,
                                                             int(num_times_per_section) + 1) and lap_num in driver_laps_info3:
                                        section_1.append(lap_time_sec)

                                    elif int(lap_num) in range(int(num_times_per_section) + 1,
                                                               2 * int(num_times_per_section) + 1) and lap_num in driver_laps_info3:
                                        section_2.append(lap_time_sec)
                                    elif int(lap_num) in range(2 * int(num_times_per_section) + 1,
                                                               int(max_laps_driver) + 1) and lap_num in driver_laps_info3:
                                        section_3.append(lap_time_sec)


                            section_averages_1_2022 = sum(section_1) / len(section_1) if section_1 else 0.0
                            section_averages_2_2022 = sum(section_2) / len(section_2) if section_2 else 0.0
                            section_averages_3_2022 = sum(section_3) / len(section_3) if section_3 else 0.0
                            # Memorizza i tempi medi delle sezioni per ogni pilota e GP nel dizionario
                            if gp not in averages_2022:
                                averages_2022[gp] = {}
                            averages_2022[gp][driver] = [section_averages_1_2022, section_averages_2_2022,
                                                         section_averages_3_2022]

                            #print("Gran Premio:", gp)
                            #print("Pilota con il maggior numero di laps percorsi:", max_laps_driver)
                            #print("Numero di tempi per sezione 1:", num_times_per_section)
                            #print("Numero di tempi per sezione 2:", num_times_per_section)
                            #print("Numero di tempi per sezione 3:", num_times_per_section3)
                            #print(f"Pilota: {driver}, Sezione 1: {section_averages_1_2014} secondi")
                            #print(f"Pilota: {driver}, Sezione 2: {section_averages_2_2014} secondi")
                            #print(f"Pilota: {driver}, Sezione 3: {section_averages_3_2014} secondi")
                            #print()
# Chiudi la connessione

client.close()

common_drivers = []
common_drivers1= []
drivers_2013 = []
drivers_2014 = []
drivers_2021 = []
drivers_2022 = []
for gp in averages_2013.keys():
    for driver in averages_2013[gp].keys():
        if driver not in drivers_2013:
            drivers_2013.append(driver)

for gp in averages_2014.keys():
    for driver in averages_2014[gp].keys():
        if driver not in drivers_2014:
            drivers_2014.append(driver)

for gp in averages_2021.keys():
    for driver in averages_2021[gp].keys():
        if driver not in drivers_2021:
            drivers_2021.append(driver)

for gp in averages_2022.keys():
    for driver in averages_2022[gp].keys():
        if driver not in drivers_2022:
            drivers_2022.append(driver)
#--------------------------------------------------------
for i in drivers_2013:
    if i in drivers_2014:
        common_drivers.append(i)

for i in drivers_2021:
    if i in drivers_2022:
        common_drivers1.append(i)

#--------------------------------------------------------

# Genera gli scatterplot per ogni GP del 2013-2014
for gp in averages_2013.keys():
    if gp in averages_2014.keys():

        section_averages_1_2013 = []
        section_averages_2_2013 = []
        section_averages_3_2013 = []

        # Nuova lista dei piloti per il 2014
        section_averages_1_2014 = []
        section_averages_2_2014 = []
        section_averages_3_2014 = []

        common_drivers2 = []

        for driver in common_drivers:
            if driver in averages_2013[gp] and driver in averages_2014[gp]:
                common_drivers2.append(driver)
                driver_data_2013 = averages_2013[gp][driver]
                driver_data_2014 = averages_2014[gp][driver]

                section_averages_1_2013.append(driver_data_2013[0])
                section_averages_2_2013.append(driver_data_2013[1])
                section_averages_3_2013.append(driver_data_2013[2])

                section_averages_1_2014.append(driver_data_2014[0])
                section_averages_2_2014.append(driver_data_2014[1])
                section_averages_3_2014.append(driver_data_2014[2])

        plt.figure(figsize=(10, 6))
        # Scatterplot per il 2013
        section_averages_1_2013_filtered = [value if value != 0 else None for value in section_averages_1_2013]
        section_averages_2_2013_filtered = [value if value != 0 else None for value in section_averages_2_2013]
        section_averages_3_2013_filtered = [value if value != 0 else None for value in section_averages_3_2013]

        if section_averages_1_2013_filtered:
            plt.scatter(range(len(section_averages_1_2013_filtered)), section_averages_1_2013_filtered,
                        color='orange', marker='^', label='Section 1 (2013)')

        if section_averages_2_2013_filtered:
            plt.scatter(range(len(section_averages_2_2013_filtered)), section_averages_2_2013_filtered,
                        color='green', marker='^', label='Section 2 (2013)')

        if section_averages_3_2013_filtered:
            plt.scatter(range(len(section_averages_3_2013_filtered)), section_averages_3_2013_filtered,
                        color='blue', marker='^', label='Section 3 (2013)')

        # Scatterplot per il 2014
        section_averages_1_2014_filtered = [value if value != 0 else None for value in section_averages_1_2014]
        section_averages_2_2014_filtered = [value if value != 0 else None for value in section_averages_2_2014]
        section_averages_3_2014_filtered = [value if value != 0 else None for value in section_averages_3_2014]

        if section_averages_1_2014_filtered:
            plt.scatter(range(len(section_averages_1_2014_filtered)), section_averages_1_2014_filtered,
                        color='orange', marker='*', label='Section 1 (2014)')

        if section_averages_2_2014_filtered:
            plt.scatter(range(len(section_averages_2_2014_filtered)), section_averages_2_2014_filtered,
                        color='green', marker='*', label='Section 2 (2014)')

        if section_averages_3_2014_filtered:
            plt.scatter(range(len(section_averages_3_2014_filtered)), section_averages_3_2014_filtered,
                        color='blue', marker='*', label='Section 3 (2014)')

        # Etichette degli assi x
        x_labels = common_drivers2
        plt.xlabel('Drivers')
        plt.ylabel('Time (s)')
        plt.title(f'Average section times {gp}')
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.xticks(range(len(x_labels)), x_labels, rotation=90)
        plt.tight_layout()
        plt.show()


# Genera gli scatterplot per ogni GP del 2021-2022
for gp in averages_2021.keys():
    if gp in averages_2022.keys():

        section_averages_1_2021 = []
        section_averages_2_2021 = []
        section_averages_3_2021 = []

        # Nuova lista dei piloti per il 2022
        section_averages_1_2022 = []
        section_averages_2_2022 = []
        section_averages_3_2022 = []

        common_drivers3 = []

        for driver in common_drivers1:
            if driver in averages_2021[gp] and driver in averages_2022[gp]:
                common_drivers3.append(driver)
                driver_data_2021 = averages_2021[gp][driver]
                driver_data_2022 = averages_2022[gp][driver]

                section_averages_1_2021.append(driver_data_2021[0])
                section_averages_2_2021.append(driver_data_2021[1])
                section_averages_3_2021.append(driver_data_2021[2])

                section_averages_1_2022.append(driver_data_2022[0])
                section_averages_2_2022.append(driver_data_2022[1])
                section_averages_3_2022.append(driver_data_2022[2])

        plt.figure(figsize=(10, 6))
        # Scatterplot per il 2013
        section_averages_1_2021_filtered = [value if value != 0 else None for value in section_averages_1_2021]
        section_averages_2_2021_filtered = [value if value != 0 else None for value in section_averages_2_2021]
        section_averages_3_2021_filtered = [value if value != 0 else None for value in section_averages_3_2021]

        if section_averages_1_2021_filtered:
            plt.scatter(range(len(section_averages_1_2021_filtered)), section_averages_1_2021_filtered,
                        color='orange', marker='^', label='Section 1 (2021)')

        if section_averages_2_2021_filtered:
            plt.scatter(range(len(section_averages_2_2021_filtered)), section_averages_2_2021_filtered,
                        color='green', marker='^', label='Section 2 (2021)')

        if section_averages_3_2021_filtered:
            plt.scatter(range(len(section_averages_3_2021_filtered)), section_averages_3_2021_filtered,
                        color='blue', marker='^', label='Section 3 (2021)')

        # Scatterplot per il 2014
        section_averages_1_2022_filtered = [value if value != 0 else None for value in section_averages_1_2022]
        section_averages_2_2022_filtered = [value if value != 0 else None for value in section_averages_2_2022]
        section_averages_3_2022_filtered = [value if value != 0 else None for value in section_averages_3_2022]

        if section_averages_1_2022_filtered:
            plt.scatter(range(len(section_averages_1_2022_filtered)), section_averages_1_2022_filtered,
                        color='orange', marker='*', label='Section 1 (2022)')

        if section_averages_2_2022_filtered:
            plt.scatter(range(len(section_averages_2_2022_filtered)), section_averages_2_2022_filtered,
                        color='green', marker='*', label='Section 2 (2022)')

        if section_averages_3_2022_filtered:
            plt.scatter(range(len(section_averages_3_2022_filtered)), section_averages_3_2022_filtered,
                        color='blue', marker='*', label='Section 3 (2022)')

        # Etichette degli assi x
        x_labels = common_drivers3
        plt.xlabel('Drivers')
        plt.ylabel('Time (s)')
        plt.title(f'Average section time {gp}')
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.xticks(range(len(x_labels)), x_labels, rotation=90)
        plt.tight_layout()
        plt.show()

# Codice per scuderie
#------------------------2013-2014-------------------------------
def rearrange_sections(averages):
    averages_car_2014 = {}
    for gp, gp_data in averages.items():
        averages_car_2014[gp] = {}
        for driver, sections in gp_data.items():
            averages_car_2014[gp][driver] = {
                "section_1": sections[0],
                "section_2": sections[1],
                "section_3": sections[2]
            }
    return averages_car_2014

# Chiamata della funzione per ottenere il nuovo dizionario con i valori riorganizzati
averages_car_2014 = rearrange_sections(averages_2014)
averages_car_2013 = rearrange_sections(averages_2013)
# Stampa del nuovo dizionario


for gp, gp_data in averages_car_2013.items():
    for driver, driver_data in gp_data.items():
        driver_data["car"] = car.get(driver)

for gp, gp_data in averages_car_2014.items():
    for driver, driver_data in gp_data.items():
        driver_data["car"] = car1.get(driver)



# Create a dictionary to store the cumulative values for each car and section
car_section_totals = {}
car_section_counts = {}

# Iterate through the race data
for race, race_data in averages_car_2013.items():
    for driver, driver_data in race_data.items():
        car = driver_data['car']
        for section in ['section_1', 'section_2', 'section_3']:
            # Check if the car key exists in the dictionary, if not, add it
            if car not in car_section_totals:
                car_section_totals[car] = {section: driver_data[section]}
                car_section_counts[car] = {section: 1}
            else:
                # If the car key exists, update the cumulative values
                car_section_totals[car][section] = car_section_totals[car].get(section, 0) + driver_data[section]
                car_section_counts[car][section] = car_section_counts[car].get(section, 0) + 1

# Calculate the average for each car and section
car_section_averages = {}
for car, section_totals in car_section_totals.items():
    car_section_averages[car] = {
        section: section_totals[section] / car_section_counts[car][section]
        for section in ['section_1', 'section_2', 'section_3']
    }

car_section_totals1 = {}
car_section_counts1 = {}

# Iterate through the race data
for race, race_data in averages_car_2014.items():
    for driver, driver_data in race_data.items():
        car = driver_data['car']
        for section in ['section_1', 'section_2', 'section_3']:
            # Check if the car key exists in the dictionary, if not, add it
            if car not in car_section_totals1:
                car_section_totals1[car] = {section: driver_data[section]}
                car_section_counts1[car] = {section: 1}
            else:
                # If the car key exists, update the cumulative values
                car_section_totals1[car][section] = car_section_totals1[car].get(section, 0) + driver_data[section]
                car_section_counts1[car][section] = car_section_counts1[car].get(section, 0) + 1

# Calculate the average for each car and section
car_section_averages1 = {}
for car, section_totals in car_section_totals1.items():
    car_section_averages1[car] = {
        section: section_totals[section] / car_section_counts1[car][section]
        for section in ['section_1', 'section_2', 'section_3']
    }


print(car_section_averages)
print(car_section_averages1)


# Estrai le macchine che sono presenti in entrambi i dizionari
common_cars = list(set(car_section_averages.keys()).intersection(car_section_averages1.keys()))

# Prepara i dati per lo scatter plot
x = common_cars
y1_section1 = [car_section_averages[car]['section_1'] for car in common_cars]
y1_section2 = [car_section_averages[car]['section_2'] for car in common_cars]
y1_section3 = [car_section_averages[car]['section_3'] for car in common_cars]

y2_section1 = [car_section_averages1[car]['section_1'] for car in common_cars]
y2_section2 = [car_section_averages1[car]['section_2'] for car in common_cars]
y2_section3 = [car_section_averages1[car]['section_3'] for car in common_cars]

# Crea lo scatter plot
plt.figure(figsize=(12, 6))

plt.scatter(x, y1_section1, label='Section 1 - 2013', marker='^', color='orange')
plt.scatter(x, y1_section2, label='Section 2 - 2013', marker='^', color='green')
plt.scatter(x, y1_section3, label='Section 3 - 2013', marker='^', color='blue')

plt.scatter(x, y2_section1, label='Section 1 - 2014', marker='*', color='orange')
plt.scatter(x, y2_section2, label='Section 2 - 2014', marker='*', color='green')
plt.scatter(x, y2_section3, label='Section 3 - 2014', marker='*', color='blue')

plt.xlabel('Team')
plt.ylabel('Time (s)')
plt.title('Section times for Teams (2013 vs. 2014)')
plt.xticks(rotation=45)
plt.legend()


plt.tight_layout()
plt.show()

#------------------------2021-2022-------------------------------
def rearrange_sections(averages):
    averages_car_2022 = {}
    for gp, gp_data in averages.items():
        averages_car_2022[gp] = {}
        for driver, sections in gp_data.items():
            averages_car_2022[gp][driver] = {
                "section_1": sections[0],
                "section_2": sections[1],
                "section_3": sections[2]
            }
    return averages_car_2022

# Chiamata della funzione per ottenere il nuovo dizionario con i valori riorganizzati
averages_car_2022 = rearrange_sections(averages_2022)
averages_car_2021 = rearrange_sections(averages_2021)
# Stampa del nuovo dizionario


for gp, gp_data in averages_car_2021.items():
    for driver, driver_data in gp_data.items():
        driver_data["car"] = car2.get(driver)

for gp, gp_data in averages_car_2022.items():
    for driver, driver_data in gp_data.items():
        driver_data["car"] = car3.get(driver)



# Create a dictionary to store the cumulative values for each car and section
car_section_totals = {}
car_section_counts = {}

# Iterate through the race data
for race, race_data in averages_car_2021.items():
    for driver, driver_data in race_data.items():
        car = driver_data['car']
        for section in ['section_1', 'section_2', 'section_3']:
            # Check if the car key exists in the dictionary, if not, add it
            if car not in car_section_totals:
                car_section_totals[car] = {section: driver_data[section]}
                car_section_counts[car] = {section: 1}
            else:
                # If the car key exists, update the cumulative values
                car_section_totals[car][section] = car_section_totals[car].get(section, 0) + driver_data[section]
                car_section_counts[car][section] = car_section_counts[car].get(section, 0) + 1

# Calculate the average for each car and section
car_section_averages = {}
for car, section_totals in car_section_totals.items():
    car_section_averages[car] = {
        section: section_totals[section] / car_section_counts[car][section]
        for section in ['section_1', 'section_2', 'section_3']
    }

car_section_totals1 = {}
car_section_counts1 = {}

# Iterate through the race data
for race, race_data in averages_car_2022.items():
    for driver, driver_data in race_data.items():
        car = driver_data['car']
        for section in ['section_1', 'section_2', 'section_3']:
            # Check if the car key exists in the dictionary, if not, add it
            if car not in car_section_totals1:
                car_section_totals1[car] = {section: driver_data[section]}
                car_section_counts1[car] = {section: 1}
            else:
                # If the car key exists, update the cumulative values
                car_section_totals1[car][section] = car_section_totals1[car].get(section, 0) + driver_data[section]
                car_section_counts1[car][section] = car_section_counts1[car].get(section, 0) + 1

# Calculate the average for each car and section
car_section_averages1 = {}
for car, section_totals in car_section_totals1.items():
    car_section_averages1[car] = {
        section: section_totals[section] / car_section_counts1[car][section]
        for section in ['section_1', 'section_2', 'section_3']
    }


print(car_section_averages)
print(car_section_averages1)


# Estrai le macchine che sono presenti in entrambi i dizionari
common_cars = list(set(car_section_averages.keys()).intersection(car_section_averages1.keys()))

# Prepara i dati per lo scatter plot
x = common_cars
y1_section1 = [car_section_averages[car]['section_1'] for car in common_cars]
y1_section2 = [car_section_averages[car]['section_2'] for car in common_cars]
y1_section3 = [car_section_averages[car]['section_3'] for car in common_cars]

y2_section1 = [car_section_averages1[car]['section_1'] for car in common_cars]
y2_section2 = [car_section_averages1[car]['section_2'] for car in common_cars]
y2_section3 = [car_section_averages1[car]['section_3'] for car in common_cars]

# Crea lo scatter plot
plt.figure(figsize=(12, 6))

plt.scatter(x, y1_section1, label='Section 1 - 2021', marker='^', color='orange')
plt.scatter(x, y1_section2, label='Section 2 - 2021', marker='^', color='green')
plt.scatter(x, y1_section3, label='Section 3 - 2021', marker='^', color='blue')

plt.scatter(x, y2_section1, label='Section 1 - 2022', marker='*', color='orange')
plt.scatter(x, y2_section2, label='Section 2 - 2022', marker='*', color='green')
plt.scatter(x, y2_section3, label='Section 3 - 2022', marker='*', color='blue')

plt.xlabel('Teams')
plt.ylabel('Time (s)')
plt.title('Section times for Teams (2021 vs. 2022)')
plt.xticks(rotation=45)
plt.legend()


plt.tight_layout()
plt.show() 