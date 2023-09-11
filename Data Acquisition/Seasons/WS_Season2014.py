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
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

# Initialize the Chrome chrome_driver
chrome_driver = webdriver.Chrome()

# List of all possible values for the 2014 season (race and chrome_driver)
seasons = ['6'] #Season 2014
races = ['103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121'] #19 Piste
drivers = ['22', '9', '27', '5', '32', '10', '15', '40', '18', '6', '36', '31', '11', '2', '16', '34', '39', '44', '45', '4', '42', '24', '43', '41']
#24 Piloti ('42' non ha fatto le ultime 4 gare, '24' e '43 non hanno fatto le ultime 3 gare, '40' non ha fatto 4 gare nella stagione, '39' ha fatto solo l'ultima e '41' solo una gara

# Set the year of our interest.
year_of_search = 2014

# <editor-fold desc="First Webscraping">

# Initialize the main dictionary that will contain all the complete_data
complete_data = {}
searched_fields = ['Summary', 'Practice', 'Qualifying', 'Pitstops', 'Race progression', 'Laps']

# Iterate through all possible combinations of chrome_driver, race, and season.
for d, r, s in itertools.product(drivers, races, seasons):
    current_url = f'https://pitwall.app/analysis/race-report?utf8=%E2%9C%93&season={s}&race={r}&driver={d}&button='
    chrome_driver.get(current_url)
    try:
        WebDriverWait(chrome_driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".section")))
    except TimeoutException:
        print("Timeout durante l'attesa dell'elemento. Riprovare...")
        # Riprova l'attesa per un numero limitato di volte, ad esempio, 3 volte
        for _ in range(10):
            try:
                chrome_driver.get(current_url)
                WebDriverWait(chrome_driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".section")))
                break  # Esci dal ciclo se l'elemento viene trovato
            except TimeoutException:
                print("Timeout durante il tentativo di attesa. Riprovare...")
        else:
            print("Attende fallita dopo diversi tentativi.")
            # Gestisci l'errore o esci dallo script se necessario    soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')

    soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')

    # Extract all sections that have the class ".block-title".
    items = soup.select('.block-title')

    # Create a pattern to extract Year, Grand Prix Name, and Driver.
    pattern = r"(\d{4})\s+(.+)\s+-\s+(.+)"
    match = re.search(pattern, items[1].getText())

    # Extract the three strings corresponding to the three capture groups of the regex pattern.
    if match:
        year = match.group(1)
        race_name = match.group(2)
        driver_name = match.group(3)

    # Retrieve all sections of the website.
    sections = soup.select('.section')

    # Create default dictionaries for Drivers and Grand Prixes inside them.
    complete_data.setdefault(driver_name, {})
    complete_data[driver_name].setdefault(race_name, {})

    # Iterate through all sections except the first one.
    for i, section in enumerate(sections[1:]):

        # Remove the '\n'
        section_data = section.get_text().strip().replace('\n', '')

        # Insert the titles of the various sections into the races.
        for title in items:
            if title.getText() in section_data:
                complete_data[driver_name][race_name][title.getText()] = section_data
                break

    # Remove the sections that are not useful to us.
    complete_data[driver_name][race_name].pop('Summary', None)
    complete_data[driver_name][race_name].pop('Practice', None)
    complete_data[driver_name][race_name].pop('Pitstops', None)
    complete_data[driver_name][race_name].pop('Race progression', None)

    # Search for and insert the necessary fields for the Qualifying section.
    if 'Qualifying' in complete_data[driver_name][race_name]:
        Qualifying_data = complete_data[driver_name][race_name]['Qualifying']
        if type(complete_data[driver_name][race_name]['Qualifying']) == str:
            complete_data[driver_name][race_name]['Qualifying'] = {}
            q3_time = re.findall(r'Q3 Time(\d+:\d+\.\d+)', Qualifying_data)
            q2_time = re.findall(r'Q2 Time(\d+:\d+\.\d+)', Qualifying_data)
            q1_time = re.findall(r'Q1 Time\s+(\d+:\d+\.\d+)', Qualifying_data)
            complete_data[driver_name][race_name]['Qualifying']['Q3 Time'] = q3_time
            complete_data[driver_name][race_name]['Qualifying']['Q2 Time'] = q2_time
            complete_data[driver_name][race_name]['Qualifying']['Q1 Time'] = q1_time

    # Search for and insert the necessary fields for the Laps section.
    if 'Laps' in complete_data[driver_name][race_name]:
        Lap_data = complete_data[driver_name][race_name]['Laps']
        if type(complete_data[driver_name][race_name]['Laps']) == str:
            complete_data[driver_name][race_name]['Laps'] = {}
            pattern = r"\d+:\d+\.\d+"
            times = re.findall(pattern, str(Lap_data))
            n_lap = range(1, len(times) + 1)
            for c in n_lap:
                complete_data[driver_name][race_name]['Laps'][c] = times[c - 1]

    # Wait for a short period of time before making the next request.
    time.sleep(1)

