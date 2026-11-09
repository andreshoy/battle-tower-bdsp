"""Consulta rápida de un entrenador de la Torre (Single) contra tu equipo actual.

Busca al entrenador con tolerancia a errores y acentos ("Ezequiel" -> Ezekiel, "laidy" -> Lady), muestra sus
Pokémon del Set/equipo indicado y, para cada uno: tipos, habilidad, objeto, movimientos, quién de tu equipo es
más rápido, el daño estimado de tus ataques y las trampas (Banda Focus, Levitación, Esfuerzo, Contraataque...).

Uso (desde la raíz del repo):
    .venv/bin/python estrategia/analisis/rival.py Mikaela --set 2 --team B
    .venv/bin/python estrategia/analisis/rival.py "Ezequiel" --set 2 --clase youngster
    .venv/bin/python estrategia/analisis/rival.py chaz --clase "school kid" --saco lickitung --resumen   # rápido
"""
import argparse
import difflib
import math
import os
import sys
import unicodedata

import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(__file__))
from bt_data import (FINAL_PATH, NON_DAMAGING, RISKY_ITEMS, RISKY_MOVES, effectiveness, move_type_map,  # noqa: E402
                     pokemon_moves, species_types)
from cobertura import YAML_PATH, resolve_member  # noqa: E402

# Potencia y categoría de los ataques de tu equipo (y del Garchomp propuesto). F = físico, E = especial.
MOVE_DATA = {
    'Waterfall': (80, 'F'), 'Earthquake': (100, 'F'), 'Crunch': (80, 'F'), 'Ice Beam': (90, 'E'),
    'Earth Power': (90, 'E'), 'Scald': (80, 'E'), 'Giga Drain': (75, 'E'), 'Sludge Bomb': (90, 'E'),
    'Shadow Ball': (80, 'E'), 'Dazzling Gleam': (80, 'E'), 'X-Scissor': (80, 'F'), 'Aerial Ace': (60, 'F'),
    'Bullet Punch': (40, 'F'), 'Aqua Tail': (90, 'F'), 'Fly': (90, 'F'), 'Outrage': (120, 'F'),
    'Dragon Claw': (80, 'F'), 'Stone Edge': (100, 'F'),
}
TYPE_ITEMS = {'Dragon Fang': 'Dragon', 'Mystic Water': 'Water', 'Black Belt': 'Fighting', 'Charcoal': 'Fire'}
RESIST_BERRIES = {
    'Occa Berry': 'Fire', 'Passho Berry': 'Water', 'Wacan Berry': 'Electric', 'Rindo Berry': 'Grass',
    'Yache Berry': 'Ice', 'Chople Berry': 'Fighting', 'Kebia Berry': 'Poison', 'Shuca Berry': 'Ground',
    'Coba Berry': 'Flying', 'Payapa Berry': 'Psychic', 'Tanga Berry': 'Bug', 'Charti Berry': 'Rock',
    'Kasib Berry': 'Ghost', 'Haban Berry': 'Dragon', 'Colbur Berry': 'Dark', 'Babiri Berry': 'Steel',
    'Roseli Berry': 'Fairy', 'Chilan Berry': 'Normal',
}
TRAP_MOVES = {
    'Endeavor': 'Esfuerzo: te deja con los mismos PS que él (combo con Banda Focus)',
    'Counter': 'Contraataque: devuelve el doble del daño físico',
    'Mirror Coat': 'Manto Espejo: devuelve el doble del daño especial',
    'Metal Burst': 'Repr. Metal: devuelve 1.5x el daño recibido',
    'Destiny Bond': 'Mismo Destino: si lo dejas KO ese turno, caes tú también',
    'Perish Song': 'Canto Mortal: cambia antes de que llegue a 0',
    'Explosion': 'Explosión', 'Final Gambit': 'Sacrificio: hace daño igual a sus PS',
    'Fissure': 'OHKO', 'Horn Drill': 'OHKO', 'Guillotine': 'OHKO', 'Sheer Cold': 'OHKO',
}
STAT_COLS = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']


