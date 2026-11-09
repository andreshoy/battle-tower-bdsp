"""Datos compartidos para los análisis de estrategia: tabla de tipos, carga del pool rival y utilidades.

Se ejecuta siempre desde la raíz del repo (las rutas `data/...` son relativas a ella).
"""
import pandas as pd

FINAL_PATH = 'data/final_battle_tower_data.parquet'

# Bulbapedia colorea cada movimiento según su tipo; el scraper guardó ese color.
COLOR_TO_TYPE = {
    '#C1C2C1': 'Normal', '#EF7374': 'Fire', '#74ACF5': 'Water', '#82C274': 'Grass',
    '#FCD659': 'Electric', '#81DFF7': 'Ice', '#FFAC59': 'Fighting', '#B884DD': 'Poison',
    '#B88E6F': 'Ground', '#ADD2F5': 'Flying', '#F584A8': 'Psychic', '#B8C26A': 'Bug',
    '#CBC7AD': 'Rock', '#A284A2': 'Ghost', '#8D98EC': 'Dragon', '#998B8C': 'Dark',
    '#98C2D1': 'Steel', '#F5A2F5': 'Fairy',
}

# Multiplicadores atacante -> defensor (solo los distintos de 1).
TYPE_CHART = {
    'Normal':   {'Rock': .5, 'Steel': .5, 'Ghost': 0},
    'Fire':     {'Grass': 2, 'Ice': 2, 'Bug': 2, 'Steel': 2, 'Fire': .5, 'Water': .5, 'Rock': .5, 'Dragon': .5},
    'Water':    {'Fire': 2, 'Ground': 2, 'Rock': 2, 'Water': .5, 'Grass': .5, 'Dragon': .5},
    'Grass':    {'Water': 2, 'Ground': 2, 'Rock': 2, 'Fire': .5, 'Grass': .5, 'Poison': .5, 'Flying': .5,
                 'Bug': .5, 'Dragon': .5, 'Steel': .5},
    'Electric': {'Water': 2, 'Flying': 2, 'Electric': .5, 'Grass': .5, 'Dragon': .5, 'Ground': 0},
    'Ice':      {'Grass': 2, 'Ground': 2, 'Flying': 2, 'Dragon': 2, 'Fire': .5, 'Water': .5, 'Ice': .5, 'Steel': .5},
    'Fighting': {'Normal': 2, 'Ice': 2, 'Rock': 2, 'Dark': 2, 'Steel': 2, 'Poison': .5, 'Flying': .5,
                 'Psychic': .5, 'Bug': .5, 'Fairy': .5, 'Ghost': 0},
    'Poison':   {'Grass': 2, 'Fairy': 2, 'Poison': .5, 'Ground': .5, 'Rock': .5, 'Ghost': .5, 'Steel': 0},
    'Ground':   {'Fire': 2, 'Electric': 2, 'Poison': 2, 'Rock': 2, 'Steel': 2, 'Grass': .5, 'Bug': .5, 'Flying': 0},
    'Flying':   {'Grass': 2, 'Fighting': 2, 'Bug': 2, 'Electric': .5, 'Rock': .5, 'Steel': .5},
    'Psychic':  {'Fighting': 2, 'Poison': 2, 'Psychic': .5, 'Steel': .5, 'Dark': 0},
    'Bug':      {'Grass': 2, 'Psychic': 2, 'Dark': 2, 'Fire': .5, 'Fighting': .5, 'Poison': .5, 'Flying': .5,
                 'Ghost': .5, 'Steel': .5, 'Fairy': .5},
    'Rock':     {'Fire': 2, 'Ice': 2, 'Flying': 2, 'Bug': 2, 'Fighting': .5, 'Ground': .5, 'Steel': .5},
    'Ghost':    {'Psychic': 2, 'Ghost': 2, 'Dark': .5, 'Normal': 0},
    'Dragon':   {'Dragon': 2, 'Steel': .5, 'Fairy': 0},
    'Dark':     {'Psychic': 2, 'Ghost': 2, 'Fighting': .5, 'Dark': .5, 'Fairy': .5},
    'Steel':    {'Ice': 2, 'Rock': 2, 'Fairy': 2, 'Fire': .5, 'Water': .5, 'Electric': .5, 'Steel': .5},
    'Fairy':    {'Fighting': 2, 'Dragon': 2, 'Dark': 2, 'Fire': .5, 'Poison': .5, 'Steel': .5},
}

# Habilidades que anulan un tipo de ataque (mecánicas de BDSP / Gen 8).
ABILITY_IMMUNITY = {
    'Levitate': 'Ground', 'Flash Fire': 'Fire', 'Water Absorb': 'Water', 'Storm Drain': 'Water',
    'Dry Skin': 'Water', 'Volt Absorb': 'Electric', 'Lightning Rod': 'Electric',
    'Motor Drive': 'Electric', 'Sap Sipper': 'Grass',
}

