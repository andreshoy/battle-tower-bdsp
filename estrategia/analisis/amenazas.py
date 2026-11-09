"""Genera estrategia/amenazas.md: qué Pokémon, objetos y movimientos rivales esperar en Single de Clase Normal.

Uso (desde la raíz del repo):
    .venv/bin/python estrategia/analisis/amenazas.py                # Set 7 + Palmer (Set 7)
    .venv/bin/python estrategia/analisis/amenazas.py --sets "Set 6,Set 7"
"""
import argparse
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from bt_data import RISKY_ITEMS, RISKY_MOVES, damaging_types, load_pool, move_type_map, pokemon_moves  # noqa: E402

OUTPUT = 'estrategia/amenazas.md'


def md_table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)]
    lines += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(lines)


def type_label(r):
    return r.type1 + (f'/{r.type2}' if r.type2 else '')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sets', default='Set 7', help='Sets de entrenadores separados por coma')
    parser.add_argument('--top', type=int, default=40)
    args = parser.parse_args()
    sets = tuple(s.strip() for s in args.sets.split(','))

    pool = load_pool(sets=sets)
    mtypes = move_type_map()
    n = len(pool)
    out = []

    out.append('# Amenazas rivales: Single, Clase Normal\n')
    out.append(f'> Generado por `estrategia/analisis/amenazas.py` con los Sets: **{", ".join(sets)}** + Palmer.  ')
    out.append('> Después de la batalla 49 los sets se reinician (50-56 = Set 1, …, 92-98 = Set 7). '
               'Por defecto se analiza el Set 7, el más difícil.\n')
    out.append(f'- Sets de Pokémon en el pool: **{n}**')
    out.append(f'- Entrenadores distintos: **{pool["trainer_name"].nunique()}**')
    out.append(f'- Especies distintas: **{pool["pokemon_name"].nunique()}**\n')

    # --- Especies más frecuentes ---
    out.append('## Especies más frecuentes\n')
    rows = []
    for name, g in sorted(pool.groupby('pokemon_name'), key=lambda kv: -len(kv[1]))[:args.top]:
        r0 = g.iloc[0]
        items = Counter(g['item']).most_common(3)
        moves = Counter(m for _, r in g.iterrows() for m in pokemon_moves(r)).most_common(5)
        rows.append([name, type_label(r0), len(g), f'{len(g) / n:.1%}',
                     ', '.join(f'{i} ({c})' for i, c in items),
                     ', '.join(m for m, _ in moves),
                     f'{g["spe"].min()}–{g["spe"].max()}'])
    out.append(md_table(['Pokémon', 'Tipo', 'Sets', '% pool', 'Objetos', 'Movimientos frecuentes', 'Vel.'], rows))

    # --- Tipos defensivos ---
    out.append('\n## Tipos de los rivales (defensivo)\n')
    tc = Counter()
    for r in pool.itertuples():
        tc[r.type1] += 1
        if r.type2:
            tc[r.type2] += 1
    out.append(md_table(['Tipo', 'Sets que lo tienen', '%'],
                        [[t, c, f'{c / n:.1%}'] for t, c in tc.most_common()]))

    # --- Presión ofensiva ---
    out.append('\n## Presión ofensiva por tipo de ataque\n')
    out.append('Porcentaje de sets rivales que llevan al menos un ataque de ese tipo. '
               'Tu equipo debería no tener debilidades compartidas contra los tipos de arriba.\n')
    oc = Counter()
    for _, r in pool.iterrows():
        for t in damaging_types(r, mtypes):
            oc[t] += 1
    out.append(md_table(['Tipo de ataque', 'Sets', '%'], [[t, c, f'{c / n:.1%}'] for t, c in oc.most_common()]))

    # --- Objetos ---
    out.append('\n## Objetos\n')
    ic = Counter(pool['item'])
    out.append(md_table(['Objeto', 'Sets', 'Por qué importa'],
                        [[i, c, RISKY_ITEMS.get(i, '')] for i, c in ic.most_common(25)]))

    # --- Movimientos peligrosos ---
    out.append('\n## Movimientos peligrosos para la racha\n')
    for cat, moves in RISKY_MOVES.items():
        carriers = pool[pool.apply(lambda r: any(m in moves for m in pokemon_moves(r)), axis=1)]
        if carriers.empty:
            continue
        out.append(f'### {cat}: {len(carriers)} sets ({len(carriers) / n:.1%})\n')
        by_species = Counter()
        for _, r in carriers.iterrows():
            for m in pokemon_moves(r):
                if m in moves:
                    by_species[(r['pokemon_name'], m)] += 1
        out.append(', '.join(f'{p} – {m} ({c})' for (p, m), c in by_species.most_common(25)) + '\n')

    # --- Habilidades a tener en cuenta ---
    out.append('## Habilidades a tener en cuenta\n')
    watch = ['Sturdy', 'Levitate', 'Intimidate', 'Flash Fire', 'Water Absorb', 'Volt Absorb', 'Lightning Rod',
             'Storm Drain', 'Motor Drive', 'Multiscale', 'Static', 'Flame Body', 'Poison Point', 'Effect Spore',
             'Cute Charm', 'Sand Veil', 'Snow Cloak', 'Rough Skin', 'Shed Skin', 'Guts', 'Marvel Scale',
             'Speed Boost', 'Moody', 'Unaware', 'Drizzle', 'Drought', 'Sand Stream', 'Snow Warning', 'Wonder Guard']
    ac = Counter(a for a in pool['ability'] if a in watch)
    out.append(md_table(['Habilidad', 'Sets'], ac.most_common()))

    # --- Palmer ---
    out.append('\n## Palmer (Magnate de la Torre)\n')
    palmer = pool[pool['trainer_name'] == 'Palmer']
    rows = [[r['pokemon_name'], type_label(r), r['ability'], r['item'], ', '.join(pokemon_moves(r)),
             f"{r['hp']}/{r['atk']}/{r['def']}/{r['spa']}/{r['spd']}/{r['spe']}"] for _, r in palmer.iterrows()]
    out.append(md_table(['Pokémon', 'Tipo', 'Habilidad', 'Objeto', 'Movimientos', 'PS/Atk/Def/SpA/SpD/Vel'], rows))

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print(f'✓ {OUTPUT} generado ({n} sets en el pool)')


if __name__ == '__main__':
    main()
