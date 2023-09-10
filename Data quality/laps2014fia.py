import json

import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode

nomi_gran_premi = [
    "australia", "malaysia", "bahrain", "china", "spain", "monaco", "canada", "austria",
    "great-britain", "germany", "hungary", "belgium", "italy", "singapore",
    "japan", "russia", "united-states", "brazil", "abu-dhabi"
]

nomi_formattati = {
    "australia": "Australian",
    "malaysia": "Malaysian",
    "china": "Chinese",
    "bahrain": "Bahrain",
    "spain": "Spanish",
    "monaco": "Monaco",
    "canada": "Canadian",
    "austria": "Austrian",
    "great-britain": "British",
    "germany": "German",
    "hungary": "Hungarian",
    "belgium": "Belgian",
    "italy": "Italian",
    "singapore": "Singapore",
    "korea": "Korean",
    "japan": "Japanese",
    "russia": "Russian",
    "abu-dhabi": "Abu Dhabi",
    "united-states": "United States",
    "brazil": "Brazilian",
}
all_data = {}
number = 0
for nome in nomi_gran_premi:

    number += 1

    data = []
    # URL della pagina web da cui fare lo scraping
    url = f"https://www.formula1.com/en/results.html/2014/races/{897+number}/{nome}/race-result.html"

    # Effettua la richiesta HTTP alla pagina web
    response = requests.get(url)

    # Controlla se la richiesta è andata a buon fine
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Trova la tabella con la classe "resultsarchive-table"
        race_table = soup.find("table", {"class": "resultsarchive-table"})



        # Trova tutte le righe della tabella tranne l'intestazione
        race_rows = race_table.find_all("tr")[1:]

        # Itera attraverso le righe della tabella e estrai i dati desiderati
        for row in race_rows:
            driver_cell = row.find("td", {"class": "dark bold"})
            lap_cell = row.find("td", {"class": "bold hide-for-mobile"})

            if driver_cell is not None and lap_cell is not None:
                driver_name_spans = driver_cell.find_all("span", {"class": "hide-for-tablet"})
                driver_surname_span = driver_cell.find("span", {"class": "hide-for-mobile"})

                driver_name_parts = [span.text.strip() for span in driver_name_spans]

                # Verifica se l'elemento driver_surname_span è presente
                if driver_surname_span is not None:
                    driver_name = " ".join(driver_name_parts) + " " + driver_surname_span.text.strip()
                else:
                    driver_name = " ".join(driver_name_parts)

                laps_completed = lap_cell.text.strip()
                if laps_completed == '':
                    laps_completed = 0

                data.append({'Driver': driver_name, 'Laps': int(laps_completed)})

    df = pd.DataFrame(data)

    if nome in nomi_formattati:
        nome = nomi_formattati[nome]

    all_data[f'{nome} GP'] = df.to_dict(orient='records')
print(all_data)


with open('laps2014fia.json', 'w') as json_file:
    json.dump(all_data, json_file, indent=4)

print("Data saved to laps2014fia.json")