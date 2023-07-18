#2013 MERGE GARA

import json

# Carica il contenuto del primo file JSON
with open('final2013.json', 'r') as file1:
    data1 = json.load(file1)

# Carica il contenuto del secondo file JSON
with open('WS_weather2013_race.json', 'r') as file2:
    data2 = json.load(file2)

# Itera attraverso il primo dizionario e aggiungi le informazioni sulle condizioni meteorologiche
for driver, races in data1.items():
    for race, details in races.items():
        if race in data2:
            if "Laps" in details:
                details["Laps"]["Weather Condition"] = data2[race]



# Salva il risultato del merge in un nuovo file JSON
with open('final2013.json', 'w') as outfile:
    json.dump(data1, outfile, indent=4)

print("Merge completato e salvato su final2013.json")