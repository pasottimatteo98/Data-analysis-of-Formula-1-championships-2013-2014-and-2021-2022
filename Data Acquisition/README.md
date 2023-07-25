# Progetto Data Management

## Installation
To install the required dependencies, use the following command:

```bash
pip install -r requirements.txt
```


## ChromeDriver
Current Version: chromedriver 115.0.5790.102  
Other version if needed:
https://googlechromelabs.github.io/chrome-for-testing/#stable

## Interpreter
A virtual Python 3.9 interpreter was used, but Conda support is also enabled.


## main.py

The main.py script is responsible for running various other scripts for web scraping and data processing. It is organized into different sections to perform specific tasks. Here's an overview of what each section does:
Web Scraping for Seasons

### Web Scraping for Seasons
This section runs web scraping scripts for different seasons. It executes the scripts sequentially for each season to gather data.
Conversion of PDF Qualifying Max Speed to JSON

### Conversion of PDF Qualifying Max Speed to JSON
This section runs scripts to convert PDF files containing qualifying max speed data to JSON format.
Merging Qualifying Max Speed - Seasons

### Merging Qualifying Max Speed - Seasons
After scraping and converting data, this section merges the qualifying max speed data with the corresponding season data.
Web Scraping of Weather Qualifying

### Web Scraping of Weather Qualifying
In this section, web scraping scripts are executed for collecting weather data during qualifying sessions.
Web Scraping of Weather Race

### Web Scraping of Weather Race
Similar to the previous section, this part runs web scraping scripts to collect weather data during race sessions.
Merging Weather Qualifying

### Merging Weather Qualifying
This section merges the weather data collected during qualifying with the corresponding race data.
Merging Weather Race

### Merging Weather Race
Finally, this section merges the weather data collected during race sessions with the rest of the data.

Once all the sections are executed, you will have the desired data merged and processed for further analysis.
Running the Script

## Running the Script
To run the main.py script, simply execute the following command:

```bash
python main.py
```
The script will start executing the various tasks in parallel (wherever possible) to speed up the process. You will see progress messages and be notified once all the scripts have been executed successfully.

