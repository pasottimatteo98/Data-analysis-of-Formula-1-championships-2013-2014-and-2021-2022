import os
import re
import json
from PyPDF4 import PdfFileReader

# Percorso della cartella contenente i file PDF
pdf_folder = 'Qualifying_Session_Max_Speed_2021/'

# Loop attraverso tutti i file nella cartella
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        file_path = os.path.join(pdf_folder, filename)
        print(filename)
        # Apri il file PDF
        with open(file_path, 'rb') as pdf_file:
            # Leggi il contenuto del PDF
            pdf_reader = PdfFileReader(pdf_file)
            pdf_content = ""
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                pdf_content += page.extractText()

                # interrompi la lettura del contenuto del PDF se incontra la parola "FINISH LINE"
                if "FINISH LINE" in pdf_content:
                    pdf_content = pdf_content.split("FINISH LINE")[0]
                    break

        # Estrarre il nome della gara e l'anno dal nome del file PDF
        race_name = ""
        race_year = ""
        match = re.match(r'(.+?)\s-\s(\d{4})', filename)
        if match:
            race_name = match.group(1).strip()
            race_year = int(match.group(2))

        # Converti il contenuto in formato JSON
        json_content = json.dumps({'content': pdf_content})

        data = json.loads(json_content)

        rows = data['content'].split('\n\n')[3:-1]
        results = []

        for i in range(0, len(rows), 4):
            if "KM/H" in rows[i]:
                continue
            result = {
                'driver': rows[i + 1],
                'km/h': rows[i + 2],
                'gp': race_name,
                'year': race_year
            }
            results.append(result)

        # Scrivi i risultati della gara in un file JSON
        output_file = f'{race_name} - {race_year}.json'
        output_path = os.path.join('Qualifying_Session_Max_Speed_2021/', output_file)
        with open(output_path, 'w') as json_file:
            json_file.write(json.dumps(results, indent=2))
