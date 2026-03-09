import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin

BASE_URL = "https://bulbapedia.bulbagarden.net"
BOSS_URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Battle_Tower_Trainers_in_Pok%C3%A9mon_Brilliant_Diamond_and_Shining_Pearl/Boss"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_color(cell):
    style = cell.get('style', '')
    if 'background:' in style:
        match = re.search(r'background:\s*(#[0-9A-Fa-f]{3,6})', style)
        if match:
            return match.group(1)
    return ""

def scrape_bosses():
    print(f"Fetching bosses from {BOSS_URL}...")
    response = requests.get(BOSS_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    all_data = []
    
    # Modes are in <h2>
    # Trainer names are in <h3>
    # The table is after the <h3>
    
    current_mode = "Unknown Mode"
    
    # Iterate through the main content
    content = soup.find('div', class_='mw-parser-output')
    if not content:
        print("Could not find content div.")
        return []

    for element in content.find_all(['h2', 'h3', 'table']):
        if element.name == 'h2':
            text = element.get_text(strip=True).replace('[edit]', '')
            if text in ['Single Battles', 'Master Class Single Battles', 'Master Class Double Battles']:
                current_mode = text
                print(f"Processing mode: {current_mode}")
        
        elif element.name == 'h3':
            # Use separator=' ' to preserve spaces between names (e.g., "Roark and Byron")
            trainer_name = element.get_text(separator=' ', strip=True).replace('[edit]', '').strip()
            print(f"  Processing trainer: {trainer_name}")
            
            # Find the next table
            table = element.find_next_sibling('table')
            if not table or 'roundy' not in table.get('class', []):
                # Sometimes there's a paragraph or something between <h3> and <table>
                table = element.find_next('table', class_='roundy')
            
            if not table:
                continue

            current_set = "Unknown"
            
            rows = table.find_all('tr')
            for row in rows:
                # Check for header row (e.g. Set 3, Team A)
                th_header = row.find('th', colspan=lambda x: x and int(x) >= 10)
                if th_header:
                    current_set = th_header.get_text(strip=True)
                    continue
                
                cells = row.find_all(['td', 'th'])
                
                # Check if it's a pokemon row (white background, usually 15+ cells)
                if len(cells) >= 15 and row.get('style') and 'background:#fff' in row.get('style'):
                    try:
                        # Indexing based on scrape_detailed_trainers.py:
                        # 2: Name, 3: Ability, 4: Item, 5-8: Moves, 9-14: Stats
                        
                        # Extract moves and colors
                        move_data = []
                        for i in range(5, 9):
                            move_name = cells[i].get_text(strip=True)
                            move_color = get_color(cells[i])
                            move_data.append((move_name, move_color))

                        all_data.append({
                            'battle_mode': current_mode,
                            'trainer_name': trainer_name,
                            'set': current_set,
                            'pokemon_name': cells[2].get_text(strip=True),
                            'ability': cells[3].get_text(strip=True),
                            'item': cells[4].get_text(strip=True),
                            'move1': move_data[0][0],
                            'move1_color': move_data[0][1],
                            'move2': move_data[1][0],
                            'move2_color': move_data[1][1],
                            'move3': move_data[2][0],
                            'move3_color': move_data[2][1],
                            'move4': move_data[3][0],
                            'move4_color': move_data[3][1],
                            'hp': cells[9].get_text(strip=True),
                            'atk': cells[10].get_text(strip=True),
                            'def': cells[11].get_text(strip=True),
                            'spa': cells[12].get_text(strip=True),
                            'spd': cells[13].get_text(strip=True),
                            'spe': cells[14].get_text(strip=True)
                        })
                    except Exception as e:
                        print(f"    Error parsing row: {e}")
                        continue
    
    return all_data

def main():
    data = scrape_bosses()
    if not data:
        print("No data scraped.")
        return

    df = pd.DataFrame(data)
    
    # Data cleaning similar to scrape_detailed_trainers.py
    # Clean 'set' column
    df['set'] = df['set'].str.replace('Single Battles ', '', regex=False)
    df['set'] = df['set'].str.replace('Double Battles ', '', regex=False)
    
    # As requested: Rename the cleaned 'set' to 'Team' and set 'Set' to "Boss"
    df['Team'] = df['set']
    df['Set'] = 'Boss'
    
    # Reorder columns
    cols = ['battle_mode', 'trainer_name', 'Set', 'Team'] + [c for c in df.columns if c not in ['battle_mode', 'trainer_name', 'Set', 'Team', 'set']]
    df = df[cols]
    
    df.to_parquet('data/battle_tower_bosses.parquet', index=False)
    print(f"Saved {len(df)} rows to data/battle_tower_bosses.parquet")

if __name__ == "__main__":
    main()
