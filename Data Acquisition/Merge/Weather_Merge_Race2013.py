import json

# Load the content of the first JSON file containing race data for 2013
with open('Final_Data/FinalDataset2013.json', 'r') as file1:
    data1 = json.load(file1)

# Load the content of the second JSON file containing weather data for race laps in 2013
with open('../RawDataCollected/WebScraping/Weather_Race/2013/Weather_Race.json', 'r') as file2:
    data2 = json.load(file2)

# Iterate through the first dictionary and add weather information for each race lap
for driver, races in data1.items():
    for race, details in races.items():
        if race in data2:
            if "Laps" in details:
                details["Laps"]["Weather Condition"] = data2[race]

# Save the merged result into a new JSON file, overwriting the existing 'FinalDataset2013.json'
with open('Final_Data/FinalDataset2013.json', 'w') as outfile:
    json.dump(data1, outfile, indent=4)
