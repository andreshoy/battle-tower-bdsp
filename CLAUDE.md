# Project Overview: Pokémon Battle Tower BDSP Tools

Tools to extract, process and visualize Battle Tower trainer data from Pokémon Brilliant Diamond / Shining Pearl,
plus a strategy workspace (`estrategia/`) for reaching a 100-win streak and the 5-star Trainer Card.
The user writes in Spanish; keep docs and strategy files in Spanish.

## Layout
- `data/` – Parquet datasets: `battle_tower_trainers.parquet` (regular trainers, rosters per Set/Team),
  `battle_tower_bosses.parquet` (Palmer + Master Class bosses), `final_battle_tower_data.parquet` (merged + types).
- `scrapers/` – Bulbapedia scrapers (`scrape_detailed_trainers.py`, `scrape_bosses.py`) and
  `generate_types_reference.py` (PokeAPI types → `data/pokemon_types_reference.parquet`, gitignored).
- `utils/merge_pokemon_data.py` – builds the final dataset (first 3 Pokémon of each regular team = Single, rest = Double). The user confirmed this data is correct: do not modify the data or this logic.
- `utils/generate_static_html.py` – writes the standalone `index.html` (do not edit `index.html` by hand).
- `ui/app.py` – NiceGUI mobile app (port 8001 or `$PORT`, used for Render deploys).
- `estrategia/` – strategy docs and analysis scripts (`estrategia/analisis/`).
- `.claude/skills/rival/` – `/rival` skill: live Battle Tower advice for a named trainer (uses `estrategia/analisis/rival.py`).

## Conventions
- Run every script from the repo root (paths like `data/...` are relative to it).
- Data is stored as Parquet. Dependencies in `requirements.txt`; use a `.venv`.