def norm(text):
    text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode().lower()
    return ''.join(c for c in text if c.isalnum())


def find_trainers(df, name, clase):
    """Nombres de entrenador parecidos a `name`; prueba el texto completo y cada palabra (ej. "laidy mikaela")."""
    keys = {norm(n): n for n in df['trainer_name'].dropna().unique()}
    queries = [norm(name)] + [norm(w) for w in str(name).split() if len(norm(w)) >= 3]
    scored = {}
    for q in queries:
        for k, n in keys.items():
            ratio = 1.0 if q == k else difflib.SequenceMatcher(None, q, k).ratio()
            if ratio >= 0.6:
                scored[n] = max(scored.get(n, 0), ratio)
    close = sorted(scored, key=lambda n: -scored[n])[:5]
    if clase:
        cq = norm(clase)
        filtered = [n for n in close if any(cq in norm(c) or difflib.SequenceMatcher(None, cq, norm(c)).ratio() > 0.6
                                            for c in df.loc[df['trainer_name'] == n, 'trainer_class'].fillna('Boss'))]
        close = filtered or close
    return close


def damage_range(attacker, move, mtype, defender_row, def_types, spe_attacker_ability):
    power, cat = MOVE_DATA[move]
    if spe_attacker_ability == 'Technician' and power <= 60:
        power *= 1.5
    a = attacker['stats'][1] if cat == 'F' else attacker['stats'][3]
    d = int(defender_row['def'] if cat == 'F' else defender_row['spd'])
    base = int(int(int(2 * 50 / 5 + 2) * power * a / d) / 50) + 2
    mult = effectiveness(mtype, def_types, defender_row['ability'])
    if mult == 0:
        return 0, 0, mult, []
    notes = []
    mod = mult * (1.5 if mtype in attacker['tipos'] else 1)
    if TYPE_ITEMS.get(attacker.get('objeto')) == mtype:
        mod *= 1.2
    ability = defender_row['ability']
    if ability in ('Solid Rock', 'Filter') and mult >= 2:
        mod *= 0.75
        notes.append(ability)
    if ability == 'Thick Fat' and mtype in ('Fire', 'Ice'):
        mod *= 0.5
        notes.append('Thick Fat')
    if ability == 'Multiscale':
        mod *= 0.5
        notes.append('Multiscale (1er golpe)')
    if RESIST_BERRIES.get(defender_row['item']) == mtype and (mult >= 2 or mtype == 'Normal'):
        mod *= 0.5
        notes.append(defender_row['item'] + ' (1er golpe)')
    hp = int(defender_row['hp'])
    lo, hi = int(base * mod * 0.85) / hp, int(base * mod) / hp
    return lo, hi, mult, notes


