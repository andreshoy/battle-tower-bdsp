import pandas as pd

def merge_data():
    try:
        # Load both parquets
        main_df = pd.read_parquet('data/battle_tower_trainers.parquet')
        ref_df = pd.read_parquet('data/pokemon_types_reference.parquet')
        
        # Merge them based on pokemon_name
        # Use how='left' to keep all trainers even if a type is missing
        merged_df = main_df.merge(ref_df, on='pokemon_name', how='left')
        
        # Reorder columns to put type1 and type2 after pokemon_name
        cols = list(merged_df.columns)
        p_idx = cols.index('pokemon_name') + 1
        
        # Pull types from the end and insert them after pokemon_name
        new_cols = (cols[:p_idx] + 
                    ['type1', 'type2'] + 
                    [c for c in cols[p_idx:] if c not in ['type1', 'type2']])
        
        merged_df = merged_df[new_cols]
        
        # Overwrite the original battle tower trainers file
        merged_df.to_parquet('data/battle_tower_trainers.parquet', index=False)
        print(f"✓ Merged data saved to 'data/battle_tower_trainers.parquet'")
        print(f"Sample of new data:\n{merged_df[['pokemon_name', 'type1', 'type2']].head()}")

    except FileNotFoundError:
        print("Error: Missing files. Please run 'generate_types_reference.py' first.")
    except Exception as e:
        print(f"Error merging: {e}")

if __name__ == "__main__":
    merge_data()
