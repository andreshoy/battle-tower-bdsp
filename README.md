# Battle Tower BDSP

Herramientas para consultar los equipos de la Torre Batalla de Pokémon Diamante Brillante / Perla Reluciente
y armar una estrategia para lograr la racha de 100 victorias (una de las 5 estrellas de la tarjeta de entrenador).

## Estructura

```
data/                      datasets en Parquet (entrenadores, jefes y dataset final combinado)
scrapers/                  descarga de datos desde Bulbapedia y tipos desde PokeAPI
utils/                     combinación de datos y generación del HTML estático
ui/app.py                  app NiceGUI (móvil) para consultar equipos rivales
index.html                 versión estática de la app (generada, no editar a mano)
estrategia/                plan para la racha de 100 y las 5 estrellas → ver estrategia/README.md
```

## Pipeline de datos

Todos los scripts se ejecutan desde la raíz del repo.

1. `python scrapers/scrape_detailed_trainers.py` → `data/battle_tower_trainers.parquet`
2. `python scrapers/scrape_bosses.py` → `data/battle_tower_bosses.parquet`
3. `python scrapers/generate_types_reference.py` → `data/pokemon_types_reference.parquet` (ignorado en git)
4. `python utils/merge_pokemon_data.py` → `data/final_battle_tower_data.parquet`
5. `python utils/generate_static_html.py` → `index.html`

## Instalación y uso

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python ui/app.py        # http://localhost:8001
```

---

hoyis es muy lindo.