# Movimientos sin daño o cuyo daño no depende de la efectividad de tipo.
NON_DAMAGING = {
    'Acid Armor', 'Acupressure', 'Agility', 'Amnesia', 'Aqua Ring', 'Attract', 'Aurora Veil', 'Baby-Doll Eyes',
    'Baton Pass', 'Belly Drum', 'Block', 'Bulk Up', 'Calm Mind', 'Charge', 'Charm', 'Confuse Ray', 'Conversion',
    'Copycat', 'Cosmic Power', 'Cotton Spore', 'Curse', 'Defend Order', 'Defense Curl', 'Destiny Bond', 'Detect',
    'Disable', 'Double Team', 'Dragon Dance', 'Encore', 'Endure', 'Fake Tears', 'Feather Dance', 'Flash',
    'Flatter', 'Focus Energy', 'Follow Me', 'Glare', 'Growl', 'Growth', 'Grudge', 'Hail', 'Harden', 'Haze',
    'Heal Bell', 'Helping Hand', 'Howl', 'Hypnosis', 'Imprison', 'Ingrain', 'Iron Defense', 'Leech Seed', 'Leer',
    'Light Screen', 'Lock-On', 'Lovely Kiss', 'Lunar Dance', 'Magic Coat', 'Magnet Rise', 'Mean Look', 'Memento',
    'Metal Sound', 'Metronome', 'Milk Drink', 'Mimic', 'Mind Reader', 'Minimize', 'Mist', 'Moonlight',
    'Morning Sun', 'Nasty Plot', 'Pain Split', 'Perish Song', 'Poison Gas', 'Poison Powder', 'Power Split',
    'Power Trick', 'Protect', 'Psych Up', 'Quick Guard', 'Quiver Dance', 'Rain Dance', 'Recover', 'Recycle',
    'Reflect', 'Rest', 'Roar', 'Rock Polish', 'Role Play', 'Roost', 'Safeguard', 'Sand Attack', 'Sandstorm',
    'Scary Face', 'Screech', 'Shell Smash', 'Sing', 'Skill Swap', 'Slack Off', 'Sleep Powder', 'Sleep Talk',
    'Smokescreen', 'Soft-Boiled', 'Spikes', 'Spite', 'Splash', 'Spore', 'Stealth Rock', 'Sticky Web',
    'Stockpile', 'Strength Sap', 'String Shot', 'Stun Spore', 'Substitute', 'Sunny Day', 'Supersonic', 'Swagger',
    'Swallow', 'Sweet Kiss', 'Sweet Scent', 'Swords Dance', 'Synthesis', 'Tail Whip', 'Taunt', 'Teeter Dance',
    'Thunder Wave', 'Tickle', 'Torment', 'Toxic', 'Toxic Spikes', 'Toxic Thread', 'Trick', 'Trick Room',
    'Whirlwind', 'Wide Guard', 'Will-O-Wisp', 'Wish', 'Withdraw', 'Worry Seed', 'Yawn',
    # Daño fijo / reflejado
    'Night Shade', 'Seismic Toss', 'Super Fang', 'Endeavor', 'Final Gambit', 'Counter', 'Mirror Coat',
    'Metal Burst', 'Present', 'Fling', 'Bide',
}

# Peligros específicos para una racha larga: agrupados por categoría.
RISKY_MOVES = {
    'OHKO (fulminan de un golpe)': {'Fissure', 'Horn Drill', 'Guillotine', 'Sheer Cold'},
    'Sueño': {'Hypnosis', 'Spore', 'Sleep Powder', 'Sing', 'Lovely Kiss', 'Yawn', 'Grass Whistle', 'Dark Void'},
    'Confusión / Atracción': {'Swagger', 'Flatter', 'Confuse Ray', 'Supersonic', 'Sweet Kiss', 'Teeter Dance',
                              'Attract', 'Dynamic Punch'},
    'Evasión / Precisión': {'Double Team', 'Minimize', 'Sand Attack', 'Smokescreen', 'Flash', 'Mud-Slap',
                            'Octazooka', 'Muddy Water'},
    'Parálisis / Quemadura / Tóxico': {'Thunder Wave', 'Glare', 'Stun Spore', 'Nuzzle', 'Will-O-Wisp', 'Toxic',
                                       'Scald', 'Lava Plume', 'Discharge', 'Body Slam', 'Force Palm'},
    'Mejora (setup)': {'Swords Dance', 'Dragon Dance', 'Calm Mind', 'Nasty Plot', 'Quiver Dance', 'Bulk Up',
                       'Shell Smash', 'Belly Drum', 'Rock Polish', 'Agility', 'Cosmic Power', 'Iron Defense',
                       'Curse', 'Growth', 'Stockpile', 'Acupressure'},
    'Prioridad': {'Extreme Speed', 'Aqua Jet', 'Bullet Punch', 'Ice Shard', 'Mach Punch', 'Quick Attack',
                  'Shadow Sneak', 'Sucker Punch', 'Vacuum Wave', 'Fake Out', 'Feint'},
    'Devolver daño / kamikaze': {'Counter', 'Mirror Coat', 'Metal Burst', 'Destiny Bond', 'Explosion',
                                 'Perish Song', 'Final Gambit', 'Endeavor', 'Memento', 'Lunar Dance'},
    'Trampa / cambio': {'Mean Look', 'Block', 'Whirlpool', 'Fire Spin', 'Sand Tomb', 'Wrap', 'Bind',
                        'Magma Storm', 'Roar', 'Whirlwind', 'Encore', 'Taunt', 'Trick', 'Perish Song'},
}

