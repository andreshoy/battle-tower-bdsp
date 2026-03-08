import pandas as pd
import requests
import time

def fetch_reference_types():
    # 1. Load your current data to know which Pokemon we need
    try:
        main_df = pd.read_parquet('data/battle_tower_trainers.parquet')
        unique_names = main_df['pokemon_name'].unique()
    except Exception as e:
        print(f"Error loading main database: {e}")
        return

    print(f"Fetching types for {len(unique_names)} unique Pokemon from PokeAPI...")
    
    type_data = []
    for i, name in enumerate(unique_names):
        # Normalize name for API (e.g., "Mime Jr." -> "mime-jr")
        api_name = name.lower().replace(' ', '-').replace('.', '').replace("'", "")
        
        # Special cases for PokeAPI if needed (e.g., Nidoran)
        if "nidoran" in api_name:
            if "female" in api_name or "♀" in api_name: api_name = "nidoran-f"
            else: api_name = "nidoran-m"

        url = f"https://pokeapi.co/api/v2/pokemon/{api_name}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                types = [t['type']['name'].capitalize() for t in data['types']]
                t1 = types[0]
                t2 = types[1] if len(types) > 1 else None
                type_data.append({'pokemon_name': name, 'type1': t1, 'type2': t2})
                print(f"[{i+1}/{len(unique_names)}] {name}: {t1}{'/' + t2 if t2 else ''}")
            else:
                print(f"[{i+1}/{len(unique_names)}] ✗ {name} not found in API")
                type_data.append({'pokemon_name': name, 'type1': 'Unknown', 'type2': None})
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            type_data.append({'pokemon_name': name, 'type1': 'Error', 'type2': None})
        
        time.sleep(0.05) # Be kind to the API

    # Save to a separate reference parquet
    ref_df = pd.DataFrame(type_data)
    ref_df.to_parquet('data/pokemon_types_reference.parquet', index=False)
    print("\n✓ Created 'data/pokemon_types_reference.parquet'")

if __name__ == "__main__":
    fetch_reference_types()
