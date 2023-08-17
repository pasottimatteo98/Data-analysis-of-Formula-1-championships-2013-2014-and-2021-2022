import os
import json
import pandas as pd

# Lista delle cartelle con gli anni desiderati
anni = ['2013', '2014', '2021', '2022']

dict_weather = {}

for anno in anni:
    # Costruisci il percorso del file JSON
    percorso_file = f"../RawDataCollected/WebScraping/Weather_Qualifying/{anno}/Weather_Qualifying.json"

    # Load the content of the JSON file
    with open(percorso_file, 'r') as file1:
        data1 = json.load(file1)
        dict_weather[anno] = {"GP": len(data1), "V": len(data1.values())}

df_weather = pd.DataFrame(dict_weather).transpose()
print(f'WEATHER QUALIFYING\n')
print(df_weather)

dict_weather = {}

for anno in anni:
    # Costruisci il percorso del file JSON
    percorso_file = f"../RawDataCollected/WebScraping/Weather_Race/{anno}/Weather_Race.json"

    # Load the content of the JSON file
    with open(percorso_file, 'r') as file1:
        data1 = json.load(file1)
        dict_weather[anno] = {"GP": len(data1), "V": len(data1.values())}

df_weather = pd.DataFrame(dict_weather).transpose()
print(f'\nWEATHER RACE\n')
print(df_weather)