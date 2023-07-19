import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Path to the folder with JSON files
folder_path = "../RawDataCollected/WebScraping/Qualifying_Max_Speed/2013"

# Path to the second JSON file
second_json_path = "../RawDataCollected/WebScraping/Seasons/Season2013.json"

# Load the second JSON
with open(second_json_path, "r") as f:
    second_json = json.load(f)
    #print(second_json)

# Explore the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(folder_path, filename), "r") as f:
            first_json = json.load(f)

        # Merge the two JSONs
        for driver_data in first_json:
            driver = driver_data["driver"]
            gp = driver_data["gp"]

            # Search for approximate matches of the driver's name in the second JSON
            driver_matches = process.extract(driver, second_json.keys(), scorer=fuzz.token_sort_ratio, limit=3)
            for driver_match in driver_matches:
                if driver_match[1] >= 60:
                    matched_driver = driver_match[0]
                    # Search for approximate matches of the GP's name in the second JSON
                    gp_matches = process.extract(gp, second_json[matched_driver].keys(), scorer=fuzz.token_sort_ratio,
                                                 limit=3)
                    for gp_match in gp_matches:
                        if gp_match[1] >= 60:
                            matched_gp = gp_match[0]
                            # Insert the "km/h" data at the specific point
                            second_json[matched_driver][matched_gp]["km/h"] = driver_data["km/h"]

    # Write the merged file
year = str(driver_data["year"])
with open("Merged_Data/Qualifying_Season_Merged_"+year+".json", "w") as f:
    json.dump(second_json, f, indent=4)
