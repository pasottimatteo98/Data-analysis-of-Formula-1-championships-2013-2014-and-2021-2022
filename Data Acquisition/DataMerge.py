import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Path della cartella con i file JSON
folder_path = "Qualifying_Session_Max_Speed_2014/"

# Path del secondo file JSON
second_json_path = "../RawDataCollected/WebScraping/Season2014.json"

# Carica il secondo JSON
with open(second_json_path, "r") as f:
    second_json = json.load(f)
    print(second_json)

# Esplora i file nella cartella
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        # Apre il file JSON
        with open(os.path.join(folder_path, filename), "r") as f:
            first_json = json.load(f)

        # Unisce i due JSON
        for driver_data in first_json:
            driver = driver_data["driver"]
            gp = driver_data["gp"]

            # Cerca corrispondenze approssimative del nome del driver nel secondo JSON
            driver_matches = process.extract(driver, second_json.keys(), scorer=fuzz.token_sort_ratio, limit=3)
            for driver_match in driver_matches:
                if driver_match[1] >= 60:
                    matched_driver = driver_match[0]
                    # Cerca corrispondenze approssimative del nome del GP nel secondo JSON
                    gp_matches = process.extract(gp, second_json[matched_driver].keys(), scorer=fuzz.token_sort_ratio,
                                                 limit=3)
                    for gp_match in gp_matches:
                        if gp_match[1] >= 60:
                            matched_gp = gp_match[0]
                            # Inserisci i dati "km/h" nel punto specifico
                            second_json[matched_driver][matched_gp]["km/h"] = driver_data["km/h"]

    # Scrive il file unificato
year = str(driver_data["year"])
with open("Clean Data/Final_Data_Year_"+year+".json", "w") as f:
    json.dump(second_json, f, indent=4)
