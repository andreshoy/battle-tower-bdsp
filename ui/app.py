from nicegui import ui
import pandas as pd

# --- DATA LOADING ---
try:
    df = pd.read_parquet('data/battle_tower_trainers.parquet')
    df = df.groupby(['trainer_name', 'Set', 'Team']).head(3).reset_index(drop=True)
except Exception as e:
    df = pd.DataFrame()

# --- STATE ---
class State:
    def __init__(self):
        self.step = 0
        self.sel_set = None
        self.sel_class = None
        self.sel_name = None
        self.sel_team = None

state = State()

# --- CONFIG & STYLES ---
TYPE_COLORS = {
    'Normal': '#A8A878', 'Fire': '#F08030', 'Water': '#6890F0', 'Grass': '#78C850',
    'Electric': '#F8D030', 'Ice': '#98D8D8', 'Fighting': '#C03028', 'Poison': '#A040A0',
    'Ground': '#E0C068', 'Flying': '#A890F0', 'Psychic': '#F85888', 'Bug': '#A8B820',
    'Rock': '#B8A038', 'Ghost': '#705898', 'Dragon': '#7038F8', 'Dark': '#705848',
    'Steel': '#B8B8D0', 'Fairy': '#EE99AC', 'Unknown': '#68A090'
}

def move_chip(name, color):
    if not name or name == "-": return None
    c = color if color and color.startswith('#') else "#C1C2C1"
    ui.label(name).style(f'background-color: {c}; color: black; font-weight: bold; border-radius: 4px; padding: 4px 8px; font-size: 0.8em; border: 1px solid rgba(0,0,0,0.1)')

def type_chip(name):
    if not name: return None
    c = TYPE_COLORS.get(name, '#C1C2C1')
    ui.label(name.upper()).style(f'background-color: {c}; color: white; font-weight: bold; border-radius: 12px; padding: 2px 10px; font-size: 0.7em; text-shadow: 1px 1px 2px rgba(0,0,0,0.3)')

# --- STATE ---
content_div = None

def go_step(n):
    state.step = n
    render_content()

@ui.page('/')
def index():
    global content_div
    # Estilo global para el cuerpo de la página
    ui.query('.q-page').style('background-color: #f5f5f5; max-width: 450px; margin: auto;')
    
    # Contenedor para la navegación superior (siempre visible)
    with ui.row().classes('w-full justify-between items-center bg-white shadow-sm p-2 sticky top-0 z-10'):
        # Botones de navegación tipo "Breadcrumbs"
        def nav_btn(label, step_target):
            is_active = state.step == step_target
            color = 'primary' if is_active else 'grey'
            return ui.button(label, on_click=lambda: go_step(step_target)).props(f'flat color={color} stack')

        nav_btn_set = ui.button('SET', on_click=lambda: go_step(0)).props('flat stack')
        ui.icon('chevron_right').classes('text-grey-4')
        nav_btn_cls = ui.button('CLS', on_click=lambda: go_step(1)).props('flat stack')
        ui.icon('chevron_right').classes('text-grey-4')
        nav_btn_nom = ui.button('NOM', on_click=lambda: go_step(2)).props('flat stack')

        # Función interna para actualizar etiquetas de la navegación
        def update_nav():
            nav_btn_set.set_text(state.sel_set.split()[-1] if state.sel_set else 'SET')
            nav_btn_set.props(f'color={"primary" if state.step==0 else "grey"}')
            
            nav_btn_cls.set_text(state.sel_class[:5] if state.sel_class else 'CLS')
            nav_btn_cls.set_visibility(state.step >= 1)
            nav_btn_cls.props(f'color={"primary" if state.step==1 else "grey"}')
            
            nav_btn_nom.set_text(state.sel_name[:5] if state.sel_name else 'NOM')
            nav_btn_nom.set_visibility(state.step >= 2)
            nav_btn_nom.props(f'color={"primary" if state.step==2 else "grey"}')

    # Contenedor dinámico principal
    content_div = ui.column().classes('w-full')
    
    # Inyectamos la función de actualización de nav en el render
    state._update_nav = update_nav
    render_content()

