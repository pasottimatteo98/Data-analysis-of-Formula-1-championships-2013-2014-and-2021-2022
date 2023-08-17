
import os
import json
import pandas as pd

# Lista delle cartelle con gli anni desiderati
anni = ['2013', '2014', '2021', '2022']

# Dizionario per memorizzare i dati
dati_per_anni = {}

for anno in anni:
    cartella_speed = f'../RawDataCollected/WebScraping/Qualifying_Max_Speed/{anno}'
    nomi_file_dict = {}  # Dizionario per memorizzare i nomi dei file

    for nome_file in os.listdir(cartella_speed):
        percorso_completo = os.path.join(cartella_speed, nome_file)
        if os.path.isfile(percorso_completo):
            nome_base, _ = os.path.splitext(nome_file)  # Ottieni il nome del file senza estensione
            nome_senza_anno = nome_base.replace(" - " + anno, "")  # Rimuovi " - <anno>"
            nomi_file_dict[nome_senza_anno] = percorso_completo
            with open(percorso_completo, 'r') as file1:
                data1 = json.load(file1)
            for dic in data1:
                nomi_file_dict[nome_senza_anno] = {"E": len(data1), "K": len(dic), "V": len(dic.values())}

    dati_per_anni[anno] = nomi_file_dict

# Creazione e visualizzazione del DataFrame
for anno, nomi_file_dict in dati_per_anni.items():
    df_speed = pd.DataFrame(nomi_file_dict).transpose()
    print(f'\n{anno}\n')
    print(df_speed)