def report(team, rows, mtypes):
    for _, r in rows.iterrows():
        rtypes = [r['type1'], r['type2'] if isinstance(r['type2'], str) else None]
        moves = pokemon_moves(r)
        stats = '/'.join(str(r[c]) for c in STAT_COLS)
        print(f"\n## {r['pokemon_name']} ({'/'.join(t for t in rtypes if t)}) · {r['ability']} · {r['item']}")
        print(f"   Stats nv50 PS/Atk/Def/SpA/SpD/Vel: {stats}")
        print('   Movimientos: ' + ', '.join(f"{m} ({mtypes.get(m, '?')}{'' if m not in NON_DAMAGING else ', estado'})"
                                           for m in moves))
        traps = [TRAP_MOVES[m] for m in moves if m in TRAP_MOVES]
        traps += [f'{cat.split(" (")[0]}: {m}' for cat, ms in RISKY_MOVES.items() for m in moves
                  if m in ms and m not in TRAP_MOVES and not cat.startswith(('Mejora', 'Prioridad', 'Trampa'))]
        if r['item'] in RISKY_ITEMS:
            traps.append(f"{r['item']}: {RISKY_ITEMS[r['item']]}")
        if r['ability'] == 'Sturdy':
            traps.append('Robustez: aguanta con 1 PS desde vida completa e inmune a OHKO')
        if r['ability'] in ('Levitate',) or 'Flying' in rtypes:
            traps.append('Inmune a Tierra (Terremoto / Tierra Viva no le hacen nada)')
        if traps:
            print('   ⚠ ' + ' | '.join(dict.fromkeys(traps)))
        for m in team:
            threats = sorted({f"{mv} x{effectiveness(mtypes[mv], m['tipos'], m['habilidad']):g}" for mv in moves
                              if mv in mtypes and mv not in NON_DAMAGING
                              and effectiveness(mtypes[mv], m['tipos'], m['habilidad']) >= 2})
            immune = sorted({mv for mv in moves if mv in mtypes and mv not in NON_DAMAGING
                             and effectiveness(mtypes[mv], m['tipos'], m['habilidad']) == 0})
            speed = int(m['stats'][5]) - int(r['spe'])
            speed_txt = 'más rápido' if speed > 0 else ('empate' if speed == 0 else 'más lento')
            dmg = []
            for name, mtype in m['ataques']:
                if name not in MOVE_DATA:
                    continue
                lo, hi, mult, notes = damage_range(m, name, mtype, r, rtypes, m['habilidad'])
                tag = 'inmune' if mult == 0 else f'{lo:.0%}-{hi:.0%}'
                ko = ' KO' if mult and lo >= 1 else ''
                dmg.append(f"{name} x{mult:g} {tag}{ko}" + (f" [{', '.join(notes)}]" if notes else ''))
            line = f"   - {m['nombre']:<10} ({speed_txt}, {m['stats'][5]} vs {r['spe']})"
            line += f" | recibe SE: {', '.join(threats) or '—'}"
            if immune:
                line += f" | inmune a: {', '.join(immune)}"
            print(line)
            print('       ' + ' · '.join(dmg))


