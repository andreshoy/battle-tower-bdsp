"""Genera estrategia/matchups.md: para cada set rival de Single Clase Normal, quién de tu equipo lo enfrenta mejor.

Criterio por miembro: le pega súper eficaz (+2), no recibe súper eficaz (+2), es más rápido (+1), le pega al menos
neutral (+0.5). Elige el de mayor puntaje y sugiere su mejor ataque.

Uso (desde la raíz del repo):
    .venv/bin/python estrategia/analisis/matchups.py                  # equipo 'actual' de equipo.yaml
    .venv/bin/python estrategia/analisis/matchups.py --equipo con_scizor
"""
import argparse
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from bt_data import (RISKY_ITEMS, RISKY_MOVES, damaging_types, effectiveness, load_pool,  # noqa: E402
                     move_type_map, pokemon_moves, species_types)
from cobertura import YAML_PATH, resolve_member  # noqa: E402

OUTPUT = 'estrategia/matchups.md'


def evaluate(member, r, mtypes):
    rtypes = [r['type1'], r['type2']]
    best_move, best_eff = None, 0
    for name, t in member['ataques']:
        eff = effectiveness(t, rtypes, r['ability'])
        if eff > best_eff:
            best_move, best_eff = name, eff
    threatened = [t for t in damaging_types(r, mtypes) if effectiveness(t, member['tipos'], member['habilidad']) >= 2]
    faster = member['velocidad'] is not None and member['velocidad'] > int(r['spe'])
    score = 2 * (best_eff >= 2) + 2 * (not threatened) + faster + 0.5 * (best_eff >= 1)
    return score, best_move, best_eff, threatened, faster


def warnings(r):
    moves = set(pokemon_moves(r))
    out = [cat.split(' (')[0] for cat, ms in RISKY_MOVES.items() if moves & ms]
    if r['item'] in RISKY_ITEMS:
        out.append(r['item'])
    if r['ability'] == 'Sturdy':
        out.append('Robustez')
    return ', '.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--equipo', default='actual')
    parser.add_argument('--sets', default='Set 7')
    args = parser.parse_args()

    with open(YAML_PATH, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    mtypes, stypes = move_type_map(), species_types()
    team = [resolve_member({'nombre': nm, **cfg['pokemon'][nm]}, mtypes, stypes) for nm in cfg['equipos'][args.equipo]]
    pool = load_pool(sets=tuple(s.strip() for s in args.sets.split(',')))
    sets = pool.drop_duplicates(subset=['pokemon_name', 'item', 'move1', 'move2', 'move3', 'move4'])

    lines = [f'# Enfrentamientos: {" / ".join(m["nombre"] for m in team)}\n',
             f'> Generado por `estrategia/analisis/matchups.py` (Sets: {args.sets} + Palmer). '
             'Úsalo junto con la app: identifica al entrenador, mira su roster y busca aquí cada Pokémon.  ',
             '> **Respuesta** = quién de tu equipo lo enfrenta mejor y con qué ataque. '
             '⚡ = eres más rápido. ⚠ = ese miembro recibe súper eficaz.  ',
             '> Limitación: solo considera tipos y velocidad, no si el ataque es físico o especial ni las stats '
             'defensivas. Ejemplo: contra Blissey conviene Gyarados (físico) aunque la tabla diga Gastrodon. '
             'Revisa las notas de [equipo.md](equipo.md).\n',
             '| Rival | Objeto | Vel | Respuesta | Alternativa | Cuidado con |', '|---|---|---|---|---|---|']
    hard = []
    for _, r in sets.sort_values('pokemon_name').iterrows():
        ranked = sorted(((evaluate(m, r, mtypes), m['nombre']) for m in team), key=lambda x: -x[0][0])

        def fmt(entry):
            (score, move, eff, threatened, faster), name = entry
            mult = f' x{eff:g}' if eff != 1 else ''
            return f"{name}: {move}{mult}{' ⚡' if faster else ''}{' ⚠' if threatened else ''}"

        lines.append(f"| **{r['pokemon_name']}** | {r['item']} | {r['spe']} | {fmt(ranked[0])} | {fmt(ranked[1])} | "
                     f"{warnings(r)} |")
        if ranked[0][0][0] < 3:
            hard.append(r['pokemon_name'])

    lines.append(f'\n## Rivales difíciles (ningún miembro tiene un enfrentamiento claro)\n')
    lines.append(', '.join(dict.fromkeys(hard)) or '—')
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'✓ {OUTPUT} generado ({len(sets)} sets rivales distintos); difíciles: {", ".join(dict.fromkeys(hard))}')


if __name__ == '__main__':
    main()
