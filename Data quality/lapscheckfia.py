
import os
import json
import pandas as pd

# Lista delle cartelle con gli anni desiderati
anni = ['2013', '2014', '2021', '2022']

for anno in anni:
    laps_file = f'../Data Quality/laps{anno}.json'
    laps_file_wiki = f'../Data Quality/laps{anno}fia.json'
    with open(laps_file, 'r') as file1:
        data1 = json.load(file1)
    with open(laps_file_wiki, 'r') as file2:
        data2 = json.load(file2)
    print(f'{anno}\n')
    for pilota, gare in data1.items():

        for gp, laps in gare.items():
            if gp in data2:
                for entry in data2[gp]:

                    while entry["Driver"] == pilota:
                        if entry["Laps"] == laps:
                            #print(f"ok - Pilota: {pilota}, GP: {gp}, Lappe: {laps}")
                            break
                        else:
                            laps2 = entry["Laps"]
                            print(f"errore - Pilota: {pilota}, GP: {gp}, Lappe file 1: {laps}, Lappe file 2: {laps2}")
                            break
            else:
                print(f"GP o pilota non trovato - Pilota: {pilota}, GP: {gp}")

    print(f"\nConfronto completato.\n")
