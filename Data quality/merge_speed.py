import json
import pandas as pd

# Elenco dei nomi dei file JSON con la parte dell'anno variabile
anni = ['2013', '2014', '2021', '2022']



for anno in anni:
    speed_dict = {}
    # Costruisci il percorso del file JSON
    percorso_file = f"../Data Acquisition/Merged_Data/Qualifying_Season_Merged_{anno}.json"

    # Load the content of the JSON file
    with open(percorso_file, 'r') as file1:
        data1 = json.load(file1)

    for driver, driver_data in data1.items():
        for gp, gp_data in driver_data.items():
            if "km/h" in gp_data:
                if gp_data["km/h"]:
                    if gp not in speed_dict:
                        speed_dict[gp] = {"number of speed data": 1}
                    else:
                        speed_dict[gp]["number of speed data"] += 1

    print(f'\n{anno} \n')

    df = pd.DataFrame(speed_dict).transpose()
    print(df)