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

# Lista di tutti i possibili valori della stagione 2014  (gara e pilota)
seasons = ['6'] #Season 2014
races = ['103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121'] #19 Piste
drivers = ['22', '9', '27', '5', '32', '10', '15', '40', '18', '6', '36', '31', '11', '2', '16', '34', '39', '44', '45', '4', '42', '24', '43', '41']
#24 Piloti ('42' non ha fatto le ultime 4 gare, '24' e '43 non hanno fatto le ultime 3 gare, '40' non ha fatto 4 gare nella stagione, '39' ha fatto solo l'ultima e '41' solo una gara

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