RISKY_ITEMS = {
    'Focus Sash': 'aguanta un golpe con 1 PS si está a vida completa',
    'Focus Band': '10% de aguantar con 1 PS',
    'Bright Powder': 'baja tu precisión',
    'Lax Incense': 'baja tu precisión',
    'Quick Claw': '20% de moverse primero',
    "King's Rock": 'probabilidad extra de retroceso',
    'Razor Fang': 'probabilidad extra de retroceso',
    'Scope Lens': 'más golpes críticos',
    'Razor Claw': 'más golpes críticos',
    'Custap Berry': 'se mueve primero con poca vida',
    'Choice Scarf': 'más velocidad (te puede adelantar)',
    'Choice Band': 'más ataque físico',
    'Choice Specs': 'más ataque especial',
    'Life Orb': 'más daño',
    'Salac Berry': 'sube velocidad con poca vida',
    'Liechi Berry': 'sube ataque con poca vida',
    'Petaya Berry': 'sube ataque especial con poca vida',
}


def effectiveness(move_type, defender_types, defender_ability=None):
    """Multiplicador de un ataque de `move_type` contra un defensor."""
    if defender_ability and ABILITY_IMMUNITY.get(defender_ability) == move_type:
        return 0.0
    mult = 1.0
    for t in defender_types:
        if t:
            mult *= TYPE_CHART[move_type].get(t, 1)
    return mult


def move_type_map():
    """Diccionario movimiento -> tipo construido a partir de los colores del dataset."""
    df = pd.read_parquet(FINAL_PATH)
    mapping = {}
    for i in range(1, 5):
        for move, color in zip(df[f'move{i}'], df[f'move{i}_color']):
            if move and move != '-' and color in COLOR_TO_TYPE:
                mapping[move] = COLOR_TO_TYPE[color]
    return mapping


def species_types():
    """Diccionario especie -> (tipo1, tipo2) según la referencia de PokeAPI incluida en el dataset final."""
    df = pd.read_parquet(FINAL_PATH).drop_duplicates('pokemon_name')
    return {r.pokemon_name: (r.type1, r.type2 if isinstance(r.type2, str) else None) for r in df.itertuples()}


def load_pool(sets=('Set 7',), palmer_sets=('Set 7',)):
    """Pool rival para Single de Clase Normal, tomado de `final_battle_tower_data.parquet` (mismos datos de la app).

    Incluye los Pokémon `battle_mode == 'Single'` de los Sets indicados, más los equipos de Palmer de Clase Normal
    indicados (`Team` 'Set 3' / 'Set 7'). Cada fila es un set concreto (especie + objeto + movimientos + stats nv. 50).
    """
    final = pd.read_parquet(FINAL_PATH)
    single = final[final['battle_mode'] == 'Single']
    pool = single[single['Set'].isin(sets)].copy()
    palmer = single[(single['Set'] == 'Boss') & (single['trainer_name'] == 'Palmer') &
                    (single['Team'].isin(palmer_sets))].copy()
    palmer['trainer_class'] = 'Tower Tycoon'
    pool = pd.concat([pool, palmer], ignore_index=True)
    pool['type2'] = pool['type2'].where(pool['type2'].apply(lambda t: isinstance(t, str)), None)
    return pool


def pokemon_moves(row):
    return [row[f'move{i}'] for i in range(1, 5) if row[f'move{i}'] and row[f'move{i}'] != '-']


def damaging_types(row, mtypes):
    """Tipos de los movimientos ofensivos (con efectividad) de una fila del pool."""
    return {mtypes[m] for m in pokemon_moves(row) if m not in NON_DAMAGING and m in mtypes}
