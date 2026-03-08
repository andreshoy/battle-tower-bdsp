# Project Overview: Pokémon Battle Tower BDSP Tools

This project is a suite of tools designed to extract, process, and visualize Battle Tower trainer and Pokémon data from Pokémon Brilliant Diamond and Shining Pearl (BDSP). It includes scrapers to gather data from Bulbapedia and interactive web applications for exploring trainer teams.

## Main Technologies
- **Python 3.x**: Core programming language.
- **BeautifulSoup4 & Requests**: For web scraping data from Bulbapedia.
- **Pandas & Pyarrow**: For data manipulation and saving/loading Parquet files.
- **NiceGUI**: A modern web framework for the mobile-optimized version of the team viewer.
- **Streamlit**: An alternative web framework used for an earlier version of the team viewer.

## Key Files
- `app_nicegui.py`: The primary, mobile-optimized web application for viewing trainer teams.
- `app.py`: A Streamlit-based version of the team viewer (kept for reference/alternative use).
- `scrape_detailed_trainers.py`: The main scraping script that fetches trainer lists and detailed Pokémon data.
- `battle_tower_trainers.parquet`: The processed dataset containing trainer and Pokémon information.
- `verify_parquet.py`: A utility script to verify the integrity and content of the Parquet file.
- `venv/`: Python virtual environment containing project dependencies.

## Building and Running

### Prerequisites
Ensure you have Python 3 installed. It is recommended to use the provided virtual environment.

### Setting up the Environment
```bash
source venv/bin/activate
# Install dependencies if needed (assuming they are already installed in venv)
# pip install requests beautifulsoup4 pandas pyarrow nicegui streamlit
```

### Running the Scraper
To update the trainer data:
```bash
python3 scrape_detailed_trainers.py
```
*Note: The script is currently set to a "demo" mode (first 5 links). Remove the limit in `main()` for a full download.*

### Running the Web Applications

**NiceGUI Version (Recommended for Mobile/Tablet):**
```bash
python3 app_nicegui.py
```
This will run the server on `http://localhost:8001` (and your local network IP).

**Streamlit Version:**
```bash
streamlit run app.py
```

## Development Conventions
- **Data Storage**: Data is primarily stored in Parquet format (`.parquet`) for efficiency and schema preservation.
- **UI Design**: The NiceGUI version is specifically designed for touch-screen devices (mobile/tablet) with large buttons and step-by-step navigation.
- **State Management**: Navigation state in the web apps is managed using `session_state` (Streamlit) or a custom `State` class (NiceGUI).
