import os
import json

season_path = "Merged_Data/Qualifying_Season_Merged_2013.json"

# Load the content of the first JSON file
with open(season_path, 'r') as file1:
    data1 = json.load(file1)

# Load the content of the second JSON file containing weather data
with open('../RawDataCollected/WebScraping/Weather_Qualifying/2013/Weather_Qualifying.json', 'r') as file2:
    data2 = json.load(file2)

# Iterate through the first dictionary and add weather information for each race
for driver, races in data1.items():
    for race, details in races.items():
        if race in data2:
            if "Qualifying" in details:
                details["Qualifying"]["Weather Condition"] = data2[race]

# Save the merged result into a new JSON file
with open('Final_Data/FinalDataset2013.json', 'w') as outfile:
    json.dump(data1, outfile, indent=4)
