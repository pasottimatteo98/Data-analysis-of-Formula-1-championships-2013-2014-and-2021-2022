#2013 GARA

import json

import requests
from bs4 import BeautifulSoup
import pandas as pd

nomi_gran_premi = [
    "Australian", "Malaysian", "Chinese", "Bahrain", "Spanish", "Monaco", "Canadian",
    "British", "German", "Hungarian", "Belgian", "Italian", "Singapore", "Korean",
    "Japanese", "Indian", "Abu_Dhabi", "United_States", "Brazilian"
]

risultati = {}

# Funzione per ottenere il testo compreso tra "Qualifiche" e "Risultati"
def ottenere_testo_tra_sezioni(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table row containing the weather information
    clima_element = soup.find("th", string="Weather")
    if clima_element:
        clima_row = clima_element.parent
        clima_data = clima_row.find("td").text.strip()
        return clima_data
    else:
        return ""

nomi_formattati = {
    "Abu_Dhabi": "Abu Dhabi",
    "United_States": "United States"
}

for nome_gran_premio in nomi_gran_premi:
    # Costruisci l'URL del Gran Premio specifico
    url = f"https://en.wikipedia.org/wiki/2013_{nome_gran_premio}_Grand_Prix"

    # Esegue l'analisi del testo delle qualifiche e dei risultati
    clima = ottenere_testo_tra_sezioni(url)


    # Salva il testo su un file
    #nome_file = f"{nome_gran_premio}_qualifiche_risultati.txt"
    #with open(nome_file, "w") as file:
    #    file.write(testo_qualifiche_risultati)

    # Lista di parole chiave relative alle condizioni meteo
    parole_chiave_meteo = [
        'wet', 'rain', 'rainfalls'
    ]

    # Cercare le parole chiave nel testo delle qualifiche e dei risultati
    condizione_meteo = ""
    for parola_chiave in parole_chiave_meteo:
        if parola_chiave in clima.lower():
            condizione_meteo = "rain"
            break

    # Se nessuna parola chiave corrispondente è stata trovata, assegna "sole" come condizione predefinita
    if not condizione_meteo:
        condizione_meteo = "sun"

    if nome_gran_premio in nomi_formattati:
        nome_gran_premio = nomi_formattati[nome_gran_premio]


    chiave_dizionario = f"{nome_gran_premio} GP"
    risultati[chiave_dizionario] = condizione_meteo


with open("../RawDataCollected/WebScraping/Weather_Race/2013/Weather_Race.json", "w") as file:
    json.dump(risultati, file, indent=4, ensure_ascii=False)