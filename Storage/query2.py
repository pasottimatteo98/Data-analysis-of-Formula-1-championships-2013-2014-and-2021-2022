import pymongo
import matplotlib.pyplot as plt
import numpy as np

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


def convert_to_seconds(time_str):
    if time_str is None:
        return None

    minutes, seconds = time_str.split(':')
    total_seconds = int(minutes) * 60 + float(seconds)
    return total_seconds

# Esegui la query per trovare tutti i documenti che hanno la struttura desiderata
query = {}
cursor = collection.find(query)
cursor1 = collection1.find(query)
# Dizionario per memorizzare i dati dei laps per ogni pilota e GP
#laps_data = {}

# Cicla sui Gran Premi (GP)
#for document in cursor:
#    for driver, driver_data in document.items():
#        if driver != "_id":
#            if isinstance(driver_data, dict):
#                for gp, gp_data in driver_data.items():
#                    if gp != "Circuit" and isinstance(gp_data, dict):
#                        laps = gp_data.get("Laps")
#                        if laps:
#                            driver_laps = []
#                            for lap_num, lap_time in laps.items():
#                                if lap_num == "Weather Condition":
#                                    continue
#                                if lap_time == "sun":
#                                    continue
#                                lap_time_sec = convert_to_seconds(lap_time)
#                                driver_laps.append(lap_time_sec)
#                            
#                            if driver not in laps_data:
#                                laps_data[driver] = {}
#                            laps_data[driver][gp] = driver_laps

# Genera i boxplot per ogni pilota in ogni Gran Premio
#for driver, driver_data in laps_data.items():
#    for gp, laps in driver_data.items():
#        plt.figure()
#        plt.boxplot(laps)
#        plt.title(f"Laps per il pilota {driver} nel Gran Premio {gp}")
#        plt.xlabel("Laps")
#        plt.ylabel("Tempo (secondi)")
#        plt.show()

# Dizionario per memorizzare i dati dei laps per ogni pilota e GP
#laps_data1 = {}

# Cicla sui Gran Premi (GP)
#for document in cursor1:
#    for driver, driver_data in document.items():
#        if driver != "_id":
#            if isinstance(driver_data, dict):
#                for gp, gp_data in driver_data.items():
#                    if gp != "Circuit" and isinstance(gp_data, dict):
#                        laps = gp_data.get("Laps")
#                        if laps:
#                            driver_laps = []
#                            for lap_num, lap_time in laps.items():
#                                if lap_num == "Weather Condition":
#                                    continue
#                                if lap_time == "sun":
#                                    continue
#                                lap_time_sec = convert_to_seconds(lap_time)
#                                driver_laps.append(lap_time_sec)
#                            
#                            if driver not in laps_data:
#                                laps_data[driver] = {}
#                            laps_data[driver][gp] = driver_laps

# Genera i boxplot per ogni pilota in ogni Gran Premio
#for driver, driver_data in laps_data1.items():
#    for gp, laps in driver_data.items():
#        plt.figure()
#        plt.boxplot(laps)
#        plt.title(f"Laps per il pilota {driver} nel Gran Premio {gp}")
#        plt.xlabel("Laps")
#        plt.ylabel("Tempo (secondi)")
#        plt.show()

# Dizionari per memorizzare i dati dei tempi medi delle sezioni per ogni pilota e GP
averages_2013 = {}
averages_2014 = {}

# Cicla sui Gran Premi (GP)

for document in cursor:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get(
                            "Laps")  # Usa il metodo get per gestire il caso in cui "Laps" non sia presente
                        if laps and laps.get("Weather Condition") == "sun":
                            max_laps_driver = max([k for k in laps.keys() if k != "Weather Condition"], key=lambda x: int(x))
                            num_times_per_section = int(max_laps_driver) // 3
                            num_times_per_section3 = int(max_laps_driver) - 2 * int(num_times_per_section)
                            section_1 = []
                            section_2 = []
                            section_3 = []
                            #section_averages = []

                            for lap_num, lap_time in laps.items():
                                if lap_num == "Weather Condition":
                                    continue
                                lap_time_sec = convert_to_seconds(lap_time)
                                if int(lap_num) in range(1, int(num_times_per_section) + 1):
                                    section_1.append(lap_time_sec)
                                elif int(lap_num) in range(int(num_times_per_section) + 1, 2 * int(num_times_per_section) + 1):
                                    section_2.append(lap_time_sec)
                                elif int(lap_num) in range(2 * int(num_times_per_section) + 1, int(max_laps_driver) + 1):
                                    section_3.append(lap_time_sec)
                            section_averages_1_2013 = sum(section_1) / len(section_1) if section_1 else 0.0
                            section_averages_2_2013 = sum(section_2) / len(section_2) if section_2 else 0.0
                            section_averages_3_2013 = sum(section_3) / len(section_3) if section_3 else 0.0
                            # Memorizza i tempi medi delle sezioni per ogni pilota e GP nel dizionario
                            if gp not in averages_2013:
                                averages_2013[gp] = {}
                            averages_2013[gp][driver] = [section_averages_1_2013, section_averages_2_2013,
                                                             section_averages_3_2013]

                            print("Gran Premio:", gp)
                            print("Pilota con il maggior numero di laps percorsi:", max_laps_driver)
                            print("Numero di tempi per sezione 1:", num_times_per_section)
                            print("Numero di tempi per sezione 2:", num_times_per_section)
                            print("Numero di tempi per sezione 3:", num_times_per_section3)
                            print(f"Pilota: {driver}, Sezione 1: {section_averages_1_2013} secondi")
                            print(f"Pilota: {driver}, Sezione 2: {section_averages_2_2013} secondi")
                            print(f"Pilota: {driver}, Sezione 3: {section_averages_3_2013} secondi")
                            print()


