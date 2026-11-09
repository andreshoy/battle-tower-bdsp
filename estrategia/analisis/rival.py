"""Consulta rápida de un entrenador de la Torre (Single) contra tu equipo actual.

Busca al entrenador con tolerancia a errores y acentos ("Ezequiel" -> Ezekiel, "laidy" -> Lady), muestra sus
Pokémon del Set/equipo indicado y, para cada uno: tipos, habilidad, objeto, movimientos, quién de tu equipo es
más rápido, el daño estimado de tus ataques y las trampas (Banda Focus, Levitación, Esfuerzo, Contraataque...).

Uso (desde la raíz del repo):
    .venv/bin/python estrategia/analisis/rival.py Mikaela --set 2 --team B
    .venv/bin/python estrategia/analisis/rival.py "Ezequiel" --set 2 --clase youngster
    .venv/bin/python estrategia/analisis/rival.py chaz --clase "school kid" --saco lickitung --resumen   # rápido
    .venv/bin/python estrategia/analisis/rival.py callie --saco marshtomp --campo gastrodon --resumen     # ¿me quedo?
    .venv/bin/python estrategia/analisis/rival.py callie --saco marshtomp --campo gastrodon --plan        # 3 contra 3
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


def summary(team, rows, mtypes, campo=None, saco=None):
    """Una línea por Pokémon rival con las dos mejores respuestas (golpes para KO, velocidad, riesgo).

    Con `campo`, contra el Pokémon que sacó el rival (o contra todos si no se sabe) evalúa primero a tu Pokémon en
    campo: si no recibe súper eficaz y gana en 3 golpes o menos, conviene quedarse y guardar a los otros dos.
    """
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
        if campo and (saco is None or r['pokemon_name'] == saco):
            mine = next((o for o in options if o[1] == campo), None)
            if mine:
                _, nm, (mv, lo, hi, mult), hits, faster, threats = mine
                stay = not threats and hits <= 3
                print(f"    = {nm} en campo: {mv} x{mult:g} {lo:.0%}-{hi:.0%} ({hits} golpe{'s' if hits > 1 else ''}), "
                      f"{'más rápido' if faster else 'más lento'}" + (f", recibe SE de {', '.join(threats)}" if threats else '')
                      + f" → {'QUÉDATE' if stay else 'CAMBIA'}")
        weak = [o[1] for o in options if o[5] and not o[4]]
        if weak:
            print(f"    ✗ evitar: {', '.join(weak)} (recibe SE y es más lento)")
        # Buena respuesta: gana en 2 golpes sin recibir súper eficaz, o en 1 golpe siendo más rápido.
        good = [o[1] for o in options if (not o[5] and o[3] <= 2) or (o[4] and o[3] == 1)]
        if len(good) == 1:
            print(f"    ★ única respuesta buena: {good[0]} (guárdalo para este)")
        elif not good:
            print("    ★ ninguna respuesta buena: llega con el que tenga más vida")


# --- Plan de batalla completo (--plan) ---------------------------------------------------------------------------
# Simula 3 contra 3 turno a turno con daño promedio: tú eliges el mejor ataque; el rival, el más dañino (o el que te
# deja KO, con prioridad si la tiene). Cada cambio regala un golpe al que entra. Ignora estados, cambios de stats,
# críticos y fallos; por eso es una guía para comparar planes, no una predicción exacta.
MOVES_PATH = 'data/moves_reference.parquet'
BOOST_ITEMS = {
    'Miracle Seed': 'Grass', 'Charcoal': 'Fire', 'Mystic Water': 'Water', 'Never-Melt Ice': 'Ice', 'Magnet': 'Electric',
    'Black Belt': 'Fighting', 'Poison Barb': 'Poison', 'Soft Sand': 'Ground', 'Sharp Beak': 'Flying',
    'Twisted Spoon': 'Psychic', 'Silver Powder': 'Bug', 'Hard Stone': 'Rock', 'Spell Tag': 'Ghost',
    'Dragon Fang': 'Dragon', 'Black Glasses': 'Dark', 'Metal Coat': 'Steel', 'Silk Scarf': 'Normal',
}
WEIGHT_KG = {'Gyarados': 235, 'Gastrodon': 29.9, 'Roserade': 14.5, 'Scizor': 118, 'Dragonite': 210,
             'Garchomp_criado': 95}
SKIP_MOVES = {'Counter', 'Mirror Coat', 'Metal Burst', 'Endeavor', 'Final Gambit', 'Present', 'Fling', 'Fake Out',
              'Fissure', 'Horn Drill', 'Guillotine', 'Sheer Cold', 'Explosion', 'Self-Destruct', 'Focus Punch'}


def load_moves():
    if not os.path.exists(MOVES_PATH):
        sys.exit(f'✗ Falta {MOVES_PATH}: ejecuta .venv/bin/python scrapers/generate_moves_reference.py')
    return pd.read_parquet(MOVES_PATH).set_index('move').to_dict('index')


def weight_power(kg):
    return next(p for lim, p in ((10, 20), (25, 40), (50, 60), (100, 80), (200, 100), (1e9, 120)) if kg < lim)


def rival_hit(r, move, me, intim, cur, moves):
    """(daño como fracción de tus PS, daño esperado con precisión, prioridad) de un ataque del rival, o None."""
    info = moves.get(move)
    if not info or info['damage_class'] == 'status' or move in SKIP_MOVES:
        return None
    hp = me['stats'][0]
    if move in ('Night Shade', 'Seismic Toss'):
        return 50 / hp, 50 / hp, 0
    if move == 'Super Fang':
        return cur / 2, cur / 2 * .9, 0
    power = info['power']
    if move in ('Low Kick', 'Grass Knot'):
        power = weight_power(WEIGHT_KG.get(me['nombre'], 60))
    elif move == 'Gyro Ball':
        power = min(150, 25 * me['stats'][5] / max(1, int(r['spe'])))
    elif move in ('Flail', 'Reversal'):
        power = 40
    elif move in ('Crush Grip', 'Heavy Slam'):
        power = 100 if move == 'Crush Grip' else 80
    if not power or pd.isna(power):
        return None
    if r['ability'] == 'Technician' and power <= 60:
        power *= 1.5
    phys = info['damage_class'] == 'physical'
    a = int(r['atk'] if phys else r['spa'])
    if phys and r['ability'] in ('Huge Power', 'Pure Power'):
        a *= 2
    if phys and intim and r['ability'] not in ('Clear Body', 'White Smoke', 'Hyper Cutter'):
        a = a * 2 / 3
    if (phys and r['item'] == 'Choice Band') or (not phys and r['item'] == 'Choice Specs'):
        a *= 1.5
    d = me['stats'][2] if phys else me['stats'][4]
    mtype = info['type']
    eff = effectiveness(mtype, me['tipos'], me['habilidad'])
    if eff == 0:
        return None
    rtypes = [r['type1'], r['type2'] if isinstance(r['type2'], str) else None]
    mod = eff * ((2 if r['ability'] == 'Adaptability' else 1.5) if mtype in rtypes else 1)
    mod *= {'Life Orb': 1.3, 'Muscle Band': 1.1 if phys else 1, 'Wise Glasses': 1 if phys else 1.1}.get(r['item'], 1)
    mod *= 1.2 if BOOST_ITEMS.get(r['item']) == mtype or (r['item'] == 'Expert Belt' and eff >= 2) else 1
    hits = 1
    if info['min_hits'] and not pd.isna(info['min_hits']):
        hits = 5 if r['ability'] == 'Skill Link' else (2 if info['max_hits'] == 2 else 3)
    base = int(int(int(2 * 50 / 5 + 2) * power * a / d) / 50) + 2
    dmg = int(base * mod * .925) * hits / hp
    acc = info['accuracy'] / 100 if info['accuracy'] and not pd.isna(info['accuracy']) else 1
    return dmg, dmg * acc, int(info['priority'])


def best_rival_move(r, me, intim, cur, moves):
    opts = [(mv, *h) for mv in pokemon_moves(r) if (h := rival_hit(r, mv, me, intim, cur, moves))]
    if not opts:
        return None
    kos = [o for o in opts if o[1] >= cur]
    return max(kos, key=lambda o: (o[3], o[2])) if kos else max(opts, key=lambda o: o[2])


def best_my_move(m, r):
    rtypes = [r['type1'], r['type2'] if isinstance(r['type2'], str) else None]
    opts = [(name, (lo + hi) / 2) for name, t in m['ataques'] if name in MOVE_DATA
            for lo, hi, _, _ in [damage_range(m, name, t, r, rtypes, m['habilidad'])] if hi > 0]
    return max(opts, key=lambda o: o[1]) if opts else None


def take(hp, dmg, sash):
    """Aplica daño; Banda Focus / Robustez dejan con 1 PS si estaba a vida completa (una sola vez)."""
    if sash and hp >= .999 and dmg >= hp:
        return .001, False
    return hp - dmg, sash


def duel(m, mhp, msash, r, rhp, rsash, intim, moves):
    """1 contra 1 hasta que uno cae. Devuelve (PS tuyos, Banda tuya, PS rival, Banda rival, tu ataque, turnos)."""
    mine = best_my_move(m, r)
    sitrus = r['item'] == 'Sitrus Berry'
    recovers = 0
    for turn in range(1, 31):
        theirs = best_rival_move(r, m, intim, mhp, moves)
        heal = ('Recover' in m['movs'] and mhp <= .5 and recovers < 3 and theirs and theirs[1] < .45
                and (not mine or mine[1] < rhp))
        rival_first = theirs and (theirs[3] > 0 or int(r['spe']) >= m['stats'][5])
        for actor in (('r', 'm') if rival_first else ('m', 'r')):
            if actor == 'm':
                if heal:
                    mhp, recovers = min(1, mhp + .5), recovers + 1
                elif mine:
                    rhp, rsash = take(rhp, mine[1], rsash)
                    if sitrus and 0 < rhp <= .5:
                        rhp, sitrus = rhp + .25, False
            elif theirs:
                mhp, msash = take(mhp, theirs[1], msash)
            if mhp <= 0 or rhp <= 0:
                return max(mhp, 0), msash, max(rhp, 0), rsash, ('Recover' if heal else mine and mine[0]), turn
        if m['objeto'] == 'Leftovers':
            mhp = min(1, mhp + 1 / 16)
    return mhp, msash, rhp, rsash, mine and mine[0], 30


def play(team, state, moves, r, rhp, rsash, bench, active, free, intim, depth=0, first=None):
    """Mejor plan (puntaje, líneas) desde este punto. El rival elige al siguiente que más te perjudica."""
    by_name = {m['nombre']: m for m in team}
    hps, sashes = state
    alive = [n for n in hps if hps[n] > 0]
    choices = [(n, False) for n in alive] if free else [(active, False)] + [(n, True) for n in alive if n != active]
    if first:  # fija la primera decisión para comparar las opciones de inicio
        choices = [c for c in choices if c[0] == first]
    pad = '    ' * depth
    best = None
    for name, switch in choices:
        m, h, sa = by_name[name], dict(hps), dict(sashes)
        rh, rs = rhp, rsash
        entering = switch or free
        it = (intim or (entering and m['habilidad'] == 'Intimidate'))
        txt = f"{'Cambia a ' if switch else ('Entra ' if free else 'Quédate con ')}{name}"
        if switch:
            hit = best_rival_move(r, m, it, h[name], moves)
            if hit:
                h[name], sa[name] = take(h[name], hit[1], sa[name])
                txt += f" (recibe {hit[0]} {min(hit[1], 1):.0%})"
        if h[name] > 0:
            h[name], sa[name], rh, rs, mv, turns = duel(m, h[name], sa[name], r, rh, rs, it, moves)
            txt += f" → {mv} ×{turns}"
        res = f"{r['pokemon_name']} KO" if rh <= 0 else f"cae {name}"
        txt += f": {res} · quedan {', '.join(f'{n} {max(v, 0):.0%}' for n, v in h.items())}"
        lines = [pad + txt]
        if rh <= 0 and not bench:
            score = 10 + sum(1 + v for v in h.values() if v > 0)
            lines[-1] += '  ✓ GANAS'
        elif rh <= 0:
            score, sub = None, []
            for i, nxt in enumerate(bench):
                rest = bench[:i] + bench[i + 1:]
                if not any(v > 0 for v in h.values()):
                    s, ls = -(1 + len(rest)), []
                else:
                    s, ls = play(team, (h, sa), moves, nxt, 1.0, nxt['item'] == 'Focus Sash' or nxt['ability'] == 'Sturdy',
                                 rest, name, False, False, depth + 1)
                sub += [f"{pad}  Si sale {nxt['pokemon_name']}:"] + ls
                score = s if score is None else min(score, s)
            lines += sub
        elif any(v > 0 for v in h.values()):
            score, ls = play(team, (h, sa), moves, r, rh, rs, bench, None, True, False, depth)
            lines += ls
        else:
            score = -(rh + len(bench))
            lines[-1] += '  ✗ PIERDES'
        if best is None or score > best[0]:
            best = (score, lines)
    return best


def plan(team, rows, saco, campo, moves):
    lead = rows[rows['pokemon_name'] == saco].iloc[0]
    bench = [r for _, r in rows[rows['pokemon_name'] != saco].iterrows()]
    hps = {m['nombre']: 1.0 for m in team}
    sashes = {m['nombre']: m['objeto'] == 'Focus Sash' for m in team}
    rsash = lead['item'] == 'Focus Sash' or lead['ability'] == 'Sturdy'
    print(f"\nPLAN 3 contra 3 (empieza {campo} contra {saco}; peor caso según a quién saque después el rival):")
    intim = next(m['habilidad'] == 'Intimidate' for m in team if m['nombre'] == campo)  # el líder ya entró
    results = [(*play(team, (hps, sashes), moves, lead, 1.0, rsash, bench, campo, False, intim, first=m['nombre']),
                m['nombre']) for m in team]
    # Diferencias menores a 0.2 (≈ 20% de PS en total) son empate: entonces gana quedarse, que no regala un golpe.
    top = max(r[0] for r in results)
    results.sort(key=lambda x: (-(top if x[0] >= top - .2 else x[0]), x[2] != campo, -x[0]))
    for i, (score, lines, name) in enumerate(results, 1):
        verdict = 'GANAS' if score >= 10 else 'PIERDES'
        tie = ' ≈ empate con la mejor' if i > 1 and score >= top - .2 else ''
        print(f"\n{i}) {'Quédate con' if name == campo else 'Cambia a'} {name} → {verdict} en el peor caso "
              f"(puntaje {score:.2f}{tie})")
        print('\n'.join('   ' + line for line in lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('nombre')
    parser.add_argument('--set', help='número de set (1-7); por defecto todos')
    parser.add_argument('--team', help='A, B o C; por defecto todos')
    parser.add_argument('--clase', help='clase del entrenador para desambiguar (ej. "youngster")')
    parser.add_argument('--equipo', default='actual', help='equipo de equipo.yaml')
    parser.add_argument('--saco', help='Pokémon que sacó el rival: elige solo el equipo que lo contiene')
    parser.add_argument('--resumen', action='store_true', help='salida corta con la mejor opción por Pokémon rival')
    parser.add_argument('--campo', help='tu Pokémon en campo (con --resumen dice si conviene quedarse)')
    parser.add_argument('--plan', action='store_true', help='con --saco y --campo: simula los 3 contra 3 y compara planes')
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
        member['objeto'] = data.get('objeto')
        member['movs'] = [mv.partition(':')[0].strip() for mv in data.get('movimientos', [])]
        team.append(member)

    name = matches[0]
    rows = df[df['trainer_name'] == name]
    if args.set:
        by_set = rows[rows['Set'] == f'Set {args.set}']
        # Palmer (jefe) guarda sus equipos de Clase Normal como Set='Boss', Team='Set 3' / 'Set 7'.
        rows = by_set if not by_set.empty else rows[(rows['Set'] == 'Boss') & (rows['Team'] == f'Set {args.set}')]
    if args.team:
        rows = rows[rows['Team'].str.upper().str.endswith(args.team.strip().upper())]
    saco = None
    if args.saco:
        species = {norm(p): p for p in rows['pokemon_name'].unique()}
        hit = difflib.get_close_matches(norm(args.saco), species.keys(), n=1, cutoff=0.6)
        if hit:
            saco = species[hit[0]]
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
        campo = next((m['nombre'] for m in team if args.campo and norm(m['nombre']) == norm(args.campo)), None)
        if args.resumen or args.plan:
            summary(team, g, mtypes, campo, saco)
            if args.plan and campo and saco:
                plan(team, g, saco, campo, load_moves())
        else:
            report(team, g, mtypes)


if __name__ == '__main__':
    main()
