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

# Esegui la query per trovare tutti i documenti che hanno la struttura desiderata
query = {}
cursor = collection.find(query)
cursor1 = collection1.find(query)
cursor2 = collection2.find(query)
cursor3 = collection3.find(query)

circuit_lenght = {}
circuit_turns = {}
speed = {}
car = {}
for document in cursor:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    #if "Qualifying" in gp_data:
                        #if gp_data.get("Qualifying").get("Weather Condition") == "sun":
                            if isinstance(gp_data, dict):
                                circuit = gp_data.get("Circuit")
                                if circuit:

                                    for i, j in circuit.items():
                                        if i == "Length":
                                            if gp not in circuit_lenght.keys():
                                                circuit_lenght[gp] = j
                                        if i == "Turns":
                                            if gp not in circuit_turns.keys():
                                                circuit_turns[gp] = j
                                    # Get the max_speed for each driver and GP
                                max_speed = gp_data.get("km/h")
                                if max_speed:
                                    if driver not in speed:
                                        speed[driver] = {}
                                    speed[driver][gp] = max_speed
                car[driver] = driver_data.get("Car")


circuit_lenght1 = {}
circuit_turns1 = {}
speed1 = {}
car1 = {}
for document in cursor1:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if "Qualifying" in gp_data:
                        if gp_data.get("Qualifying").get("Weather Condition") == "sun":
                            if isinstance(gp_data, dict):
                                circuit = gp_data.get("Circuit")
                                if circuit:

                                    for i, j in circuit.items():
                                        if i == "Length":
                                            if gp not in circuit_lenght1.keys():
                                                circuit_lenght1[gp] = j
                                        if i == "Turns":
                                            if gp not in circuit_turns1.keys():
                                                circuit_turns1[gp] = j
                                    # Get the max_speed for each driver and GP
                                max_speed = gp_data.get("km/h")
                                if max_speed:
                                    if driver not in speed1:
                                        speed1[driver] = {}
                                    speed1[driver][gp] = max_speed
                car1[driver] = driver_data.get("Car")



circuit_lenght2 = {}
circuit_turns2 = {}
speed2 = {}
car2 = {}
for document in cursor2:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if "Qualifying" in gp_data:
                        if gp_data.get("Qualifying").get("Weather Condition") == "sun":
                            if isinstance(gp_data, dict):
                                circuit = gp_data.get("Circuit")
                                if circuit:

                                    for i, j in circuit.items():
                                        if i == "Length":
                                            if gp not in circuit_lenght2.keys():
                                                circuit_lenght2[gp] = j
                                        if i == "Turns":
                                            if gp not in circuit_turns2.keys():
                                                circuit_turns2[gp] = j
                                    # Get the max_speed for each driver and GP
                                max_speed = gp_data.get("km/h")
                                if max_speed:
                                    if driver not in speed2:
                                        speed2[driver] = {}
                                    speed2[driver][gp] = float(max_speed)
                car2[driver] = driver_data.get("Car")

circuit_lenght3 = {}
circuit_turns3 = {}
speed3 = {}
car3 = {}
for document in cursor3:
    for driver, driver_data in document.items():
        if driver != "_id":
            if isinstance(driver_data, dict):
                for gp, gp_data in driver_data.items():
                    if "Qualifying" in gp_data:
                        if gp_data.get("Qualifying").get("Weather Condition") == "sun":
                            if isinstance(gp_data, dict):
                                circuit = gp_data.get("Circuit")
                                if circuit:

                                    for i, j in circuit.items():
                                        if i == "Length":
                                            if gp not in circuit_lenght3.keys():
                                                circuit_lenght3[gp] = j
                                        if i == "Turns":
                                            if gp not in circuit_turns3.keys():
                                                circuit_turns3[gp] = j
                                    # Get the max_speed for each driver and GP
                                max_speed = gp_data.get("km/h")
                                if max_speed:
                                    if driver not in speed3:
                                        speed3[driver] = {}
                                    speed3[driver][gp] = float(max_speed)
                car3[driver] = driver_data.get("Car")

# Create a new dictionary to store the drivers' speeds for each GP


gp_drivers_speeds = {}

# Iterate through the 'speed' dictionary
for driver, gp_speeds in speed.items():
    for gp, driver_speed in gp_speeds.items():
        if gp not in gp_drivers_speeds:
            gp_drivers_speeds[gp] = {}
        gp_drivers_speeds[gp][driver] = driver_speed

# Display the result


# Create a new dictionary to store the drivers' speeds for each GP
gp_drivers_speeds1 = {}

