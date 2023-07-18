
import os
import json

# Ottenere il percorso assoluto completo del file Season2014.json
file1_path = os.path.abspath("/Users/martaprivitera/Documents/Università magistrale DataScience/Data Management/DataMan/DataManag/DataManagement/RawDataCollected/WebScraping/Season2014.json")

# Caricare il contenuto del primo file JSON
with open(file1_path, 'r') as file1:
    data1 = json.load(file1)
# Carica il contenuto del secondo file JSON
with open('WS_weather2014_qualifiche.json', 'r') as file2:
    data2 = json.load(file2)

# Itera attraverso il primo dizionario e aggiungi le informazioni sulle condizioni meteorologiche
for driver, races in data1.items():
    for race, details in races.items():
        if race in data2:
            if "Qualifying" in details:
                details["Qualifying"]["Weather Condition"] = data2[race]



# Salva il risultato del merge in un nuovo file JSON
with open('final2014.json', 'w') as outfile:
    json.dump(data1, outfile, indent=4)

print("Merge completato e salvato su final2014.json")