def summary(team, rows, mtypes):
    """Una línea por Pokémon rival con las dos mejores respuestas (golpes para KO, velocidad, riesgo)."""
    for _, r in rows.iterrows():
        rtypes = [r['type1'], r['type2'] if isinstance(r['type2'], str) else None]
        moves = pokemon_moves(r)
        sturdy = r['item'] == 'Focus Sash' or r['ability'] == 'Sturdy'
        options = []
        for m in team:
            best = None
            for name, mtype in m['ataques']:
                if name not in MOVE_DATA:
                    continue
                lo, hi, mult, _ = damage_range(m, name, mtype, r, rtypes, m['habilidad'])
                if lo > 0 and (best is None or lo > best[1]):
                    best = (name, lo, hi, mult)
            if not best:
                continue
            hits = max(2 if sturdy else 1, math.ceil(1 / best[1]))
            threats = [mv for mv in moves if mv in mtypes and mv not in NON_DAMAGING
                       and effectiveness(mtypes[mv], m['tipos'], m['habilidad']) >= 2]
            faster = m['stats'][5] > int(r['spe'])
            cost = hits + (0 if faster else 0.5) + (1.5 if threats and not faster else 0.75 if threats else 0)
            options.append((cost, m['nombre'], best, hits, faster, threats))
        options.sort()
        traps = [TRAP_MOVES[mv] for mv in moves if mv in TRAP_MOVES]
        if r['item'] in RISKY_ITEMS:
            traps.append(r['item'])
        if r['ability'] in ('Sturdy', 'Levitate') or 'Flying' in rtypes:
            traps.append('Robustez' if r['ability'] == 'Sturdy' else 'inmune a Tierra')
        print(f"- {r['pokemon_name']} ({'/'.join(t for t in rtypes if t)}, {r['ability']}, {r['item']}, Vel {r['spe']}, "
              f"Def {r['def']} / SpD {r['spd']}) movs: {', '.join(moves)}" + (f" ⚠ {'; '.join(traps)}" if traps else ''))
        for cost, nm, (mv, lo, hi, mult), hits, faster, threats in options[:2]:
            print(f"    → {nm}: {mv} x{mult:g} {lo:.0%}-{hi:.0%} ({hits} golpe{'s' if hits > 1 else ''}), "
                  f"{'más rápido' if faster else 'más lento'}" + (f", recibe SE de {', '.join(threats)}" if threats else ''))
        weak = [o[1] for o in options if o[5] and not o[4]]
        if weak:
            print(f"    ✗ evitar: {', '.join(weak)} (recibe SE y es más lento)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('nombre')
    parser.add_argument('--set', help='número de set (1-7); por defecto todos')
    parser.add_argument('--team', help='A, B o C; por defecto todos')
    parser.add_argument('--clase', help='clase del entrenador para desambiguar (ej. "youngster")')
    parser.add_argument('--equipo', default='actual', help='equipo de equipo.yaml')
    parser.add_argument('--saco', help='Pokémon que sacó el rival: elige solo el equipo que lo contiene')
    parser.add_argument('--resumen', action='store_true', help='salida corta con la mejor opción por Pokémon rival')
    args = parser.parse_args()

    df = pd.read_parquet(FINAL_PATH)
    df = df[df['battle_mode'] == 'Single'].copy()
    df['type2'] = df['type2'].where(df['type2'].apply(lambda t: isinstance(t, str)), None)
    matches = find_trainers(df, args.nombre, args.clase)
    if not matches:
        sys.exit(f'✗ No encontré a "{args.nombre}" en los datos Single.')

    with open(YAML_PATH, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    mtypes, stypes = move_type_map(), species_types()
    team = []
    for nm in cfg['equipos'][args.equipo]:
        data = cfg['pokemon'][nm]
        member = resolve_member({'nombre': nm, **data}, mtypes, stypes)
        member['stats'] = data['stats']
        team.append(member)

    name = matches[0]
    rows = df[df['trainer_name'] == name]
    if args.set:
        by_set = rows[rows['Set'] == f'Set {args.set}']
        # Palmer (jefe) guarda sus equipos de Clase Normal como Set='Boss', Team='Set 3' / 'Set 7'.
        rows = by_set if not by_set.empty else rows[(rows['Set'] == 'Boss') & (rows['Team'] == f'Set {args.set}')]
    if args.team:
        rows = rows[rows['Team'].str.upper().str.endswith(args.team.strip().upper())]
    if args.saco:
        species = {norm(p): p for p in rows['pokemon_name'].unique()}
        hit = difflib.get_close_matches(norm(args.saco), species.keys(), n=1, cutoff=0.6)
        if hit:
            keys = rows.loc[rows['pokemon_name'] == species[hit[0]], ['Set', 'Team']].drop_duplicates()
            if not args.set and len(keys) > 1:
                keys = keys.tail(1)  # sin set indicado: el más alto
            rows = rows.merge(keys, on=['Set', 'Team'])
            args.set = args.set or keys.iloc[0]['Set'].replace('Set ', '')
    others = [m for m in matches[1:]]
    classes = ', '.join(sorted(set(rows['trainer_class'].fillna('Boss'))))
    print(f"# {classes} {name}" + (f" — Set {args.set}" if args.set else '') + (f", Team {args.team.upper()}" if args.team else ''))
    if others:
        print(f'(otros nombres parecidos: {", ".join(others)})')
    if rows.empty:
        avail = df[df['trainer_name'] == name].groupby('Set')['Team'].apply(lambda t: ', '.join(sorted(set(t))))
        sys.exit('✗ Sin datos para ese Set/equipo. Disponible:\n' + avail.to_string())
    for team_name, g in rows.groupby(['Set', 'Team']):
        print(f'\n=== {team_name[0]} · {team_name[1]} ===')
        (summary if args.resumen else report)(team, g, mtypes)


if __name__ == '__main__':
    main()