# Iterate through the 'speed' dictionary
for driver, gp_speeds in speed1.items():
    for gp, driver_speed in gp_speeds.items():
        if gp not in gp_drivers_speeds1:
            gp_drivers_speeds1[gp] = {}
        gp_drivers_speeds1[gp][driver] = driver_speed

# Display the result
gp_drivers_speeds2 = {}

# Iterate through the 'speed' dictionary
for driver, gp_speeds in speed2.items():
    for gp, driver_speed in gp_speeds.items():
        if gp not in gp_drivers_speeds2:
            gp_drivers_speeds2[gp] = {}
        gp_drivers_speeds2[gp][driver] = driver_speed

gp_drivers_speeds3 = {}

# Iterate through the 'speed' dictionary
for driver, gp_speeds in speed3.items():
    for gp, driver_speed in gp_speeds.items():
        if gp not in gp_drivers_speeds3:
            gp_drivers_speeds3[gp] = {}
        gp_drivers_speeds3[gp][driver] = driver_speed



# Assuming you have already retrieved the circuit lengths and turns in the circuit_lenght and circuit_turns dictionaries

# Create a list of tuples to store the data for the scatter plot, maintaining associations
data_points = []

# Iterate through the circuit lengths and turns dictionaries
for gp in circuit_lenght:
    if gp in circuit_lenght1:
        if gp in circuit_turns:
            data_points.append((circuit_lenght[gp], circuit_turns[gp], gp))

# Convert the data_points list to a numpy array for sorting
data_points = np.array(data_points, dtype=[('Length', float), ('Turns', int), ('GP', object)])

# Sort the data_points array based on both x (Length) and y (Turns) axes
sorted_indices = np.lexsort((data_points['Turns'], data_points['Length']))

# Extract sorted x_values, y_values, and labels based on the sorted indices
x_values_sorted = data_points['Length'][sorted_indices]
y_values_sorted = data_points['Turns'][sorted_indices]
labels_sorted = data_points['GP'][sorted_indices]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values_sorted, y_values_sorted, s=80, alpha=0.7)
plt.xlabel("Length of GP circuit (km)")
plt.ylabel("Number of turns")
plt.title("GP circuit length vs number of turns (2013-2014)")


# Add labels for each point (GP name)
for x, y, label in zip(x_values_sorted, y_values_sorted, labels_sorted):
    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')

plt.show()

# Create a list of tuples to store the data for the scatter plot, maintaining associations
data_points1 = []

# Iterate through the circuit lengths and turns dictionaries
for gp in circuit_lenght2:
    if gp in circuit_lenght3:
        if gp in circuit_turns2:
            data_points1.append((circuit_lenght2[gp], circuit_turns2[gp], gp))

# Convert the data_points list to a numpy array for sorting
data_points1 = np.array(data_points1, dtype=[('Length', float), ('Turns', int), ('GP', object)])

# Sort the data_points array based on both x (Length) and y (Turns) axes
sorted_indices = np.lexsort((data_points1['Turns'], data_points1['Length']))

# Extract sorted x_values, y_values, and labels based on the sorted indices
x_values_sorted = data_points1['Length'][sorted_indices]
y_values_sorted = data_points1['Turns'][sorted_indices]
labels_sorted = data_points1['GP'][sorted_indices]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values_sorted, y_values_sorted, s=80, alpha=0.7)
plt.xlabel("Length of GP circuit (km)")
plt.ylabel("Number of turns")
plt.title("GP circuit length vs number of turns (2021-2022)")


# Add labels for each point (GP name)
for x, y, label in zip(x_values_sorted, y_values_sorted, labels_sorted):
    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')

plt.show()

# Trova i piloti comuni nei due anni per ogni GP

# Trova i piloti comuni nei due anni per ogni GP
common_gp = list(set(gp_drivers_speeds.keys()).intersection(set(gp_drivers_speeds1.keys())))
common_pilots_by_gp = {}
for gp in common_gp:
    common_pilots_by_gp[gp] = list(set(gp_drivers_speeds[gp].keys()) & set(gp_drivers_speeds1[gp].keys()))

# Genera un grafico scatter per ogni GP con i piloti comuni
for gp in common_pilots_by_gp.keys():
    common_pilots = common_pilots_by_gp[gp]
    x_values = list(range(len(common_pilots)))  # Coordinate x dei piloti (numerici)
    common_pilots_speed_2013 = [gp_drivers_speeds[gp][pilot] for pilot in common_pilots]
    common_pilots_speed_2014 = [gp_drivers_speeds1[gp][pilot] for pilot in common_pilots]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, common_pilots_speed_2013, color='blue', label='2013')
    plt.scatter(x_values, common_pilots_speed_2014, color='red', label='2014')
    plt.xticks(x_values, common_pilots, rotation=45)
    plt.xlabel('Drivers')
    plt.ylabel('Speed (km/h)')
    plt.title(f'Maximum speed {gp}')
    plt.legend()

    plt.tight_layout()
    for i in range(len(x_values)):
        plt.plot([x_values[i], x_values[i]], [common_pilots_speed_2013[i], common_pilots_speed_2014[i]], color='gray', linestyle='dotted')

    # Mostra il grafico per il GP corrente
    plt.show()



