import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from urllib.parse import urljoin

BASE_URL = "https://bulbapedia.bulbagarden.net"
LIST_URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Battle_Tower_Trainers_in_Pok%C3%A9mon_Brilliant_Diamond_and_Shining_Pearl"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_trainer_list():
    print("Fetching trainer list...")
    response = requests.get(LIST_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    header = soup.find('span', id='List_of_Trainers')
    table = header.find_parent().find_next('table', class_='roundy sortable')
    
    trainers = []
    for row in table.find_all('tr')[2:]: # Skip header rows
        cells = row.find_all('td')
        if len(cells) >= 2:
            trainer_class = cells[0].get_text(strip=True)
            name_cell = cells[1]
            name = name_cell.get_text(strip=True)
            link = name_cell.find('a')['href'] if name_cell.find('a') else None
            
            trainers.append({
                'trainer_class': trainer_class,
                'trainer_name': name,
                'link': urljoin(BASE_URL, link) if link else None
            })
    return trainers

def scrape_trainer_details(trainer):
    if not trainer['link']:
        return []
    
    # Cache pages to avoid redundant requests for trainers in the same class page
    # (Actually many trainers of same class are on same page)
    return trainer['link']

def parse_trainer_page(url, target_name):
    print(f"Parsing page for {target_name}...")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the section for the specific trainer name
    span = soup.find('span', id=target_name.replace(' ', '_'))
    if not span:
        # Try finding by text if ID doesn't match
        span = soup.find(lambda tag: tag.name == "span" and target_name in tag.text)
    
    if not span:
        return []

    # The table is usually a sibling after the header
    table = span.find_parent().find_next('table', class_='roundy')
    if not table:
        return []

    pokemon_list = []
    current_set = "Unknown"
    
    rows = table.find_all('tr')
    for row in rows:
        # Check if it's a header row for a Set (e.g., "Single Battles Set 1")
        th_header = row.find('th', colspan="18")
        if th_header:
            current_set = th_header.get_text(strip=True)
            continue
            
        cells = row.find_all(['td', 'th'])
        # A pokemon row typically has many cells. Based on previous analysis:
        # Index 2: Name, 3: Ability, 4: Item, 5-8: Moves, 9-14: Stats
        if len(cells) >= 15 and row.get('style') and 'background:#fff' in row.get('style'):
            try:
                name = cells[2].get_text(strip=True)
                ability = cells[3].get_text(strip=True)
                item = cells[4].get_text(strip=True)
                moves = [cells[i].get_text(strip=True) for i in range(5, 9)]
                stats = [cells[i].get_text(strip=True) for i in range(9, 15)]
                
                pokemon_list.append({
                    'set': current_set,
                    'pokemon_name': name,
                    'ability': ability,
                    'item': item,
                    'move1': moves[0],
                    'move2': moves[1],
                    'move3': moves[2],
                    'move4': moves[3],
                    'hp': stats[0],
                    'atk': stats[1],
                    'def': stats[2],
                    'spa': stats[3],
                    'spd': stats[4],
                    'spe': stats[5]
                })
            except Exception as e:
                continue
                
    return pokemon_list

def main():
    trainers = get_trainer_list()
    # Limit to first 20 for demonstration speed, remove slice for full download
    # trainers = trainers[:20] 
    
    all_data = []
    
    # We group by link to minimize requests
    from collections import defaultdict
    by_link = defaultdict(list)
    for t in trainers:
        if t['link']:
            by_link[t['link']].append(t)
            
    # Limit to first 5 unique links for demonstration speed
    demo_links = list(by_link.keys())
    for link in demo_links:
        link_trainers = by_link[link]
        # Fetch page once
        try:
            response = requests.get(link, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for t in link_trainers:
                target_id = t['trainer_name'].replace(' ', '_')
                span = soup.find('span', id=target_id)
                if not span: continue
                
                table = span.find_parent().find_next('table', class_='roundy')
                if not table: continue
                
                current_set = "Unknown"
                for row in table.find_all('tr'):
                    th_header = row.find('th', colspan=lambda x: x and int(x) >= 10)
                    if th_header:
                        current_set = th_header.get_text(strip=True)
                        continue
                    
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 15 and row.get('style') and 'background:#fff' in row.get('style'):
                        # Extract moves and their background colors
                        move_data = []
                        for i in range(5, 9):
                            move_name = cells[i].get_text(strip=True)
                            style = cells[i].get('style', '')
                            # Extract hex color from background: #XXXXXX
                            color = ""
                            if 'background:' in style:
                                import re
                                match = re.search(r'background:\s*(#[0-9A-Fa-f]{3,6})', style)
                                if match:
                                    color = match.group(1)
                            move_data.append((move_name, color))

                        all_data.append({
                            'trainer_class': t['trainer_class'],
                            'trainer_name': t['trainer_name'],
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
            time.sleep(0.5) # Be nice
        except Exception as e:
            print(f"Error processing {link}: {e}")

    df = pd.DataFrame(all_data)
    
    # Clean the 'set' column by removing battle type prefixes
    df['set'] = df['set'].str.replace('Single Battles ', '', regex=False)
    df['set'] = df['set'].str.replace('Double Battles ', '', regex=False)
    
    # Split 'set' column into 'Set' and 'Team'
    # Pattern: "Set 1: Team A" -> "Set 1", "Team A"
    df[['Set', 'Team']] = df['set'].str.split(': ', n=1, expand=True)
    
    # Handle missing values
    df['Set'] = df['Set'].fillna('Unknown')
    df['Team'] = df['Team'].fillna('Unknown')

    # Filter for the first 3 pokemon per trainer, set, and team
    df = df.groupby(['trainer_name', 'Set', 'Team']).head(3)
    
    # Drop the original 'set' column and reorder to put Set/Team at the beginning
    cols = ['trainer_class', 'trainer_name', 'Set', 'Team'] + [c for c in df.columns if c not in ['trainer_class', 'trainer_name', 'Set', 'Team', 'set']]
    df = df[cols]
    
    df.to_parquet('data/battle_tower_trainers.parquet', index=False)
    print(f"Saved {len(df)} rows to data/battle_tower_trainers.parquet")

if __name__ == "__main__":
    main()
