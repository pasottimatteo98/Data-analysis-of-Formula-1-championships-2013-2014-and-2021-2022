# Formula 1 Data Management System

A comprehensive data acquisition, processing, and analysis system for Formula 1 racing statistics across multiple seasons (2013, 2014, 2021, 2022).

## Project Overview

This project collects, processes, and analyzes Formula 1 racing data through web scraping multiple sources, data transformation, and storage in MongoDB for comprehensive analysis. The system captures detailed information about drivers, teams, races, qualifying sessions, lap times, weather conditions, and circuit characteristics.

## Repository Structure

```
├── ChromeDriver/            # Contains Chrome WebDriver executable
├── Data Acquisition/        # Main data acquisition scripts
│   ├── Final_Data/          # Final processed datasets
│   ├── Merge/               # Scripts for merging different data sources
│   ├── Merged_Data/         # Intermediate merged datasets
│   ├── Qualifying_Max_Speed/# Scripts for qualifying speed data
│   ├── Seasons/             # Web scraping scripts for season data
│   └── Weather/             # Weather data acquisition scripts
│       ├── WS_Weather_Qualifying/ # Weather during qualifying sessions
│       └── WS_Weather_Race/  # Weather during races
├── Data Quality/            # Data validation and quality checks
├── RawDataCollected/        # Raw data from web scraping
│   └── WebScraping/         # Organized by data type and season
├── Storage/                 # Database connection and query scripts
```

## Data Collection Process

The data acquisition pipeline involves several steps:

1. **Web Scraping**: Using Selenium and BeautifulSoup to scrape data from:
   - F1 statistics websites (pitwall.app)
   - Wikipedia (circuit information)
   - Official F1 website (race results)

2. **Data Processing**: Transforming raw data into structured formats:
   - Extracting qualifying times (Q1, Q2, Q3)
   - Collecting lap times
   - Gathering circuit information (length, turns)
   - Recording maximum speeds
   - Documenting weather conditions

3. **Data Merging**: Combining different data sources into comprehensive datasets:
   - Qualifying data with season data
   - Weather data integration
   - Circuit information alignment

4. **Database Storage**: Storing processed data in MongoDB for analysis

## Key Features

- Comprehensive F1 data across multiple seasons (2013, 2014, 2021, 2022)
- Detailed driver and team statistics
- Complete lap-by-lap timing data
- Qualifying session performance metrics
- Maximum speed information for qualifying sessions
- Weather condition data for both qualifying and races
- Circuit characteristics (length, number of turns)
- Multi-threaded data acquisition for efficiency

## Technology Stack

- **Programming Language**: Python
- **Web Scraping**: Selenium, BeautifulSoup4
- **Data Processing**: Pandas, NumPy
- **Database**: MongoDB Atlas
- **Data Visualization**: Matplotlib, Seaborn
- **PDF Processing**: (for qualifying speed data extraction)

## Data Quality and Validation

The project includes comprehensive data quality checks to ensure:
- Consistency in number of laps across data sources
- Validation of qualifying times
- Verification of circuit information
- Checking for missing data points
- Cross-referencing with official F1 statistics

## Analysis Capabilities

The project enables various analyses:

1. **Performance Comparisons**:
   - Year-to-year performance changes for drivers and teams
   - Impact of regulation changes between seasons
   - Comparative analysis of different car designs

2. **Circuit Analysis**:
   - Relationships between circuit characteristics and performance
   - Impact of circuit length and turns on lap times and maximum speeds

3. **Weather Impact Assessment**:
   - Effect of weather conditions on qualifying performance
   - Impact of rain on race strategies and outcomes

4. **Lap Time Analysis**:
   - Sectional performance across different parts of races
   - Consistency analysis throughout race distance
   - Tire degradation patterns

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB Atlas account
- Chrome WebDriver (compatible with your Chrome version)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/f1-data-management.git
   cd f1-data-management
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure MongoDB connection:
   - Update the connection string in `Storage/Connection.py`

### Running the Data Acquisition Pipeline

Execute the main script to run the complete data acquisition process:

```
python Data\ Acquisition/main.py
```

This will:
1. Perform web scraping for seasons data
2. Convert PDF qualifying maximum speed data to JSON
3. Merge qualifying speed data with season data
4. Collect weather data for qualifying and races
5. Merge all data into final datasets

### Querying and Analysis

Example queries are provided in the `Storage` directory:
- `query1.py`: Qualifying time analysis
- `query2.py`: Lap section analysis
- `query3.py`: Circuit characteristics analysis

## Contributors

- Matteo Pasotti
- Eleonora Brambatti
- Marta Privitera


## Acknowledgments

- Formula 1 data providers
- Web scraping libraries and tools
- MongoDB Atlas for database services
