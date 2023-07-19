import PyPDF4
import re
import json
import os

# Define the input and output directories
input_dir = "Qualifying_Max_Speed/Qualifying_Session_Max_Speed_2013"
output_dir = "../RawDataCollected/WebScraping/Qualifying_Max_Speed/2013"

# Iterate through each file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.pdf'):
        file_path = os.path.join(input_dir, filename)

        # Open the PDF file
        with open(os.path.join(input_dir, filename), 'rb') as pdf_file:
            pdf_reader = PyPDF4.PdfFileReader(pdf_file)

            filename = os.path.basename(pdf_file.name)
            print(filename)
            gp_name = re.search(r'^([\w\s]+) - \d{4}\.pdf$', filename).group(1)
            year = int(re.search(r'^[\w\s]+ - (\d{4})\.pdf$', filename).group(1))

            # Extract the text from each page of the PDF
            text = ''
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()

            # Use regular expressions to extract the required data
            pattern = re.compile(r'^\d+\s+(\d+)\s+(.+)\s+(\d+\.\d+)\s+(\d+:\d+:\d+)$', re.MULTILINE)
            data = []
            for match in pattern.finditer(text):
                entry = {
                    'driver': match.group(2),
                    'km/h': float(match.group(3)),
                    'gp': gp_name,
                    'year': year
                }
                data.append(entry)

            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'w') as output_file:
                json_data = json.dumps(data, indent=4)
                output_file.write(json_data)