# </editor-fold>

# <editor-fold desc="Second Webscraping">

# Pilot - Car Webscrabing
current_url = "https://pitwall.app/seasons/2014-formula-1-world-championship"
chrome_driver.get(current_url)
WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".section")))
soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')

# Retrieve the necessary table.
table = soup.select_one('.ui-tabs-panel')

# Retrieve each row of the table
rows = table.find_all("tr")

# Initialize the dictionary
driver_car_data = []

# For each row except the first one, which is the header row, retrieve the columns and save the data in the dictionary
for row in rows[1:]:
    cols = row.find_all("td")
    driv = cols[1].get_text(strip=True)
    car = cols[2].get_text(strip=True)
    driver_car_data.append({"Driver": driv, "Car": car})

# Insert the cars into the main dictionary based on the driver's name.
for item in driver_car_data:
    driv = item['Driver']
    car = item['Car']
    found_match = False
    for key in complete_data.keys():
        similarity = fuzz.ratio(driv, key)
        if similarity >= 75:
            complete_data[key]['Car'] = car
            found_match = True
            break
    if not found_match:
        complete_data[driv] = {'Car': car}

# Wait for a short period of time before making the next request.
time.sleep(1)

# </editor-fold>

# <editor-fold desc="Third Webscraping">


# Race Circuit Webscrabing
url = f"https://en.wikipedia.org/wiki/{year_of_search}_Formula_One_World_Championship"
chrome_driver.get(url)
WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wikitable")))
soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')

# Select all the tables with the class .wikitable.
tables = soup.select('.wikitable')

# Our table of interest is the third one.
table = tables[2]

# Extract the rows
rows = table.find_all("tr")

# Initialize the dictionary
Circuit_Data = []

# For each row  retrieve the columns and save the data in the dictionary
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if cols:
        # Change the name from "Grand Prix" to "GP" for compatibility with the first dictionary.
        race_prix = cols[0].text.strip().replace("Grand Prix", "GP")

        name_circuit = cols[1].text.strip()
        name_circuit = name_circuit.split(",")[0]
        Circuit_Data.append({"Circuit": name_circuit, "Prix": race_prix})

# Insert the Circuit into the main dictionary foreach driver based on the races name.
for item in Circuit_Data:
    circuit = item['Circuit']
    prix = item['Prix']
    for pilot in complete_data:
        if prix in complete_data[pilot]:
            complete_data[pilot][prix]['Circuit'] = {'Name': circuit, 'Length': None, 'Turns': None}

# Wait for a short period of time before making the next request.
time.sleep(1)

# </editor-fold>


# Initialize the dictionary.
circuit_url = []

# Insert the circuit names into the dictionary by replacing spaces with underscores.
for item in Circuit_Data:
    final_url = item["Circuit"].replace(" ", "_")
    circuit_url.append({"CircuitURL": final_url})

# <editor-fold desc="Fourth Webscraping">

# Initialize the dictionary.
stats_circuit = []