def render_content():
    if content_div is None: return
    content_div.clear()
    state._update_nav()

    with content_div:
        # --- PASO 0: SETS ---
        if state.step == 0:
            with ui.column().classes('w-full p-4 items-center'):
                ui.label('SELECCIONA EL SET').classes('text-h6 text-weight-bold text-grey-8 mb-4')
                sets = sorted(df['Set'].unique())
                with ui.grid(columns=2).classes('w-full gap-4'):
                    for s in sets:
                        num = s.split()[-1]
                        ui.button(num, on_click=lambda s=s: (setattr(state, 'sel_set', s), go_step(1))) \
                            .props('outline color=blue-8 size=xl').classes('h-24 text-h3 text-weight-black rounded-xl bg-white shadow-md')

        # --- PASO 1: CLASES ---
        elif state.step == 1:
            with ui.column().classes('w-full p-2'):
                ui.label(f'CLASES - SET {state.sel_set.split()[-1]}').classes('text-subtitle1 text-center w-full text-grey-7 mb-2')
                df_filtered = df[df['Set'] == state.sel_set]
                classes = sorted(df_filtered['trainer_class'].unique())
                curr_l = ""
                for c in classes:
                    if c[0] != curr_l:
                        curr_l = c[0]
                        ui.label(curr_l).classes('text-h6 text-white bg-blue-8 rounded-sm px-4 py-1 mt-4 shadow-sm w-full')
                    ui.button(c, on_click=lambda c=c: (setattr(state, 'sel_class', c), go_step(2))) \
                        .props('flat color=grey-9 align=left').classes('w-full text-left bg-white border-b border-grey-2 py-2')

        # --- PASO 2: NOMBRES ---
        elif state.step == 2:
            with ui.column().classes('w-full p-2'):
                ui.label(state.sel_class.upper()).classes('text-h6 text-center w-full text-blue-9 mb-2')
                df_filtered = df[(df['Set'] == state.sel_set) & (df['trainer_class'] == state.sel_class)]
                names = sorted(df_filtered['trainer_name'].unique())
                for n in names:
                    ui.button(n, on_click=lambda n=n: (setattr(state, 'sel_name', n), go_step(3))) \
                        .props('unelevated color=white text-color=black border').classes('w-full mb-2 h-14 text-weight-bold shadow-sm')

        # --- PASO 3: EQUIPO ---
        elif state.step == 3:
            df_f = df[(df['Set'] == state.sel_set) & (df['trainer_class'] == state.sel_class) & (df['trainer_name'] == state.sel_name)]
            teams = sorted(df_f['Team'].unique())
            if not state.sel_team: state.sel_team = teams[0]

            with ui.column().classes('w-full p-2'):
                with ui.row().classes('w-full justify-center gap-2 mb-4'):
                    for t in teams:
                        t_num = t.split()[-1]
                        ui.button(t_num, on_click=lambda t=t: (setattr(state, 'sel_team', t), render_content())) \
                            .props(f'{"unelevated" if state.sel_team==t else "outline"} color=blue-8 round')

                ui.label(f'{state.sel_name} ({state.sel_team.split()[-1]})').classes('text-h6 text-center w-full text-weight-bold')
                
                team_data = df_f[df_f['Team'] == state.sel_team]
                for _, p in team_data.iterrows():
                    with ui.card().classes('w-full mb-4 shadow-lg border-l-4 border-blue-8'):
                        with ui.row().classes('w-full items-center gap-2'):
                            ui.label(p['pokemon_name'].upper()).classes('text-h5 text-weight-bolder text-grey-10')
                            type_chip(p['type1'])
                            if p['type2']: type_chip(p['type2'])
                        
                        with ui.row().classes('w-full text-grey-7 items-center'):
                            ui.label(f"Habilidad: {p['ability']} | Objeto: {p['item']}").classes('text-caption')
                        
                        # --- Stats Row ---
                        with ui.row().classes('w-full justify-between mt-2 text-center'):
                            stats = [('HP', 'hp'), ('Atk', 'atk'), ('Def', 'def'), ('SpA', 'spa'), ('SpD', 'spd'), ('Spe', 'spe')]
                            for label, col in stats:
                                with ui.column().classes('items-center'):
                                    ui.label(label).classes('text-caption text-weight-bold text-grey-5 uppercase')
                                    ui.label(str(p[col])).classes('text-weight-bold text-blue-9')

                        with ui.row().classes('w-full gap-1 mt-2'):
                            for m in range(1, 5):
                                move_chip(p[f'move{m}'], p[f'move{m}_color'])

import os

ui.run(title='Battle Tower BDSP', port=int(os.environ.get('PORT', 8001)), reload=False, host='0.0.0.0')
