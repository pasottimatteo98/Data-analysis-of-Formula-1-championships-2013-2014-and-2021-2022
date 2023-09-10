import pymongo
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import iqr
from adjustText import adjust_text
import seaborn as sns

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

circuit_lenght1 = {}
circuit_turns1 = {}
speed1 = {}
car1 = {}
for document in cursor1:
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
                                    if gp not in circuit_lenght1.keys():
                                        circuit_lenght1[gp] = j
                                if i == "Turns":
                                    if gp not in circuit_turns1.keys():
                                        circuit_turns1[gp] = j

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
#plt.scatter(x_values_sorted, y_values_sorted, s=80, alpha=0.7)
sns.scatterplot(x=x_values_sorted, y=y_values_sorted, alpha=0.7)
plt.xlabel("Length of GP circuit (km)")
plt.ylabel("Number of turns")
plt.title("GP circuit length vs number of turns (2013-2014)")


# Add labels for each point (GP name)
#for x, y, label in zip(x_values_sorted, y_values_sorted, labels_sorted):
#    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')

text_objects = []
for x, y, label in zip(x_values_sorted, y_values_sorted, labels_sorted):
    text = plt.text(x, y, label, fontsize=8, ha='right', va='bottom', alpha=0.7)
    text_objects.append(text)

# Adjust label positions to avoid overlap using adjustText
adjust_text(text_objects, arrowprops=dict(arrowstyle='fancy, head_length=0.5, head_width=0.3', color='gray', lw=0.5))


plt.show()

circuit_lenght2 = {}
circuit_turns2 = {}
speed2 = {}
car2 = {}
for document in cursor2:
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
                                    if gp not in circuit_lenght2.keys():
                                        circuit_lenght2[gp] = j
                                if i == "Turns":
                                    if gp not in circuit_turns2.keys():
                                        circuit_turns2[gp] = j
                                    # Get the max_speed for each driver and GP


circuit_lenght3 = {}
circuit_turns3 = {}
speed3 = {}
car3 = {}
for document in cursor3:
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
                                    if gp not in circuit_lenght3.keys():
                                        circuit_lenght3[gp] = j
                                if i == "Turns":
                                    if gp not in circuit_turns3.keys():
                                        circuit_turns3[gp] = j

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
#plt.scatter(x_values_sorted, y_values_sorted, s=80, alpha=0.7)
sns.scatterplot(x=x_values_sorted, y=y_values_sorted, alpha=0.7)
plt.xlabel("Length of GP circuit (km)")
plt.ylabel("Number of turns")
plt.title("GP circuit length vs number of turns (2021-2022)")

# Add labels for each point (GP name)
#for x, y, label in zip(x_values_sorted, y_values_sorted, labels_sorted):
#    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')

# Add labels for each point (GP name) with manual avoidance of overlap
text_objects = []
for x, y, label in zip(x_values_sorted, y_values_sorted, labels_sorted):
    text = plt.text(x, y, label, fontsize=8, ha='right', va='bottom', alpha=0.7)
    text_objects.append(text)

# Adjust label positions to avoid overlap using adjustText
adjust_text(text_objects, arrowprops=dict(arrowstyle='fancy, head_length=0.5, head_width=0.3', color='white', lw=0.5))

plt.show()