# Trova i piloti comuni nei due anni per ogni GP
common_gp1 = list(set(gp_drivers_speeds2.keys()).intersection(set(gp_drivers_speeds3.keys())))
common_pilots_by_gp1 = {}
print(common_gp1)

for gp in common_gp1:
    common_pilots_by_gp1[gp] = list(set(gp_drivers_speeds2[gp].keys()) & set(gp_drivers_speeds3[gp].keys()))

# Genera un grafico scatter per ogni GP con i piloti comuni
for gp in common_pilots_by_gp1.keys():
    common_pilots = common_pilots_by_gp1[gp]
    x_values = list(range(len(common_pilots)))  # Coordinate x dei piloti (numerici)
    common_pilots_speed_2021 = [gp_drivers_speeds2[gp][pilot] for pilot in common_pilots]
    common_pilots_speed_2022 = [gp_drivers_speeds3[gp][pilot] for pilot in common_pilots]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, common_pilots_speed_2021, color='blue', label='2021')
    plt.scatter(x_values, common_pilots_speed_2022, color='red', label='2022')
    plt.xticks(x_values, common_pilots, rotation=45)
    plt.xlabel('Drivers')
    plt.ylabel('Speed (km/h)')
    plt.title(f'Maximum speed {gp}')
    plt.legend()

    plt.tight_layout()
    for i in range(len(x_values)):
        plt.plot([x_values[i], x_values[i]], [common_pilots_speed_2021[i], common_pilots_speed_2022[i]], color='gray', linestyle='dotted')

    # Mostra il grafico per il GP corrente
    plt.show()


for driver, tempi in speed.items():
    if driver in car:
        tempi['car'] = car[driver]


for driver, tempi in speed1.items():
    if driver in car1:
        tempi['car'] = car1[driver]

for driver, tempi in speed2.items():
    if driver in car2:
        tempi['car'] = car2[driver]

for driver, tempi in speed3.items():
    if driver in car3:
        tempi['car'] = car3[driver]


from collections import defaultdict

# Dizionario con le macchine come chiavi e una lista delle velocità dei piloti con quella macchina
velocita_per_macchina = defaultdict(list)

# Iteriamo attraverso il dizionario dei tempi dei piloti
for pilota, tempi in speed.items():
    car_pilota = tempi.get('car')
    if car_pilota:
        # Aggiungiamo le velocità dei piloti alla lista corrispondente alla macchina
        velocita_pilota = [tempo for gp, tempo in tempi.items() if gp != 'car']
        velocita_per_macchina[car_pilota].extend(velocita_pilota)

# Dizionario con le macchine come chiavi e la media delle velocità di tutti i piloti con quella macchina come valore
media_velocita_per_macchina = {}

for macchina, velocita_piloti in velocita_per_macchina.items():
    # Calcoliamo la media delle velocità per la macchina
    media_velocita_macchina = sum(velocita_piloti) / len(velocita_piloti)
    media_velocita_per_macchina[macchina] = media_velocita_macchina

# Dizionario con le macchine come chiavi e una lista delle velocità dei piloti con quella macchina
velocita_per_macchina1 = defaultdict(list)

# Iteriamo attraverso il dizionario dei tempi dei piloti
for pilota, tempi in speed1.items():
    car_pilota = tempi.get('car')
    if car_pilota:
        # Aggiungiamo le velocità dei piloti alla lista corrispondente alla macchina
        velocita_pilota = [tempo for gp, tempo in tempi.items() if gp != 'car']
        velocita_per_macchina1[car_pilota].extend(velocita_pilota)

# Dizionario con le macchine come chiavi e la media delle velocità di tutti i piloti con quella macchina come valore
media_velocita_per_macchina1 = {}

for macchina, velocita_piloti in velocita_per_macchina1.items():
    # Calcoliamo la media delle velocità per la macchina
    media_velocita_macchina = sum(velocita_piloti) / len(velocita_piloti)
    media_velocita_per_macchina1[macchina] = media_velocita_macchina




