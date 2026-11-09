"""Potencia, categoría, precisión y prioridad de los movimientos del dataset (PokeAPI) -> data/moves_reference.parquet.

Lo usa `estrategia/analisis/rival.py --plan` para estimar el daño que te hace el rival.
Uso (desde la raíz del repo): .venv/bin/python scrapers/generate_moves_reference.py
"""
import time

import pandas as pd
import requests

OUTPUT = 'data/moves_reference.parquet'


def api_name(move):
    return move.lower().replace(' ', '-').replace("'", '').replace('.', '')


def main():
    df = pd.read_parquet('data/final_battle_tower_data.parquet')
    moves = sorted({m for i in range(1, 5) for m in df[f'move{i}'] if m and m != '-'})
    print(f'Consultando {len(moves)} movimientos en PokeAPI...')
    rows = []
    for i, move in enumerate(moves):
        try:
            r = requests.get(f'https://pokeapi.co/api/v2/move/{api_name(move)}', timeout=15)
            r.raise_for_status()
            d = r.json()
            meta = d.get('meta') or {}
            rows.append({'move': move, 'power': d['power'], 'damage_class': d['damage_class']['name'],
                         'accuracy': d['accuracy'], 'priority': d['priority'], 'type': d['type']['name'].capitalize(),
                         'min_hits': meta.get('min_hits'), 'max_hits': meta.get('max_hits')})
        except Exception as e:  # noqa: BLE001
            print(f'  ✗ {move}: {e}')
        if (i + 1) % 50 == 0:
            print(f'  {i + 1}/{len(moves)}')
        time.sleep(0.05)
    pd.DataFrame(rows).to_parquet(OUTPUT, index=False)
    print(f'✓ {OUTPUT} ({len(rows)} movimientos)')


if __name__ == '__main__':
    main()
