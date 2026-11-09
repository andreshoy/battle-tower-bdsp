"""Cruza equipos candidatos (equipo.yaml) contra el pool rival de Single Clase Normal.

Para cada Pokémon calcula:
  - amenazado: sets rivales con al menos un ataque súper eficaz contra él
  - golpea SE: sets rivales a los que pega súper eficaz con algún movimiento
  - no lo daña: sets rivales que resisten o anulan todos sus ataques
  - más rápidos: sets rivales con más velocidad que él (si se indica `velocidad`)
Y para el equipo: rivales a los que nadie pega SE y rivales que amenazan a los tres.

Uso (desde la raíz del repo):
    .venv/bin/python estrategia/analisis/cobertura.py                 # todos los equipos
    .venv/bin/python estrategia/analisis/cobertura.py --equipo actual
    .venv/bin/python estrategia/analisis/cobertura.py --trios          # ranking de todas las combinaciones de 3
"""
import argparse
import os
import sys
from itertools import combinations

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from bt_data import NON_DAMAGING, damaging_types, effectiveness, load_pool, move_type_map, species_types  # noqa: E402

YAML_PATH = os.path.join(os.path.dirname(__file__), 'equipo.yaml')


def resolve_member(m, mtypes, stypes):
    """Normaliza un miembro del YAML: tipos y tipo de cada movimiento ofensivo."""
    types = m.get('tipos') or stypes.get(m['nombre'])
    if not types:
        sys.exit(f"✗ No conozco los tipos de {m['nombre']}: agrega `tipos: [Tipo1, Tipo2]` en equipo.yaml")
    attacks = []
    for mv in m.get('movimientos', []):
        name, _, explicit = mv.partition(':')
        name = name.strip()
        if name in NON_DAMAGING:
            continue
        mtype = explicit.strip() or mtypes.get(name)
        if not mtype:
            sys.exit(f"✗ No conozco el tipo de '{name}' ({m['nombre']}): escríbelo como '{name}:Tipo'")
        attacks.append((name, mtype))
    return {'nombre': m['nombre'], 'tipos': [t for t in types if t], 'habilidad': m.get('habilidad'),
            'ataques': attacks, 'velocidad': m.get('velocidad')}


def analyze(team, pool, mtypes):
    rows = []
    for _, r in pool.iterrows():
        rtypes = [r['type1'], r['type2']]
        info = {'rival': f"{r['pokemon_name']} ({r['item']})", 'especie': r['pokemon_name'],
                'amenaza': {}, 'golpea': {}}
        for m in team:
            info['amenaza'][m['nombre']] = any(
                effectiveness(t, m['tipos'], m['habilidad']) >= 2 for t in damaging_types(r, mtypes))
            info['golpea'][m['nombre']] = max(
                (effectiveness(t, rtypes, r['ability']) for _, t in m['ataques']), default=0)
        info['spe'] = int(r['spe'])
        rows.append(info)
    return rows


def unique_species(rows):
    seen, out = set(), []
    for r in rows:
        if r['especie'] not in seen:
            seen.add(r['especie'])
            out.append(r['especie'])
    return out


def report(name, team, rows):
    n = len(rows)
    print(f'\n=== Equipo: {name} ({" / ".join(m["nombre"] for m in team)}) — {n} sets rivales ===\n')
    print(f'{"Pokémon":<14}{"Amenazado":>11}{"Golpea SE":>11}{"No lo daña":>12}{"Más rápidos":>13}')
    for m in team:
        nm = m['nombre']
        threat = sum(r['amenaza'][nm] for r in rows)
        se = sum(r['golpea'][nm] >= 2 for r in rows)
        walled = sum(r['golpea'][nm] < 1 for r in rows)
        faster = f"{sum(r['spe'] > m['velocidad'] for r in rows):>13}" if m['velocidad'] else f'{"-":>13}'
        print(f'{nm:<14}{threat:>11}{se:>11}{walled:>12}{faster}')

    nobody_se = [r for r in rows if all(v < 2 for v in r['golpea'].values())]
    all_threat = [r for r in rows if all(r['amenaza'].values())]
    print(f'\nRivales a los que NADIE pega súper eficaz: {len(nobody_se)} ({len(nobody_se) / n:.0%})')
    print('  ' + ', '.join(unique_species(nobody_se)))
    print(f'\nRivales que amenazan a los TRES: {len(all_threat)} ({len(all_threat) / n:.0%})')
    print('  ' + (', '.join(unique_species(all_threat)) or '—'))

    print('\nDebilidades defensivas (x2 o más):')
    for m in team:
        weak = [t for t in sorted({'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison',
                                   'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark',
                                   'Steel', 'Fairy'})
                if effectiveness(t, m['tipos'], m['habilidad']) >= 2]
        print(f"  {m['nombre']:<14}{', '.join(weak)}")


def rank_trios(members, pool, mtypes):
    """Ordena todas las combinaciones de 3: menos rivales sin respuesta SE y menos rivales que amenazan a los tres."""
    rows = analyze(members, pool, mtypes)
    n = len(rows)
    results = []
    for trio in combinations(members, 3):
        names = [m['nombre'] for m in trio]
        nobody_se = sum(all(r['golpea'][nm] < 2 for nm in names) for r in rows)
        all_threat = sum(all(r['amenaza'][nm] for nm in names) for r in rows)
        results.append((nobody_se + 2 * all_threat, nobody_se, all_threat, names))
    print(f'\n=== Ranking de tríos ({n} sets rivales; puntaje = sin SE + 2 x amenazan a los tres, menor es mejor) ===\n')
    print(f'{"#":>3}  {"Trío":<36}{"Sin SE":>8}{"Amenazan 3":>12}{"Puntaje":>9}')
    for i, (score, nse, at, names) in enumerate(sorted(results), 1):
        print(f'{i:>3}  {" / ".join(names):<36}{nse:>8}{at:>12}{score:>9}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--equipo', help='nombre de un equipo de equipo.yaml (por defecto todos)')
    parser.add_argument('--trios', action='store_true', help='ordena todas las combinaciones de 3 de `pokemon`')
    parser.add_argument('--sets', default='Set 7')
    args = parser.parse_args()

    with open(YAML_PATH, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    mtypes, stypes = move_type_map(), species_types()
    members = {name: resolve_member({'nombre': name, **data}, mtypes, stypes)
               for name, data in cfg['pokemon'].items()}
    pool = load_pool(sets=tuple(s.strip() for s in args.sets.split(',')))

    if args.trios:
        rank_trios(list(members.values()), pool, mtypes)
        return
    teams = cfg['equipos']
    if args.equipo:
        teams = {args.equipo: teams[args.equipo]}
    for name, names in teams.items():
        team = [members[nm] for nm in names]
        report(name, team, analyze(team, pool, mtypes))


if __name__ == '__main__':
    main()
