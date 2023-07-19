import os
import re
import json
from PyPDF4 import PdfFileReader

# Path to the folder containing the PDF files
pdf_folder = 'Qualifying_Max_Speed/Qualifying_Session_Max_Speed_2021'

# Loop through each file in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        file_path = os.path.join(pdf_folder, filename)
        print(filename)
        # Open the PDF file
        with open(file_path, 'rb') as pdf_file:
            # Read the content of the PDF
            pdf_reader = PdfFileReader(pdf_file)
            pdf_content = ""
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                pdf_content += page.extractText()

                # Stop reading the content of the PDF if it encounters the word "FINISH LINE"
                if "FINISH LINE" in pdf_content:
                    pdf_content = pdf_content.split("FINISH LINE")[0]
                    break

        # Extract the race name and year from the PDF filename
        race_name = ""
        race_year = ""
        match = re.match(r'(.+?)\s-\s(\d{4})', filename)
        if match:
            race_name = match.group(1).strip()
            race_year = int(match.group(2))

        # Convert the content to JSON format
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

        # Write the race results to a JSON file
        output_file = f'{race_name} - {race_year}.json'
        output_path = os.path.join('../RawDataCollected/WebScraping/Qualifying_Max_Speed/2021', output_file)
        with open(output_path, 'w') as json_file:
            json_file.write(json.dumps(results, indent=2))
