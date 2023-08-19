
import json
import pandas as pd

# Elenco dei nomi dei file JSON con la parte dell'anno variabile
anni = ['2013', '2014', '2021', '2022']



for anno in anni:
    wq_dict = {}
    # Costruisci il percorso del file JSON
    percorso_file = f"../Data Acquisition/Final_Data/FinalDataset{anno}.json"

    # Load the content of the JSON file
    with open(percorso_file, 'r') as file1:
        data1 = json.load(file1)

    for driver, driver_data in data1.items():
        for gp, gp_data in driver_data.items():
            if "Qualifying" in gp_data:
                if gp_data["Qualifying"]["Weather Condition"] and (gp_data["Qualifying"]["Weather Condition"] == "rain" or gp_data["Qualifying"]["Weather Condition"] == "sun"):
                    if gp not in wq_dict:
                        wq_dict[gp] = {"number of wq": 1, "number of wr": 0}
                    else:
                        wq_dict[gp]["number of wq"] += 1
            if "Laps" in gp_data:
                if gp_data["Laps"]["Weather Condition"] and (gp_data["Laps"]["Weather Condition"] == "rain" or gp_data["Laps"]["Weather Condition"] == "sun"):
                    if gp not in wq_dict:
                        wq_dict[gp] = {"number of wq": wq_dict[gp]["number of wq"], "number of wr": 1}
                    else:
                        wq_dict[gp]["number of wr"] += 1


    print(f'\n{anno} \n')

    df = pd.DataFrame(wq_dict).transpose()
    print(df)