# Lista delle macchine comuni ad entrambi i dizionari
macchine_comuni = list(set(media_velocita_per_macchina.keys()) & set(media_velocita_per_macchina1.keys()))

# Estraiamo i valori di velocità media massima delle macchine comuni
velocita_media_max_dizionario1 = [media_velocita_per_macchina[macchina] for macchina in macchine_comuni]
velocita_media_max_dizionario2 = [media_velocita_per_macchina1[macchina] for macchina in macchine_comuni]

# Creiamo lo scatterplot
plt.scatter(macchine_comuni, velocita_media_max_dizionario1, label='2013', color='blue')
plt.scatter(macchine_comuni, velocita_media_max_dizionario2, label='2014', color='red')

# Aggiungiamo le etichette degli assi e il titolo del grafico
plt.xlabel('Teams')
plt.ylabel('Speed (km/h)')
plt.title('Average maximum speed per Teams (2013 vs 2014)')
plt.xticks(rotation=45)

# Aggiungiamo la legenda
plt.legend()

# Mostrare lo scatterplot
plt.tight_layout()
for i in range(len(macchine_comuni)):
    plt.plot([macchine_comuni[i], macchine_comuni[i]], [velocita_media_max_dizionario1[i], velocita_media_max_dizionario2[i]], color='gray',
             linestyle='dotted')

plt.show()

# Dizionario con le macchine come chiavi e una lista delle velocità dei piloti con quella macchina
velocita_per_macchina2 = defaultdict(list)

# Iteriamo attraverso il dizionario dei tempi dei piloti
for pilota, tempi in speed2.items():
    car_pilota = tempi.get('car')
    if car_pilota:
        # Aggiungiamo le velocità dei piloti alla lista corrispondente alla macchina
        velocita_pilota = [tempo for gp, tempo in tempi.items() if gp != 'car']
        velocita_per_macchina2[car_pilota].extend(velocita_pilota)

# Dizionario con le macchine come chiavi e la media delle velocità di tutti i piloti con quella macchina come valore
media_velocita_per_macchina2 = {}

for macchina, velocita_piloti in velocita_per_macchina2.items():
    # Calcoliamo la media delle velocità per la macchina
    media_velocita_macchina = sum(velocita_piloti) / len(velocita_piloti)
    media_velocita_per_macchina2[macchina] = media_velocita_macchina

# Dizionario con le macchine come chiavi e una lista delle velocità dei piloti con quella macchina
velocita_per_macchina3 = defaultdict(list)

# Iteriamo attraverso il dizionario dei tempi dei piloti
for pilota, tempi in speed3.items():
    car_pilota = tempi.get('car')
    if car_pilota:
        # Aggiungiamo le velocità dei piloti alla lista corrispondente alla macchina
        velocita_pilota = [tempo for gp, tempo in tempi.items() if gp != 'car']
        velocita_per_macchina3[car_pilota].extend(velocita_pilota)

# Dizionario con le macchine come chiavi e la media delle velocità di tutti i piloti con quella macchina come valore
media_velocita_per_macchina3 = {}

for macchina, velocita_piloti in velocita_per_macchina3.items():
    # Calcoliamo la media delle velocità per la macchina
    media_velocita_macchina = sum(velocita_piloti) / len(velocita_piloti)
    media_velocita_per_macchina3[macchina] = media_velocita_macchina




# Lista delle macchine comuni ad entrambi i dizionari
macchine_comuni = list(set(media_velocita_per_macchina2.keys()) & set(media_velocita_per_macchina3.keys()))

# Estraiamo i valori di velocità media massima delle macchine comuni
velocita_media_max_dizionario1 = [media_velocita_per_macchina2[macchina] for macchina in macchine_comuni]
velocita_media_max_dizionario2 = [media_velocita_per_macchina3[macchina] for macchina in macchine_comuni]

# Creiamo lo scatterplot
plt.scatter(macchine_comuni, velocita_media_max_dizionario1, label='2021', color='blue')
plt.scatter(macchine_comuni, velocita_media_max_dizionario2, label='2022', color='red')

# Aggiungiamo le etichette degli assi e il titolo del grafico
plt.xlabel('Teams')
plt.ylabel('Speed (km/h)')
plt.title('Average maximum speed per Teams (2021 vs 2022)')
plt.xticks(rotation=45)

# Aggiungiamo la legenda
plt.legend()

# Mostrare lo scatterplot
plt.tight_layout()
for i in range(len(macchine_comuni)):
    plt.plot([macchine_comuni[i], macchine_comuni[i]], [velocita_media_max_dizionario1[i], velocita_media_max_dizionario2[i]], color='gray',
             linestyle='dotted')
plt.show()