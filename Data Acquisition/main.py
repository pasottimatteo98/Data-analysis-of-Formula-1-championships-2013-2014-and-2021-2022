import concurrent.futures
import subprocess
import sys


def run_script(script_name):
    print(f"Executing {script_name}:")
    subprocess.run([sys.executable, script_name], check=True)


if __name__ == "__main__":
    # Web scraping scripts for seasons (executed in parallel)
    script_names_web_scraping = ["Seasons/WS_Season2013.py", "Seasons/WS_Season2014.py", "Seasons/WS_Season2021.py",
                                 "Seasons/WS_Season2022.py"]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the web scraping scripts for seasons in parallel
        futures_web_scraping = [executor.submit(run_script, script) for script in script_names_web_scraping]

        # Wait for all web scraping scripts for seasons to complete
        concurrent.futures.wait(futures_web_scraping)

    print("Web Scraping of Seasons Completed")

    # Conversion scripts for PDF Qualifying Max Speed to JSON
    script_names_conversion = [
        "Qualifying_Max_Speed/PDFtoJSON_2013.py",
        "Qualifying_Max_Speed/PDFtoJSON_2014.py",
        "Qualifying_Max_Speed/PDFtoJSON_2021.py",
        "Qualifying_Max_Speed/PDFtoJSON_2022.py",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the PDF-to-JSON conversion scripts in parallel
        futures_conversion = [executor.submit(run_script, script) for script in script_names_conversion]

        # Wait for all conversion scripts to complete
        concurrent.futures.wait(futures_conversion)

    print("Conversion of PDF Qualifying Max Speed to JSON completed")

    print("Merging Qualifying Max Speed - Seasons")
    script_names_merge_qualifying_max_speed = [
        "Merge/QualifyingMaxSpeed_Season_Merge2013.py",
        "Merge/QualifyingMaxSpeed_Season_Merge2014.py",
        "Merge/QualifyingMaxSpeed_Season_Merge2021.py",
        "Merge/QualifyingMaxSpeed_Season_Merge2022.py",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Esegui gli script di merge Qualifying Max Speed - Seasons in parallelo
        futures_merge_qualifying_max_speed = [executor.submit(run_script, script) for script in
                                              script_names_merge_qualifying_max_speed]

        # Attendi il completamento di tutti gli script di merge Qualifying Max Speed - Seasons
        concurrent.futures.wait(futures_merge_qualifying_max_speed)

    print("Merging Qualifying Max Speed - Seasons Completed")

    # Web scraping scripts for Weather Qualifying
    script_names_weather_qualifying = [
        "Weather/WS_Weather_Qualifying/WS_Weather2013_Qualifying.py",
        "Weather/WS_Weather_Qualifying/WS_Weather2014_Qualifying.py",
        "Weather/WS_Weather_Qualifying/WS_Weather2021_Qualifying.py",
        "Weather/WS_Weather_Qualifying/WS_Weather2022_Qualifying.py",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the web scraping scripts for Weather Qualifying in parallel
        futures_weather_qualifying = [executor.submit(run_script, script) for script in script_names_weather_qualifying]

        # Wait for all web scraping scripts for Weather Qualifying to complete
        concurrent.futures.wait(futures_weather_qualifying)

    print("Web Scraping of Weather Qualifying Completed")

    # Web scraping scripts for Weather Race
    script_names_weather_race = [
        "Weather/WS_Weather_Race/WS_Weather2013_Race.py",
        "Weather/WS_Weather_Race/WS_Weather2014_Race.py",
        "Weather/WS_Weather_Race/WS_Weather2021_Race.py",
        "Weather/WS_Weather_Race/WS_Weather2022_Race.py",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the web scraping scripts for Weather Race in parallel
        futures_weather_race = [executor.submit(run_script, script) for script in script_names_weather_race]

        # Wait for all web scraping scripts for Weather Race to complete
        concurrent.futures.wait(futures_weather_race)

    print("Web Scraping of Weather Race Completed")

    # Merge Weather Qualifying scripts
    script_names_merge_weather_qualifying = [
        "Merge/Weather_Merge_Qualifying2013.py",
        "Merge/Weather_Merge_Qualifying2014.py",
        "Merge/Weather_Merge_Qualifying2021.py",
        "Merge/Weather_Merge_Qualifying2022.py",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the merge scripts for Weather Qualifying in parallel
        futures_merge_weather_qualifying = [executor.submit(run_script, script) for script in
                                            script_names_merge_weather_qualifying]

        # Wait for all merge scripts for Weather Qualifying to complete
        concurrent.futures.wait(futures_merge_weather_qualifying)

    print("Merging Weather Qualifying Completed")

    # Merge Weather Race scripts
    script_names_merge_weather_race = [
        "Merge/Weather_Merge_Race2013.py",
        "Merge/Weather_Merge_Race2014.py",
        "Merge/Weather_Merge_Race2021.py",
        "Merge/Weather_Merge_Race2022.py",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the merge scripts for Weather Race in parallel
        futures_merge_weather_race = [executor.submit(run_script, script) for script in script_names_merge_weather_race]

        # Wait for all merge scripts for Weather Race to complete
        concurrent.futures.wait(futures_merge_weather_race)

    print("Merging Weather Race Completed")

    print("All scripts have been executed.")