# Cicla sui Gran Premi (GP)
for document in cursor1:  # Utilizza cursor1 per il 2014
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if gp != "Circuit" and isinstance(gp_data, dict):
                        laps = gp_data.get(
                            "Laps")  # Usa il metodo get per gestire il caso in cui "Laps" non sia presente
                        if laps and laps.get("Weather Condition") == "sun":
                            max_laps_driver = max([k for k in laps.keys() if k != "Weather Condition"], key=lambda x: int(x))
                            num_times_per_section = int(max_laps_driver) // 3
                            num_times_per_section3 = int(max_laps_driver) - 2 * int(num_times_per_section)
                            section_1 = []
                            section_2 = []
                            section_3 = []

                            for lap_num, lap_time in laps.items():
                                if lap_num == "Weather Condition":
                                    continue
                                lap_time_sec = convert_to_seconds(lap_time)
                                if int(lap_num) in range(1, int(num_times_per_section) + 1):
                                    section_1.append(lap_time_sec)
                                elif int(lap_num) in range(int(num_times_per_section) + 1, 2 * int(num_times_per_section) + 1):
                                    section_2.append(lap_time_sec)
                                elif int(lap_num) in range(2 * int(num_times_per_section) + 1, int(max_laps_driver) + 1):
                                    section_3.append(lap_time_sec)
                            section_averages_1_2014 = sum(section_1) / len(section_1) if section_1 else 0.0
                            section_averages_2_2014 = sum(section_2) / len(section_2) if section_2 else 0.0
                            section_averages_3_2014 = sum(section_3) / len(section_3) if section_3 else 0.0
                            # Memorizza i tempi medi delle sezioni per ogni pilota e GP nel dizionario
                            if gp not in averages_2014:
                                averages_2014[gp] = {}
                            averages_2014[gp][driver] = [section_averages_1_2014, section_averages_2_2014,
                                                         section_averages_3_2014]

                            print("Gran Premio:", gp)
                            print("Pilota con il maggior numero di laps percorsi:", max_laps_driver)
                            print("Numero di tempi per sezione 1:", num_times_per_section)
                            print("Numero di tempi per sezione 2:", num_times_per_section)
                            print("Numero di tempi per sezione 3:", num_times_per_section3)
                            print(f"Pilota: {driver}, Sezione 1: {section_averages_1_2014} secondi")
                            print(f"Pilota: {driver}, Sezione 2: {section_averages_2_2014} secondi")
                            print(f"Pilota: {driver}, Sezione 3: {section_averages_3_2014} secondi")
                            print()
# Chiudi la connessione
client.close()

print(averages_2013)
print(averages_2014)


common_drivers = []
drivers_2013 = []
drivers_2014 = []
for gp in averages_2013.keys():
    for driver in averages_2013[gp].keys():
        if driver not in drivers_2013:
            drivers_2013.append(driver)

for gp in averages_2014.keys():
    for driver in averages_2014[gp].keys():
        if driver not in drivers_2014:
            drivers_2014.append(driver)
#print(drivers_2013)
#print(drivers_2014)
for i in drivers_2013:
    if i in drivers_2014:
        common_drivers.append(i)

#print(common_drivers)


# Genera gli scatterplot per ogni GP
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
        section_averages_1_2013_filtered = [value for value in section_averages_1_2013 if value != 0]
        section_averages_2_2013_filtered = [value for value in section_averages_2_2013 if value != 0]
        section_averages_3_2013_filtered = [value for value in section_averages_3_2013 if value != 0]

        if section_averages_1_2013_filtered:
            plt.scatter(range(len(section_averages_1_2013_filtered)), section_averages_1_2013_filtered,
                        color='orange', marker='^', label='Sezione 1 (2013)')

        if section_averages_2_2013_filtered:
            plt.scatter(range(len(section_averages_2_2013_filtered)), section_averages_2_2013_filtered,
                        color='green', marker='^', label='Sezione 2 (2013)')

        if section_averages_3_2013_filtered:
            plt.scatter(range(len(section_averages_3_2013_filtered)), section_averages_3_2013_filtered,
                        color='blue', marker='^', label='Sezione 3 (2013)')

        # Scatterplot per il 2014
        section_averages_1_2014_filtered = [value for value in section_averages_1_2014 if value != 0]
        section_averages_2_2014_filtered = [value for value in section_averages_2_2014 if value != 0]
        section_averages_3_2014_filtered = [value for value in section_averages_3_2014 if value != 0]

        if section_averages_1_2014_filtered:
            plt.scatter(range(len(section_averages_1_2014_filtered)), section_averages_1_2014_filtered,
                        color='orange', marker='*', label='Sezione 1 (2014)')

        if section_averages_2_2014_filtered:
            plt.scatter(range(len(section_averages_2_2014_filtered)), section_averages_2_2014_filtered,
                        color='green', marker='*', label='Sezione 2 (2014)')

        if section_averages_3_2014_filtered:
            plt.scatter(range(len(section_averages_3_2014_filtered)), section_averages_3_2014_filtered,
                        color='blue', marker='*', label='Sezione 3 (2014)')


            # Etichette degli assi x
        x_labels = common_drivers2
        plt.xlabel('Piloti')
        plt.ylabel('Tempo medio sulle sezioni (secondi)')
        plt.title(f'Tempi medi sulle sezioni per il GP: {gp}')
        plt.legend()
        plt.xticks(range(len(x_labels)), x_labels, rotation=90)
        plt.tight_layout()
        plt.show()