# For each converted circuit, insert it into the Wikipedia URL and perform webscraping for each site
for _url in circuit_url:
    _url = _url["CircuitURL"]
    current_url = f"https://en.wikipedia.org/wiki/{_url}"
    chrome_driver.get(current_url)
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".infobox")))
    soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')

    # Retrieve the necessary table.
    table = soup.select_one('.vcard')

    # Search for the string "Grand Prix Circuit" and if present, start processing all the data extracted from the
    # "Grand Prix Circuit" string. Then remove any noise present in the data acquisition.
    indice = table.getText().find("Grand Prix Circuit")
    if indice != -1:
        sub_string = table.getText()[indice:].replace("(5th Variation)", "") \
            .replace("(4th Variation)", "") \
            .replace("(3rd Variation)", "") \
            .replace("(2nd Variation)", "") \
            .replace("(1st Variation)", "") \
            .replace("present", "2023")
        sub_string = re.sub(r"\bMotorcycle Grand Prix Circuit\b", "", sub_string)
        sub_string = sub_string.replace("SurfaceAsphalt concrete with Graywacke aggregate", "")

    # Initialize the dictionary.
    date_matches = []

    # Insert the year ranges present on the page into the dictionary.
    for date_match in re.findall(r"\bGrand Prix Circuit\b \((.*?)\)", sub_string):
        if date_match not in date_matches:
            date_matches.append(date_match)
    date_matches += re.findall(r"6th Variation \((.*?)\)", sub_string)
    date_matches += re.findall(r"GP-Strecke \((.*?)\)", sub_string)
    date_matches += re.findall(r"Red Bull Ring \((.*?)\)", sub_string)



    # For each date range or single date found, check if it matches our reference year or if it is within the range.
    for date_match in date_matches:
        if "–" in date_match:
            anno_inizio, anno_fine = date_match.split("–")
            if int(anno_inizio) <= year_of_search <= int(anno_fine):

                # Split on the date range and take the second match.
                circuit_info = sub_string.split(date_match)[1]

                # Check if there is 'Length' in the match, otherwise look in the next one
                if "Length" not in circuit_info:
                    circuit_info = sub_string.split(date_match)[2]
                if "Length" in circuit_info:
                    # Extract the length and clean it up.
                    length = circuit_info.split("Length")[1].split("km")[0].strip().replace("[1]", "").replace(
                        "[2]", "").replace("[3]", "").replace("[4]", "").replace("[5]", "").replace("3.426 miles (", "")

                    # Extract the turns and clean it up.
                    turns_match = re.search(r'Turns(\d+)', circuit_info)
                    curve = turns_match.group(1)

                    # Adjust the circuit names to insert them into the dictionary.
                    turns = _url.replace("_", " ")
                    stats_circuit.append({"Circuit": turns, "Length": length, "Turns": curve})
        else:
            if year_of_search == date_match:
                # Split on the date range and take the second match.
                circuit_info = sub_string.split(date_match)[1]

                # Check if there is 'Length' in the match, otherwise look in the next one
                if "Length" not in circuit_info:
                    circuit_info = sub_string.split(date_match)[2]
                if "Length" in circuit_info:
                    # Extract the length and clean it up.
                    length = circuit_info.split("Length")[1].split("km")[0].strip().replace("[1]", "").replace(
                        "[2]", "").replace("[3]", "").replace("[4]", "").replace("[5]", "").replace("3.426 miles (", "")

                    # Extract the turns and clean it up.
                    turns_match = re.search(r'Turns(\d+)', circuit_info)
                    curve = turns_match.group(1)

                    # Adjust the circuit names to insert them into the dictionary.
                    turns = _url.replace("_", " ")
                    stats_circuit.append({"Circuit": turns, "Length": length, "Turns": curve})

    # Wait for a short period of time before making the next request.
    time.sleep(1)

# Insert the data of each circuit into the main dictionary for each driver and for each race, based on the name of
# the circuit.
for driver in complete_data:
    for gp in complete_data[driver]:
        if gp != "Car":
            nome_circuito = complete_data[driver][gp]["Circuit"]["Name"]
            for circuit in stats_circuit:
                if circuit["Circuit"] == nome_circuito:
                    complete_data[driver][gp]["Circuit"]["Length"] = circuit["Length"]
                    complete_data[driver][gp]["Circuit"]["Turns"] = circuit["Turns"]

# </editor-fold>

# Close the Selenium chrome_driver.
chrome_driver.quit()

# Writes the data to the JSON file.
with open(f'../RawDataCollected/WebScraping/Seasons/Season{year}.json', 'w') as outfile:
    json.dump(complete_data, outfile, indent=4)
