import itertools
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Inizializza il driver di Chrome
s = Service('../ChromeDriver/chromedriver.exe')
driver = webdriver.Chrome(service=s)
# URL della pagina da cui effettuare lo scraping

# Lista di tutti i possibili valori della stagione 2022  (gara e pilota)
seasons = ['74'] #Season 2022
races = ['1156', '1157', '1158', '1159', '1160', '1161', '1162', '1163', '1164', '1165', '1166', '1167', '1168', '1169', '1170', '1171', '1172', '1173', '1174', '1175', '1176', '1177'] #22 Piste
drivers = ['17', '22', '9', '13', '10', '15', '848', '3', '6', '7', '21', '11', '16', '20', '8', '853', '12', '851', '14' , '854', '4', '855' ]
#22 Piloti ('4' ha saltato 2 gare, '855' ne ha fatta solo 1 e '15' ne ha fatte solo 2)

# Inizializza il dizionario che conterrà tutti i dati
data = {}
data_inside = ['Summary', 'Practice', 'Qualifying', 'Pitstops', 'Race progression', 'Laps']


# Itera su tutte le possibili combinazioni di stagione, gara e pilota
for s, r, d in itertools.product(seasons, races, drivers):
    # Costruisce l'URL con i valori correnti
    current_url = f'https://pitwall.app/analysis/race-report?utf8=%E2%9C%93&season={s}&race={r}&driver={d}&button='
    # Visita l'URL con Selenium
    driver.get(current_url)
    # Attende che la pagina sia caricata
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".section")))
    # Crea un oggetto Beautiful Soup a partire dal contenuto HTML della pagina
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    Title = soup.select_one('.section')
    pattern = r"(\d{4})\s+(\w+\s+\w+)\s+-\s+(\w+\s+\w+)"

    # Esegui la ricerca del pattern nella stringa di esempio
    match = re.search(pattern, Title.getText())

    # Estrai le tre stringhe corrispondenti ai tre gruppi di cattura del pattern regex
    if match:
        year = match.group(1)
        race_name = match.group(2)
        driver_name = match.group(3)

    # Estrae i dati dal contenuto della pagina
    sections = soup.select('.section')
    data[f"{driver_name} - {race_name}"] = {}
    for i, section in enumerate(sections):
        section_data = section.get_text().strip().replace('\n', '')
        data[f"{driver_name} - {race_name}"][data_inside[i]] = section_data
    # Attende un breve periodo di tempo prima di effettuare la successiva richiesta
    time.sleep(1)

# Chiude il driver di Selenium
driver.quit()

# Scrive i dati nel file JSON
with open(f'../RawDataCollected/WebScraping/Season{year}.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
