#2022 qualifiche

import json
import requests
from bs4 import BeautifulSoup

nomi_gran_premi = [
    "Bahrain", "Saudi_Arabian", "Australian", "Emilia_Romagna", "Miami", "Spanish", "Monaco",
    "Azerbaijan", "Canadian", "British", "Austrian", "French", "Hungarian",
    "Belgian", "Dutch", "Italian", "Singapore", "Japanese", "United_States", "Mexico_City", "Brazilian", "Abu_Dhabi"
]

risultati = {}


# Funzione per ottenere il testo compreso tra due sezioni
def ottenere_testo_tra_sezioni(url, inizio_sezione, fine_sezione):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    inizio = soup.find("span", id=inizio_sezione)
    fine = soup.find("span", id=fine_sezione)

    # Verifica se le sezioni sono state trovate correttamente
    if inizio and fine:
        paragrafi = soup.find_all("p")

        # Trova l'indice del primo paragrafo dopo la sezione di inizio
        indice_inizio = paragrafi.index(inizio.find_next("p"))

        # Trova l'indice del primo paragrafo prima della sezione di fine
        indice_fine = paragrafi.index(fine.find_previous("p"))

        # Estrai il testo compreso tra le sezioni
        testo_sezione = ""
        for i in range(indice_inizio, indice_fine + 1):
            testo_sezione += paragrafi[i].get_text() + "\n"

        return testo_sezione.strip()  # Rimuovi eventuali spazi vuoti all'inizio e alla fine del testo finale

    else:
        return ""


nomi_formattati = {
    "Abu_Dhabi": "Abu Dhabi",
    "United_States": "United States",
    "Saudi_Arabian": "Saudi Arabian",
    "Emilia_Romagna": "Emilia Romagna",
    "Mexico_City": "Mexico City"
}

for nome_gran_premio in nomi_gran_premi:
    # Costruisci l'URL del Gran Premio specifico
    url = f"https://en.wikipedia.org/wiki/2022_{nome_gran_premio}_Grand_Prix"

    # Esegue l'analisi del testo delle qualifiche e dei risultati
    testo_qualifiche_risultati = ottenere_testo_tra_sezioni(url, "Qualifying", "Sprint_qualifying")
    if not testo_qualifiche_risultati:
        testo_qualifiche_risultati = ottenere_testo_tra_sezioni(url, "Qualifying", "Race")

    # Salva il testo su un file
    # nome_file = f"{nome_gran_premio}_qualifiche_risultati.txt"
    # with open(nome_file, "w", encoding="utf-8") as file:
    #    file.write(testo_qualifiche_risultati)

    # Lista di parole chiave relative alle condizioni meteo
    parole_chiave_meteo = [' wet', ' rain', ' rainfalls', 'Rain', ' Rain', ' Rainfalls', ' wet']

    # Cercare le parole chiave nel testo delle qualifiche e dei risultati
    condizione_meteo = ""
    for parola_chiave in parole_chiave_meteo:
        if parola_chiave in testo_qualifiche_risultati.lower():
            condizione_meteo = "rain"
            break

    # Se nessuna parola chiave corrispondente è stata trovata, assegna "sole" come condizione predefinita
    if not condizione_meteo:
        condizione_meteo = "sun"

    chiave_dizionario = f"{nome_gran_premio} GP"
    risultati[chiave_dizionario] = condizione_meteo

    nomi_completi = {
        "Emilia_Romagna": "Gran_Premio_dell'Emilia-Romagna",
        "Bahrain": "Gran_Premio_del_Bahrein",
        "Spanish": "Gran_Premio_di_Spagna",
        "Monaco": "Gran_Premio_di_Monaco",
        "Azerbaijan": "Gran_Premio_d'Azerbaigian",
        "Dutch": "Gran_Premio_d'Olanda",
        "British": "Gran_Premio_di_Gran_Bretagna",
        "Mexico_City": "Gran_Premio_di_Città_del_Messico",
        "Hungarian": "Gran_Premio_d'Ungheria",
        "Belgian": "Gran_Premio_del_Belgio",
        "Italian": "Gran_Premio_d'Italia",
        "Abu_Dhabi": "Gran_Premio_di_Abu_Dhabi",
        "United_States": "Gran_Premio_degli_Stati_Uniti_d'America",
        "Brazilian": "Gran_Premio_di_San_Paolo",
        "French": "Gran_Premio_di_Francia",
        "Saudi_Arabian": "Gran_Premio_d'Arabia_Saudita",
        "Austrian": "Gran_Premio_d'Austria",
        "Australian": "Gran_Premio_d'Australia",
        "Singapore": "Gran_Premio_di_Singapore",
        "Japanese": "Gran_Premio_del_Giappone",
        "Canadian": "Gran_Premio_del_Canada",
        "Miami": "Gran_Premio_di_Miami"
    }

    dizionario_nomi = {}

    for nome in nomi_gran_premi:
        dizionario_nomi[nome] = nomi_completi[nome]

    # Se il Gran Premio è classificato come "sun", effettua il web scraping sulla pagina Wikipedia italiana del Gran Premio corrispondente
    if condizione_meteo == "sun":
        nome_gran_premio_italiano = dizionario_nomi[nome_gran_premio]
        
        url_italian_gp = f"https://it.wikipedia.org/wiki/{nome_gran_premio_italiano}_2022"
        # Esegue l'analisi del testo delle qualifiche e dei risultati dalla pagina Wikipedia italiana
        testo_qualifiche_risultati_italiano = ottenere_testo_tra_sezioni(url_italian_gp, "Qualifiche",
                                                                         "Qualifica_Sprint")
        if not testo_qualifiche_risultati_italiano:
            testo_qualifiche_risultati_italiano = ottenere_testo_tra_sezioni(url_italian_gp, "Qualifiche", "Gara")
            # Salva il testo su un file
        #nome_file = f"{nome_gran_premio}_qualifiche_risultati.txt"
        #with open(nome_file, "w", encoding="utf-8") as file:
        #    file.write(testo_qualifiche_risultati_italiano)
        # Cercare le parole chiave nel testo delle qualifiche e dei risultati in italiano
        parole_chiave_meteo_italiano = [
            'bagnata', 'bagnato', 'pioggia,', 'acqua', 'gomme da bagnato', 'pista scivolosa',
            'spray d\'acqua', 'visibilità ridotta', 'aquaplaning',
            'pneumatici da pioggia'
        ]
        for parola_chiave in parole_chiave_meteo_italiano:
            if "possibile arrivo della pioggia" in testo_qualifiche_risultati_italiano:
                condizione_meteo = "sun"
            elif parola_chiave in testo_qualifiche_risultati_italiano.lower():
                condizione_meteo = "rain"
                break

    # Aggiungi la condizione per formattare il nome del Gran Premio
    if nome_gran_premio in nomi_formattati:
        nome_gran_premio = nomi_formattati[nome_gran_premio]


    chiave_dizionario = f"{nome_gran_premio} GP"
    risultati[chiave_dizionario] = condizione_meteo


del risultati["Abu_Dhabi GP"]
del risultati["United_States GP"]
del risultati["Mexico_City GP"]
del risultati["Saudi_Arabian GP"]
del risultati["Emilia_Romagna GP"]

# Salvataggio del dizionario su un file JSON
with open("../RawDataCollected/WebScraping/Weather_Qualifying/2022/Weather_Qualifying.json", "w", encoding="utf-8") as file:
    json.dump(risultati, file, indent=4, ensure_ascii=False)