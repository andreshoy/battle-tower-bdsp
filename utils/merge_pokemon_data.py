import pandas as pd

def merge_data():
    try:
        # Load all three parquets
        print("Loading datasets...")
        trainers_df = pd.read_parquet('data/battle_tower_trainers.parquet')
        bosses_df = pd.read_parquet('data/battle_tower_bosses.parquet')
        ref_df = pd.read_parquet('data/pokemon_types_reference.parquet')
        
        # 1. Prepare Standard Trainers
        # Mark them as 'Standard' temporarily to identify them
        trainers_df['battle_mode'] = 'Standard'
        
        # 2. Prepare Bosses
        # Simplify battle_mode names
        bosses_df['battle_mode'] = bosses_df['battle_mode'].replace({
            'Single Battles': 'Single',
            'Master Class Single Battles': 'Single',
            'Master Class Double Battles': 'Double'
        })
            
        # Drop types if they exist to avoid merge conflicts/duplicates
        trainers_df = trainers_df.drop(columns=['type1', 'type2'], errors='ignore')
        bosses_df = bosses_df.drop(columns=['type1', 'type2'], errors='ignore')
        
        # Concatenate trainers and bosses
        print(f"Combining {len(trainers_df)} trainers and {len(bosses_df)} bosses...")
        combined_df = pd.concat([trainers_df, bosses_df], ignore_index=True)
        
        # 3. Apply the Single/Double logic for Standard trainers
        # Group by trainer, set, and team, then use cumcount to get the position (0-6)
        print("Applying Single/Double logic to standard trainers...")
        mask_standard = combined_df['battle_mode'] == 'Standard'
        # We need to ensure we group by the columns that define a "team"
        group_cols = ['trainer_name', 'Set', 'Team']
        pos_in_team = combined_df[mask_standard].groupby(group_cols).cumcount()
        
        # Assign Single to first 3, Double to the rest
        combined_df.loc[mask_standard, 'battle_mode'] = pos_in_team.apply(
            lambda x: 'Single' if x < 3 else 'Double'
        )
        
        # 4. Merge with types based on pokemon_name
        print("Merging with type references...")
        merged_df = combined_df.merge(ref_df, on='pokemon_name', how='left')
        
        # Robust column reordering
        cols = list(merged_df.columns)
        if 'pokemon_name' in cols and 'type1' in cols and 'type2' in cols:
            base_cols = ['battle_mode', 'trainer_class', 'trainer_name', 'Set', 'Team', 'pokemon_name', 'type1', 'type2']
            remaining_cols = [c for c in cols if c not in base_cols]
            final_cols = [c for c in base_cols if c in cols] + remaining_cols
            merged_df = merged_df[final_cols]
        
        # Save the final combined dataset to a new file
        output_file = 'data/final_battle_tower_data.parquet'
        merged_df.to_parquet(output_file, index=False)
        
        print(f"✓ Combined and merged data saved to '{output_file}'")
        print(f"Total rows: {len(merged_df)}")
        
        # Verification snippet
        print("\n--- Verification: Sample of Standard Trainer (Set 7) ---")
        sample_std = merged_df[(merged_df['trainer_name'] == 'Abbey') & (merged_df['Set'] == 'Set 7')].head(7)
        print(sample_std[['trainer_name', 'Set', 'Team', 'battle_mode', 'pokemon_name']])
        
        print("\n--- Verification: Sample of Bosses ---")
        print(merged_df[merged_df['Set'] == 'Boss'].head(5)[['trainer_name', 'battle_mode', 'pokemon_name']])

    except FileNotFoundError as e:
        print(f"Error: Missing files. {e}")
    except Exception as e:
        print(f"Error merging: {e}")

if __name__ == "__main__":
    merge_data()
