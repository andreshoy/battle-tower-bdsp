import pandas as pd
import json
import os
import math

def generate_html():
    # Load data
    try:
        df = pd.read_parquet('data/final_battle_tower_data.parquet')
        # We handle any potential NaNs in trainer_class (for Bosses)
        df['trainer_class'] = df['trainer_class'].fillna('Boss')
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Prepare data for JS
    # Structure: { mode: { set_name: { class_name: { trainer_name: { team_name: [pokemon_list] } } } } }
    data_struct = {}
    for _, row in df.iterrows():
        m = row['battle_mode']
        s = row['Set']
        c = row['trainer_class']
        n = row['trainer_name']
        t = row['Team']
        
        if m not in data_struct: data_struct[m] = {}
        if s not in data_struct[m]: data_struct[m][s] = {}
        if c not in data_struct[m][s]: data_struct[m][s][c] = {}
        if n not in data_struct[m][s][c]: data_struct[m][s][c][n] = {}
        if t not in data_struct[m][s][c][n]: data_struct[m][s][c][n][t] = []
        
        pokemon = row.to_dict()
        # Clean up missing types or nan
        if pokemon['type2'] is None or (isinstance(pokemon['type2'], float) and math.isnan(pokemon['type2'])): 
            pokemon['type2'] = ""
        data_struct[m][s][c][n][t].append(pokemon)

    json_data = json.dumps(data_struct)

    type_colors = {
        'Normal': '#A8A878', 'Fire': '#F08030', 'Water': '#6890F0', 'Grass': '#78C850',
        'Electric': '#F8D030', 'Ice': '#98D8D8', 'Fighting': '#C03028', 'Poison': '#A040A0',
        'Ground': '#E0C068', 'Flying': '#A890F0', 'Psychic': '#F85888', 'Bug': '#A8B820',
        'Rock': '#B8A038', 'Ghost': '#705898', 'Dragon': '#7038F8', 'Dark': '#705848',
        'Steel': '#B8B8D0', 'Fairy': '#EE99AC', 'Unknown': '#68A090'
    }

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Battle Tower BDSP</title>
    
    <!-- PWA Meta Tags -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="BT BDSP">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#1976d2">
    
    <!-- Manifest (Inline) -->
    <link rel="manifest" href='data:application/json,{{"name":"Battle Tower BDSP","short_name":"BT BDSP","start_url":".","display":"standalone","background_color":"#f5f5f5","theme_color":"#1976d2","icons":[{{"src":"https://cdn-icons-png.flaticon.com/512/188/188987.png","sizes":"512x512","type":"image/png"}}]}}'>
    
    <!-- Icon -->
    <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/188/188987.png">

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        body {{ 
            background-color: #f5f5f5; 
            font-family: sans-serif; 
            -webkit-tap-highlight-color: transparent;
            user-select: none;
        }}
        .max-w-mobile {{ max-width: 450px; margin: auto; }}
        .type-chip {{ 
            font-weight: bold; border-radius: 12px; padding: 2px 10px; font-size: 0.7em; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3); color: white; text-transform: uppercase;
        }}
        .move-chip {{
            color: black; font-weight: bold; border-radius: 4px; padding: 4px 8px; 
            font-size: 0.8em; border: 1px solid rgba(0,0,0,0.1); display: inline-block;
        }}
        .breadcrumb-btn {{ text-transform: uppercase; font-size: 0.875rem; font-weight: 500; }}
        .active-btn {{ color: #1976d2; border-bottom: 2px solid #1976d2; }}
        .inactive-btn {{ color: #9e9e9e; }}
        
        /* Safe Area for modern phones */
        .safe-top {{ padding-top: env(safe-area-inset-top); }}
    </style>
</head>
<body class="bg-gray-100">
    <div id="app" class="max-w-mobile min-h-screen bg-white shadow-xl flex flex-col">
        <!-- Navigation -->
        <div class="sticky top-0 z-10 bg-white shadow-sm p-2 flex items-center justify-between safe-top overflow-x-auto whitespace-nowrap">
            <button onclick="goStep(0)" id="nav-mod" class="breadcrumb-btn px-2 py-1">MOD</button>
            <span id="sep-set" class="material-icons text-gray-300 hidden text-sm">chevron_right</span>
            <button onclick="goStep(1)" id="nav-set" class="breadcrumb-btn px-2 py-1 hidden">SET</button>
            <span id="sep-cls" class="material-icons text-gray-300 hidden text-sm">chevron_right</span>
            <button onclick="goStep(2)" id="nav-cls" class="breadcrumb-btn px-2 py-1 hidden">CLS</button>
            <span id="sep-nom" class="material-icons text-gray-300 hidden text-sm">chevron_right</span>
            <button onclick="goStep(3)" id="nav-nom" class="breadcrumb-btn px-2 py-1 hidden">NOM</button>
        </div>

        <!-- Content -->
        <div id="content" class="flex-1 p-2"></div>
    </div>

    <script>
        const data = {json_data};
        const typeColors = {json.dumps(type_colors)};
        let state = {{
            step: 0,
            selMode: null,
            selSet: null,
            selClass: null,
            selName: null,
            selTeam: null
        }};

        function goStep(n) {{
            state.step = n;
            render();
        }}

        function render() {{
            const content = document.getElementById('content');
            content.innerHTML = '';
            updateNav();

            if (state.step === 0) {{
                renderStep0(content);
            }} else if (state.step === 1) {{
                renderStep1(content);
            }} else if (state.step === 2) {{
                renderStep2(content);
            }} else if (state.step === 3) {{
                renderStep3(content);
            }} else if (state.step === 4) {{
                renderStep4(content);
            }}
        }}

        function updateNav() {{
            const btnMod = document.getElementById('nav-mod');
            const btnSet = document.getElementById('nav-set');
            const btnCls = document.getElementById('nav-cls');
            const btnNom = document.getElementById('nav-nom');
            
            const sepSet = document.getElementById('sep-set');
            const sepCls = document.getElementById('sep-cls');
            const sepNom = document.getElementById('sep-nom');

            btnMod.innerText = state.selMode ? state.selMode.substring(0, 3).toUpperCase() : 'MOD';
            btnMod.className = `breadcrumb-btn px-2 py-1 ${{state.step === 0 ? 'active-btn' : 'inactive-btn'}}`;

            if (state.step >= 1) {{
                btnSet.classList.remove('hidden');
                sepSet.classList.remove('hidden');
                btnSet.innerText = state.selSet ? state.selSet.split(' ').pop() : 'SET';
                btnSet.className = `breadcrumb-btn px-2 py-1 ${{state.step === 1 ? 'active-btn' : 'inactive-btn'}}`;
            }} else {{
                btnSet.classList.add('hidden');
                sepSet.classList.add('hidden');
            }}

            if (state.step >= 2) {{
                btnCls.classList.remove('hidden');
                sepCls.classList.remove('hidden');
                btnCls.innerText = state.selClass ? state.selClass.substring(0, 5) : 'CLS';
                btnCls.className = `breadcrumb-btn px-2 py-1 ${{state.step === 2 ? 'active-btn' : 'inactive-btn'}}`;
            }} else {{
                btnCls.classList.add('hidden');
                sepCls.classList.add('hidden');
            }}

            if (state.step >= 3) {{
                btnNom.classList.remove('hidden');
                sepNom.classList.remove('hidden');
                btnNom.innerText = state.selName ? state.selName.substring(0, 5) : 'NOM';
                btnNom.className = `breadcrumb-btn px-2 py-1 ${{state.step === 3 ? 'active-btn' : 'inactive-btn'}}`;
            }} else {{
                btnNom.classList.add('hidden');
                sepNom.classList.add('hidden');
            }}
        }}

        function renderStep0(container) {{
            const div = document.createElement('div');
            div.className = 'flex flex-col items-center p-4';
            div.innerHTML = '<h2 class="text-xl font-bold text-gray-700 mb-6">SELECCIONA EL MODO</h2>';
            
            const col = document.createElement('div');
            col.className = 'flex flex-col w-full gap-4';
            
            // Order explicitly if possible, else just use keys
            const modes = ['Single', 'Double'].filter(m => Object.keys(data).includes(m));
            
            modes.forEach(m => {{
                const btn = document.createElement('button');
                btn.className = 'w-full h-24 text-3xl font-black rounded-xl bg-white shadow-md border-2 border-blue-600 text-blue-600 active:bg-blue-50 uppercase';
                btn.innerText = m;
                btn.onclick = () => {{
                    state.selMode = m;
                    goStep(1);
                }};
                col.appendChild(btn);
            }});
            div.appendChild(col);
            container.appendChild(div);
        }}

        function renderStep1(container) {{
            const div = document.createElement('div');
            div.className = 'flex flex-col items-center p-4';
            div.innerHTML = `<h2 class="text-xl font-bold text-gray-700 mb-6">SETS - ${{state.selMode.toUpperCase()}}</h2>`;
            
            const grid = document.createElement('div');
            grid.className = 'grid grid-cols-2 gap-4 w-full';
            
            Object.keys(data[state.selMode]).sort().forEach(s => {{
                const btn = document.createElement('button');
                btn.className = 'h-24 text-3xl font-black rounded-xl bg-white shadow-md border-2 border-blue-600 text-blue-600 active:bg-blue-50';
                btn.innerText = s.includes(' ') ? s.split(' ').pop() : s;
                btn.onclick = () => {{
                    state.selSet = s;
                    goStep(2);
                }};
                grid.appendChild(btn);
            }});
            div.appendChild(grid);
            container.appendChild(div);
        }}

        function renderStep2(container) {{
            const div = document.createElement('div');
            div.className = 'w-full p-2';
            div.innerHTML = `<h2 class="text-lg text-center text-gray-600 mb-2">CLASES - ${{state.selSet}}</h2>`;
            
            const classes = Object.keys(data[state.selMode][state.selSet]).sort();
            let currL = '';
            classes.forEach(c => {{
                if (c[0] !== currL) {{
                    currL = c[0];
                    const header = document.createElement('div');
                    header.className = 'text-lg text-white bg-blue-600 rounded-sm px-4 py-1 mt-4 shadow-sm w-full font-bold';
                    header.innerText = currL;
                    div.appendChild(header);
                }}
                const btn = document.createElement('button');
                btn.className = 'w-full text-left bg-white border-b border-gray-200 py-3 px-4 text-gray-800 hover:bg-gray-50';
                btn.innerText = c;
                btn.onclick = () => {{
                    state.selClass = c;
                    goStep(3);
                }};
                div.appendChild(btn);
            }});
            container.appendChild(div);
        }}

        function renderStep3(container) {{
            const div = document.createElement('div');
            div.className = 'w-full p-2';
            div.innerHTML = `<h2 class="text-xl font-bold text-center text-blue-800 mb-4 uppercase mt-2">${{state.selClass}}</h2>`;
            
            const names = Object.keys(data[state.selMode][state.selSet][state.selClass]).sort();
            names.forEach(n => {{
                const btn = document.createElement('button');
                btn.className = 'w-full mb-3 h-14 font-bold bg-white border border-gray-300 rounded shadow-sm active:bg-gray-100';
                btn.innerText = n;
                btn.onclick = () => {{
                    state.selName = n;
                    state.selTeam = null; // Reset team selection
                    goStep(4);
                }};
                div.appendChild(btn);
            }});
            container.appendChild(div);
        }}

        function renderStep4(container) {{
            const teamsData = data[state.selMode][state.selSet][state.selClass][state.selName];
            const teams = Object.keys(teamsData).sort();
            if (!state.selTeam || !teams.includes(state.selTeam)) state.selTeam = teams[0];

            const div = document.createElement('div');
            div.className = 'w-full p-2';

            // Team selector buttons
            const btnRow = document.createElement('div');
            btnRow.className = 'flex justify-center gap-2 mb-4';
            teams.forEach(t => {{
                const tLabel = t.includes(' ') ? t.split(' ').pop() : t;
                const btn = document.createElement('button');
                const isActive = state.selTeam === t;
                btn.className = `w-10 h-10 rounded-full border-2 border-blue-600 font-bold ${{isActive ? 'bg-blue-600 text-white' : 'text-blue-600 bg-white'}}`;
                btn.innerText = tLabel;
                btn.onclick = () => {{
                    state.selTeam = t;
                    render();
                }};
                btnRow.appendChild(btn);
            }});
            div.appendChild(btnRow);

            const title = document.createElement('h2');
            title.className = 'text-xl font-bold text-center mb-4';
            title.innerText = `${{state.selName}} (${{state.selTeam}})`;
            div.appendChild(title);

            const pokemonList = teamsData[state.selTeam];
            pokemonList.forEach(p => {{
                const card = document.createElement('div');
                card.className = 'bg-white rounded-lg p-4 mb-4 shadow-md border-l-4 border-blue-600';
                
                // Header: Name and Types
                const header = document.createElement('div');
                header.className = 'flex items-center gap-2 mb-1';
                header.innerHTML = `<span class="text-xl font-black text-gray-900">${{p.pokemon_name.toUpperCase()}}</span>`;
                
                const t1 = document.createElement('span');
                t1.className = 'type-chip';
                t1.style.backgroundColor = typeColors[p.type1] || '#C1C2C1';
                t1.innerText = p.type1;
                header.appendChild(t1);

                if (p.type2 && p.type2 !== "None" && p.type2.trim() !== "") {{
                    const t2 = document.createElement('span');
                    t2.className = 'type-chip';
                    t2.style.backgroundColor = typeColors[p.type2] || '#C1C2C1';
                    t2.innerText = p.type2;
                    header.appendChild(t2);
                }}
                card.appendChild(header);

                // Ability and Item
                const sub = document.createElement('div');
                sub.className = 'text-xs text-gray-500 mb-3';
                sub.innerText = `Habilidad: ${{p.ability}} | Objeto: ${{p.item}}`;
                card.appendChild(sub);

                // Stats
                const statsRow = document.createElement('div');
                statsRow.className = 'flex justify-between text-center mb-3';
                const stats = [['HP', 'hp'], ['Atk', 'atk'], ['Def', 'def'], ['SpA', 'spa'], ['SpD', 'spd'], ['Spe', 'spe']];
                stats.forEach(([label, key]) => {{
                    const sCol = document.createElement('div');
                    sCol.className = 'flex flex-col';
                    sCol.innerHTML = `<span class="text-[10px] font-bold text-gray-400 uppercase">${{label}}</span>
                                     <span class="font-bold text-blue-700">${{p[key]}}</span>`;
                    statsRow.appendChild(sCol);
                }});
                card.appendChild(statsRow);

                // Moves
                const movesRow = document.createElement('div');
                movesRow.className = 'flex flex-wrap gap-1';
                for (let i = 1; i <= 4; i++) {{
                    const moveName = p[`move${{i}}`];
                    const moveColor = p[`move${{i}}_color`];
                    if (moveName && moveName !== '-' && moveName !== 'None') {{
                        const mChip = document.createElement('span');
                        mChip.className = 'move-chip';
                        mChip.style.backgroundColor = (moveColor && moveColor.startsWith('#')) ? moveColor : '#C1C2C1';
                        mChip.innerText = moveName;
                        movesRow.appendChild(mChip);
                    }}
                }}
                card.appendChild(movesRow);

                div.appendChild(card);
            }});

            container.appendChild(div);
        }}

        render();
    </script>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Successfully generated index.html")

if __name__ == "__main__":
    generate_html()
